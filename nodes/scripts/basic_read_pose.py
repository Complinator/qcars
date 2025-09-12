#!/usr/bin/env python3
import rospy
from gazebo_msgs.msg import ModelStates

name = rospy.get_param('/qcar_model_name', 'qcar')
def cb(msg: ModelStates):
    try:
        idx = msg.name.index(name)
        pose = msg.pose[idx]
        p = pose.position
        o = pose.orientation
        rospy.loginfo_throttle(0.5, f'{name} pos=({p.x:.2f},{p.y:.2f},{p.z:.2f}) yaw(qz)={o.z:.2f}')
    except ValueError:
        pass

def main():
    rospy.init_node('qcar_print_model_states')
    topic = rospy.get_param('~topic', '/gazebo/model_states')
    rospy.Subscriber(topic, ModelStates, cb, queue_size=5)
    rospy.loginfo(f'Subscribed to {topic} (qcar_model_name param controls which model to track)')
    rospy.spin()

if __name__ == '__main__':
    main()