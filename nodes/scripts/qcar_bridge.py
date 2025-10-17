#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64

class QCarTargetsBridge:
    def __init__(self):
        rospy.init_node('qcar_targets_bridge')
        
        # Subscribe to QCar target topics
        rospy.Subscriber('/qcar/velocity_target', Float64, self.velocity_callback)
        rospy.Subscriber('/qcar/steering_target', Float64, self.steering_callback)
        
        # Publishers to Gazebo controllers
        self.rl_pub = rospy.Publisher('/qcar/rl_controller/command', Float64, queue_size=10)
        self.rr_pub = rospy.Publisher('/qcar/rr_controller/command', Float64, queue_size=10)
        self.fl_pub = rospy.Publisher('/qcar/base_fl_controller/command', Float64, queue_size=10)
        self.fr_pub = rospy.Publisher('/qcar/base_fr_controller/command', Float64, queue_size=10)
        
        # Parameters
        self.wheel_radius = rospy.get_param('~wheel_radius', 0.05)  # meters
        self.max_steering = rospy.get_param('~max_steering', 0.6)   # radians
        
        rospy.loginfo("QCar targets bridge started")
    
    def velocity_callback(self, msg):
        # Convert velocity (m/s) to wheel angular velocity (rad/s)
        wheel_speed = msg.data / self.wheel_radius
        rospy.loginfo(f"Setting wheel speed to {wheel_speed} rad/s")
        
        # Send to rear wheel controllers
        self.rl_pub.publish(Float64(data=-wheel_speed))
        self.rr_pub.publish(Float64(data=wheel_speed))
    
    def steering_callback(self, msg):
        # Clamp steering angle
        steering_angle = max(-self.max_steering, min(self.max_steering, msg.data))
        
        # Send to front wheel controllers
        self.fl_pub.publish(Float64(data=steering_angle))
        self.fr_pub.publish(Float64(data=steering_angle))

if __name__ == '__main__':
    try:
        bridge = QCarTargetsBridge()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass