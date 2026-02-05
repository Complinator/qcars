#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from sensor_msgs.msg import LaserScan
import cv2
import numpy as np
import math

class LidarVisualizer(Node):
    def __init__(self):
        super().__init__('lidar_visualizer')

        self.declare_parameter('scan_topic', '/qcar/scan')
        scan_topic = self.get_parameter('scan_topic').value

        # QoS for Gazebo sensors (usually Best Effort/Volatile)
        # Matching the Camera QoS strategy which proved successful for Gazebo
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.create_subscription(
            LaserScan,
            scan_topic,
            self.scan_callback,
            qos_profile
        )

        self.window_name = "QCar Lidar View"
        # 600x600 image
        self.width = 600
        self.height = 600
        # Scale: pixels per meter. 
        # If we want to see ~10 meters around the robot: 300px / 10m = 30 px/m
        self.scale = 30.0 
        self.image = np.zeros((self.height, self.width, 3), np.uint8)

        self.get_logger().info(f"Lidar Visualizer started on {scan_topic} (QoS: Best Effort)")

    def scan_callback(self, msg):
        # Create black image (refresh)
        self.image.fill(0)
        
        # Draw center (Robot) - Red Dot
        cx, cy = self.width // 2, self.height // 2
        cv2.circle(self.image, (cx, cy), 6, (0, 0, 255), -1) 
        # Draw small arrow for heading
        cv2.line(self.image, (cx, cy), (cx, cy - 20), (0, 0, 150), 2)

        # Extract data
        ranges = np.array(msg.ranges)
        # Filter invalid ranges
        ranges[np.isinf(ranges)] = 0
        ranges[np.isnan(ranges)] = 0
        
        # Angles
        angle_min = msg.angle_min
        angle_increment = msg.angle_increment
        
        # Vectorized calculation for performance
        indices = np.arange(len(ranges))
        angles = angle_min + indices * angle_increment
        
        # Filter out zero ranges
        valid = (ranges > 0.1) 
        
        r_valid = ranges[valid]
        a_valid = angles[valid]
        
        # Convert Polar to Cartesian (ROS Frame: X fwd, Y left)
        # x = r * cos(theta)
        # y = r * sin(theta)
        x = r_valid * np.cos(a_valid)
        y = r_valid * np.sin(a_valid)
        
        # Map to Screen Coordinates
        # Image Top-Left is (0,0).
        # We want Robot (0,0) at (cx, cy)
        # Screen X increases to RIGHT. ROS Y increases to LEFT. -> Screen X = cx - (y * scale)
        # Screen Y increases DOWN. ROS X increases UP (Forward). -> Screen Y = cy - (x * scale)
        
        px = (cx - y * self.scale).astype(np.int32)
        py = (cy - x * self.scale).astype(np.int32)
        
        # Filter points inside image bounds
        in_bounds = (px >= 0) & (px < self.width) & (py >= 0) & (py < self.height)
        
        # Draw points
        # Using numpy advanced indexing to set pixels is much faster than looping
        # However, multiple points might map to same pixel.
        px_b = px[in_bounds]
        py_b = py[in_bounds]
        
        if len(px_b) > 0:
            self.image[py_b, px_b] = (255, 255, 255) # White pixels

        # Display
        cv2.imshow(self.window_name, self.image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = LidarVisualizer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
