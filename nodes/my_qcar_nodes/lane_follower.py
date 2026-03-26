#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool, Float64


class LaneFollower(Node):
    def __init__(self):
        super().__init__('lane_follower')

        self.declare_parameter('center_offset_topic', '/planning/center_offset')
        self.declare_parameter('lane_detected_topic', '/planning/lane_detected')
        self.declare_parameter('velocity_topic', '/qcar/velocity_target')
        self.declare_parameter('steering_topic', '/qcar/steering_target')

        self.declare_parameter('kp', 0.0045)
        self.declare_parameter('kd', 0.0015)
        self.declare_parameter('max_steering', 0.45)
        self.declare_parameter('base_velocity', 0.55)
        self.declare_parameter('slow_velocity', 0.30)
        self.declare_parameter('deadband_px', 8.0)
        self.declare_parameter('lane_timeout_sec', 0.6)

        center_offset_topic = self.get_parameter('center_offset_topic').value
        lane_detected_topic = self.get_parameter('lane_detected_topic').value
        velocity_topic = self.get_parameter('velocity_topic').value
        steering_topic = self.get_parameter('steering_topic').value

        self.kp = float(self.get_parameter('kp').value)
        self.kd = float(self.get_parameter('kd').value)
        self.max_steering = float(self.get_parameter('max_steering').value)
        self.base_velocity = float(self.get_parameter('base_velocity').value)
        self.slow_velocity = float(self.get_parameter('slow_velocity').value)
        self.deadband_px = float(self.get_parameter('deadband_px').value)
        self.lane_timeout_sec = float(self.get_parameter('lane_timeout_sec').value)

        self.center_offset_px = 0.0
        self.last_offset_px = 0.0
        self.lane_detected = False
        self.last_lane_time = self.get_clock().now()

        self.create_subscription(Float64, center_offset_topic, self.offset_callback, 10)
        self.create_subscription(Bool, lane_detected_topic, self.detected_callback, 10)

        self.velocity_pub = self.create_publisher(Float64, velocity_topic, 10)
        self.steering_pub = self.create_publisher(Float64, steering_topic, 10)

        self.dt = 0.05
        self.create_timer(self.dt, self.control_loop)

        self.get_logger().info('Lane follower started')

    def offset_callback(self, msg: Float64) -> None:
        self.center_offset_px = float(msg.data)

    def detected_callback(self, msg: Bool) -> None:
        self.lane_detected = bool(msg.data)
        if self.lane_detected:
            self.last_lane_time = self.get_clock().now()

    def lane_is_recent(self) -> bool:
        elapsed = (self.get_clock().now() - self.last_lane_time).nanoseconds / 1e9
        return self.lane_detected and elapsed <= self.lane_timeout_sec

    def control_loop(self) -> None:
        if not self.lane_is_recent():
            self.velocity_pub.publish(Float64(data=0.0))
            self.steering_pub.publish(Float64(data=0.0))
            return

        error = self.center_offset_px
        if abs(error) < self.deadband_px:
            error = 0.0

        derivative = (error - self.last_offset_px) / self.dt
        self.last_offset_px = error

        steering_cmd = self.kp * error + self.kd * derivative
        steering_cmd = max(-self.max_steering, min(self.max_steering, steering_cmd))

        velocity_cmd = self.base_velocity if abs(steering_cmd) < 0.22 else self.slow_velocity

        self.velocity_pub.publish(Float64(data=velocity_cmd))
        self.steering_pub.publish(Float64(data=steering_cmd))


def main(args=None):
    rclpy.init(args=args)
    node = LaneFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
