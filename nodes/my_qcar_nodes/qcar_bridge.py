#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Float64MultiArray
import time
import math

class QCarTargetsBridge(Node):
    def __init__(self):
        super().__init__('qcar_targets_bridge')
        
        # Subscribe to QCar target topics
        self.create_subscription(Float64, '/qcar/velocity_target', self.velocity_callback, 10)
        self.create_subscription(Float64, '/qcar/steering_target', self.steering_callback, 10)
        
        # Publishers to Gazebo controllers
        self.rl_pub = self.create_publisher(Float64MultiArray, '/rl_controller/commands', 10)
        self.rr_pub = self.create_publisher(Float64MultiArray, '/rr_controller/commands', 10)
        self.fl_pub = self.create_publisher(Float64MultiArray, '/base_fl_controller/commands', 10)
        self.fr_pub = self.create_publisher(Float64MultiArray, '/base_fr_controller/commands', 10)
        
        # Parameters
        self.declare_parameter('wheel_radius', 0.05)
        self.declare_parameter('max_steering', 0.6)
        self.declare_parameter('steering_speed', 2.0) # Rad/s max change rate

        self.wheel_radius = self.get_parameter('wheel_radius').value
        self.max_steering = self.get_parameter('max_steering').value
        self.steering_speed = self.get_parameter('steering_speed').value
        
        # State variables for smoothing
        self.target_steering = 0.0
        self.current_steering = 0.0
        self.target_velocity = 0.0
        self.current_velocity = 0.0
        
        # Timer for control loop (50Hz)
        self.dt = 0.02
        self.create_timer(self.dt, self.control_loop)
        
        self.get_logger().info("QCar targets bridge started (with smoothing)")
    
    def velocity_callback(self, msg):
        self.target_velocity = msg.data
    
    def steering_callback(self, msg):
        # Clamp input target immediately
        self.target_steering = max(-self.max_steering, min(self.max_steering, msg.data))

    def control_loop(self):
        self.update_steering()
        self.update_velocity()
        
    def update_steering(self):
        # Slew rate limiter for steering
        diff = self.target_steering - self.current_steering
        max_change = self.steering_speed * self.dt
        
        if abs(diff) < max_change:
            self.current_steering = self.target_steering
        else:
            self.current_steering += math.copysign(max_change, diff)
            
        # Send to front wheel controllers
        msg_steer = Float64MultiArray(data=[self.current_steering])
        self.fl_pub.publish(msg_steer)
        self.fr_pub.publish(msg_steer)
        
    def update_velocity(self):
        # We can also smooth velocity if desired, but user only complained about steering "brute"
        # and direction. For now, pass velocity through but applying correct signs.
        self.current_velocity = self.target_velocity 
        
        # Convert velocity (m/s) to wheel angular velocity (rad/s)
        wheel_speed = self.current_velocity / self.wheel_radius
        
        # Fix for "one forward, one reverse": 
        # Previous code had: rl = -speed, rr = speed.
        # User said "one straight, one reverse". 
        # Assuming both should be positive for forward motion based on standard conventions (unless motors are mounted mirror)
        # We'll set both to positive and see. If robot goes backward, we negate both. 
        # If it spins, we negate one.
        # Given previous state was [-speed, speed] and it spun (one fwd, one rev), 
        # [speed, speed] should make them go same direction.
        
        msg_rl = Float64MultiArray(data=[wheel_speed])
        msg_rr = Float64MultiArray(data=[wheel_speed])
        
        self.rl_pub.publish(msg_rl)
        self.rr_pub.publish(msg_rr)

def main(args=None):
    rclpy.init(args=args)
    node = QCarTargetsBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
