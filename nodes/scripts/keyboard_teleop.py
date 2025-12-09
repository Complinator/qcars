#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
import sys, select, tty, termios

# Instructions for the user
msg = """
Control Your QCar!
---------------------------
Moving around:
        w
   a    s    d

w/s : increase/decrease linear velocity
a/d : increase/decrease steering angle

space key, s : force stop

CTRL-C to quit
"""

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('keyboard_teleop')
    
    vel_pub = rospy.Publisher('/qcar/velocity_target', Float64, queue_size=10)
    steer_pub = rospy.Publisher('/qcar/steering_target', Float64, queue_size=10)
    
    speed = 0.2  # m/s
    angle = 0.5  # radians
    
    target_speed = 0
    target_angle = 0
    
    try:
        print(msg)
        while(1):
            key = getKey()
            
            if key == 'w':
                target_speed = speed
            elif key == 's':
                target_speed = -speed
            elif key == 'a':
                target_angle = angle
            elif key == 'd':
                target_angle = -angle
            elif key == ' ' or key == 's':
                target_speed = 0
                target_angle = 0
            
            if (key == '\x03'): # CTRL-C
                break

            vel_pub.publish(Float64(data=target_speed))
            steer_pub.publish(Float64(data=target_angle))

    except Exception as e:
        print(e)

    finally:
        vel_pub.publish(Float64(data=0))
        steer_pub.publish(Float64(data=0))
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
