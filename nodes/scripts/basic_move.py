#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64

def main():
    rospy.init_node('basic_move')
    
    # Publishers to the same topics the QCar hardware node expects
    vel_pub = rospy.Publisher('/qcar/velocity_target', Float64, queue_size=10)
    steer_pub = rospy.Publisher('/qcar/steering_target', Float64, queue_size=10)
    
    rate = rospy.Rate(10)  # 10 Hz
    
    # Movement parameters (adjustable via rosparam)
    velocity = rospy.get_param('~velocity', 1.0)    # m/s
    steering = rospy.get_param('~steering', 20.0)    # radians
    
    rospy.loginfo(f"Publishing velocity: {velocity} m/s, steering: {steering} rad")
    
    while not rospy.is_shutdown():
        vel_pub.publish(Float64(data=velocity))
        steer_pub.publish(Float64(data=steering))
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass