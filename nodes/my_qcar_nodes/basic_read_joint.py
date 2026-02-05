#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import time

class BasicReadJoint(Node):
    def __init__(self):
        super().__init__('qcar_print_joint_states')
        self.declare_parameter('topic', '/joint_states')
        topic = self.get_parameter('topic').value
        
        self.create_subscription(JointState, topic, self.cb, 10)
        self.get_logger().info(f'Subscribed to {topic}')
        
        self.last_log_time = 0.0

    def cb(self, msg: JointState):
        now = time.time()
        if now - self.last_log_time < 0.5:
            return
        self.last_log_time = now
        pairs = list(zip(msg.name, msg.position))
        # Log limited sample
        self.get_logger().info(f'Joint positions (sample): {pairs[:6]}')

def main(args=None):
    rclpy.init(args=args)
    node = BasicReadJoint()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
