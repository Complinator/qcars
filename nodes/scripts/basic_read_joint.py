#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState

last = 0.0
def cb(msg: JointState):
    global last
    now = rospy.Time.now().to_sec()
    if now - last < 0.5:
        return
    last = now
    pairs = list(zip(msg.name, msg.position))
    rospy.loginfo_throttle(0.5, f'Joint positions (sample): {pairs[:6]}')

def main():
    rospy.init_node('qcar_print_joint_states')
    topic = rospy.get_param('~topic', '/joint_states')
    rospy.Subscriber(topic, JointState, cb, queue_size=10)
    rospy.loginfo(f'Subscribed to {topic}')
    rospy.spin()

if __name__ == '__main__':
    main()