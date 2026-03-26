#!/usr/bin/env python3
import cv2

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from cv_bridge import CvBridge
from sensor_msgs.msg import Image


class PerceptionViewer(Node):
    def __init__(self):
        super().__init__('perception_viewer')

        self.declare_parameter('lane_overlay_topic', '/perception/lane/overlay')
        self.declare_parameter('object_overlay_topic', '/perception/object/overlay')

        lane_overlay_topic = self.get_parameter('lane_overlay_topic').value
        object_overlay_topic = self.get_parameter('object_overlay_topic').value

        self.bridge = CvBridge()
        self.lane_frame = None
        self.object_frame = None

        self.create_subscription(Image, lane_overlay_topic, self.lane_cb, qos_profile_sensor_data)
        self.create_subscription(Image, object_overlay_topic, self.object_cb, qos_profile_sensor_data)

        self.create_timer(0.03, self.render)

        self.get_logger().info(f'Viewing lane overlay: {lane_overlay_topic}')
        self.get_logger().info(f'Viewing object overlay: {object_overlay_topic}')

    def lane_cb(self, msg: Image) -> None:
        self.lane_frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

    def object_cb(self, msg: Image) -> None:
        self.object_frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

    def render(self) -> None:
        if self.lane_frame is not None:
            cv2.imshow('Lane Overlay', self.lane_frame)
        if self.object_frame is not None:
            cv2.imshow('Object Overlay', self.object_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = PerceptionViewer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
