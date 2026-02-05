#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class BasicMove(Node):
    def __init__(self):
        super().__init__('basic_move')
        
        # Publishers to the same topics the QCar hardware node expects
        self.vel_pub = self.create_publisher(Float64, '/qcar/velocity_target', 10)
        self.steer_pub = self.create_publisher(Float64, '/qcar/steering_target', 10)
        
        # Movement parameters
        self.declare_parameter('velocity', 0.2)
        self.declare_parameter('steering', -0.6)
        
        self.velocity = self.get_parameter('velocity').value
        self.steering = self.get_parameter('steering').value
        
        self.get_logger().info(f"Publishing velocity: {self.velocity} m/s, steering: {self.steering} rad")
        
        self.timer = self.create_timer(0.1, self.timer_callback) # 10 Hz

    def timer_callback(self):
        self.vel_pub.publish(Float64(data=self.velocity))
        self.steer_pub.publish(Float64(data=self.steering))

def main(args=None):
    rclpy.init(args=args)
    node = BasicMove()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
