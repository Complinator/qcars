#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import os
import sys

class CameraVisualizer(Node):
    def __init__(self):
        super().__init__('camera_visualizer')

        self.declare_parameter('image_topic', '/qcar/csi_front/image_raw')
        image_topic = self.get_parameter('image_topic').value
        
        self.bridge = CvBridge()
        
        # Explicit QoS profile for Gazebo (Best Effort, Volatile)
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        
        self.create_subscription(
            Image, 
            image_topic, 
            self.image_callback, 
            qos_profile
        )
        
        self.window_name = "QCar Camera Feed"
        self.cv_image = np.zeros((480, 640, 3), np.uint8)
        cv2.putText(self.cv_image, "Waiting for data...", (50, 240), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Debug info
        self.get_logger().info(f"Subscribed to {image_topic}")
        self.get_logger().info(f"DISPLAY env var: {os.environ.get('DISPLAY', 'Not Set')}")
        self.get_logger().info("Attempting to open window...")
        
        self.last_msg_time = 0
        self.msg_count = 0
        
        # Timer
        self.timer = self.create_timer(0.05, self.timer_callback) 

    def image_callback(self, msg):
        self.msg_count += 1
        self.last_msg_time = self.get_clock().now().nanoseconds
        # Throttled log
        if self.msg_count % 30 == 0:
            self.get_logger().info(f"Received {self.msg_count} images. Last size: {msg.width}x{msg.height}")
            
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            self.get_logger().error(f"CvBridge Error: {e}")

    def timer_callback(self):
        try:
            cv2.imshow(self.window_name, self.cv_image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                rclpy.shutdown()
        except cv2.error as e:
            self.get_logger().error(f"OpenCV Window Error (Headless?): {e}", throttle_duration_sec=5.0)

def main(args=None):
    rclpy.init(args=args)
    node = CameraVisualizer()
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
