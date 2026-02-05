#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
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

settings = None

def main(args=None):
    global settings
    settings = termios.tcgetattr(sys.stdin)
    
    rclpy.init(args=args)
    node = Node('keyboard_teleop')
    
    vel_pub = node.create_publisher(Float64, '/qcar/velocity_target', 10)
    steer_pub = node.create_publisher(Float64, '/qcar/steering_target', 10)
    
    speed = 0.2  # m/s
    angle = 0.5  # radians
    
    target_speed = 0.0
    target_angle = 0.0
    
    try:
        print(msg)
        while rclpy.ok():
            key = getKey()
            
            if key == 'w':
                target_speed = speed
            elif key == 's':
                target_speed = -speed
            elif key == 'a':
                target_angle = angle
            elif key == 'd':
                target_angle = -angle
            elif key == ' ' or key == 'x': # 's' used for backward in original but prompt says 's' stops? Original code: 's' -> bw, ' ' or 's' -> stop. Conflict?
                # Original code:
                # elif key == 's': target_speed = -speed
                # elif key == ' ' or key == 's': target_speed = 0 ...
                # Wait, if key is 's', it hits the first elif. The second elif for 's' is unreachable/shadowed.
                # I will fix this logic. "space key, s : force stop" in text, but code used 's' for backward.
                # Assuming 'x' or space for stop is safer. But following original behavior: 's' goes backward.
                target_speed = 0.0
                target_angle = 0.0
            
            # Let's check original code behavior for 's'.
            # Original:
            # if key == 'w': ...
            # elif key == 's': target_speed = -speed
            # ...
            # elif key == ' ' or key == 's': target_speed = 0
            #
            # If key is 's', it enters the first elif block and skips the rest. So it goes backward.
            # The help text says "space key, s : force stop". This is contradictory.
            # I will preserve the code behavior (backward) and add 'x' for stop.
            
            if key == '\x03': # CTRL-C
                break

            vel_pub.publish(Float64(data=float(target_speed)))
            steer_pub.publish(Float64(data=float(target_angle)))

    except Exception as e:
        print(e)

    finally:
        vel_pub.publish(Float64(data=0.0))
        steer_pub.publish(Float64(data=0.0))
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
