#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from gazebo_msgs.msg import ModelStates

class BasicReadPose(Node):
    def __init__(self):
        super().__init__('qcar_print_model_states')
        self.declare_parameter('topic', '/gazebo/model_states')
        self.declare_parameter('qcar_model_name', 'qcar')
        
        topic = self.get_parameter('topic').value
        self.model_name = self.get_parameter('qcar_model_name').value
        
        self.create_subscription(ModelStates, topic, self.cb, 5)
        self.get_logger().info(f'Subscribed to {topic} (tracking {self.model_name})')

    def cb(self, msg: ModelStates):
        try:
            idx = msg.name.index(self.model_name)
            pose = msg.pose[idx]
            p = pose.position
            o = pose.orientation
            
            # Using logger throttle is cleaner
            self.get_logger().info(
                f'{self.model_name} pos=({p.x:.2f},{p.y:.2f},{p.z:.2f}) yaw(qz)={o.z:.2f}',
                throttle_duration_sec=0.5
            )
        except ValueError:
            pass

def main(args=None):
    rclpy.init(args=args)
    node = BasicReadPose()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
