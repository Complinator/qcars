#!/usr/bin/env python3
import cv2
import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import Float64, Float64MultiArray


class LaneDetectionNode(Node):
    def __init__(self):
        super().__init__('lane_detection_node')

        self.declare_parameter('image_topic', '/qcar/csi_front/image_raw')
        self.declare_parameter('overlay_topic', '/perception/lane/overlay')
        self.declare_parameter('center_offset_topic', '/planning/center_offset')
        self.declare_parameter('waypoints_topic', '/planning/waypoints')

        image_topic = self.get_parameter('image_topic').value
        overlay_topic = self.get_parameter('overlay_topic').value
        center_offset_topic = self.get_parameter('center_offset_topic').value
        waypoints_topic = self.get_parameter('waypoints_topic').value

        self.bridge = CvBridge()

        self.image_sub = self.create_subscription(
            Image,
            image_topic,
            self.image_callback,
            qos_profile_sensor_data,
        )

        self.overlay_pub = self.create_publisher(Image, overlay_topic, 10)
        self.center_offset_pub = self.create_publisher(Float64, center_offset_topic, 10)
        self.waypoints_pub = self.create_publisher(Float64MultiArray, waypoints_topic, 10)

        self.get_logger().info(f'Lane detection subscribed to: {image_topic}')

    def image_callback(self, msg: Image) -> None:
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        overlay, center_offset_px, waypoints = self.detect_lanes(frame)

        overlay_msg = self.bridge.cv2_to_imgmsg(overlay, encoding='bgr8')
        overlay_msg.header = msg.header
        self.overlay_pub.publish(overlay_msg)

        self.center_offset_pub.publish(Float64(data=float(center_offset_px)))

        waypoints_msg = Float64MultiArray()
        waypoints_msg.data = [float(v) for xy in waypoints for v in xy]
        self.waypoints_pub.publish(waypoints_msg)

    def detect_lanes(self, frame: np.ndarray):
        h, w = frame.shape[:2]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        white_mask = cv2.inRange(hsv, np.array([0, 0, 180]), np.array([180, 40, 255]))
        yellow_mask = cv2.inRange(hsv, np.array([15, 80, 80]), np.array([40, 255, 255]))
        mask = cv2.bitwise_or(white_mask, yellow_mask)

        edges = cv2.Canny(mask, 60, 150)

        roi = np.zeros_like(edges)
        polygon = np.array([
            [
                (int(0.05 * w), h),
                (int(0.42 * w), int(0.62 * h)),
                (int(0.58 * w), int(0.62 * h)),
                (int(0.95 * w), h),
            ]
        ], dtype=np.int32)
        cv2.fillPoly(roi, polygon, 255)
        cropped = cv2.bitwise_and(edges, roi)

        lines = cv2.HoughLinesP(
            cropped,
            rho=1,
            theta=np.pi / 180,
            threshold=30,
            minLineLength=30,
            maxLineGap=120,
        )

        left_points = []
        right_points = []

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if x2 == x1:
                    continue
                slope = (y2 - y1) / (x2 - x1)
                if abs(slope) < 0.4:
                    continue
                if slope < 0:
                    left_points.extend([(x1, y1), (x2, y2)])
                else:
                    right_points.extend([(x1, y1), (x2, y2)])

        overlay = frame.copy()
        y_bottom = h - 1
        y_top = int(0.62 * h)

        left_x_bottom, left_x_top = None, None
        right_x_bottom, right_x_top = None, None

        if len(left_points) >= 4:
            lx, ly = zip(*left_points)
            left_fit = np.polyfit(ly, lx, 1)
            left_x_bottom = int(np.polyval(left_fit, y_bottom))
            left_x_top = int(np.polyval(left_fit, y_top))
            cv2.line(overlay, (left_x_bottom, y_bottom), (left_x_top, y_top), (0, 255, 0), 4)

        if len(right_points) >= 4:
            rx, ry = zip(*right_points)
            right_fit = np.polyfit(ry, rx, 1)
            right_x_bottom = int(np.polyval(right_fit, y_bottom))
            right_x_top = int(np.polyval(right_fit, y_top))
            cv2.line(overlay, (right_x_bottom, y_bottom), (right_x_top, y_top), (0, 255, 0), 4)

        waypoints = []
        center_offset_px = 0.0

        if left_x_bottom is not None and right_x_bottom is not None:
            lane_center_bottom = 0.5 * (left_x_bottom + right_x_bottom)
            lane_center_top = 0.5 * (left_x_top + right_x_top)

            cv2.line(
                overlay,
                (int(lane_center_bottom), y_bottom),
                (int(lane_center_top), y_top),
                (255, 0, 0),
                3,
            )

            image_center = w / 2.0
            center_offset_px = image_center - lane_center_bottom

            ys = np.linspace(y_bottom, y_top, num=15)
            for y in ys:
                alpha = (y_bottom - y) / max((y_bottom - y_top), 1)
                x = lane_center_bottom * (1.0 - alpha) + lane_center_top * alpha
                waypoints.append((x, y))

            cv2.putText(
                overlay,
                f'Center offset(px): {center_offset_px:.1f}',
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (50, 220, 255),
                2,
                cv2.LINE_AA,
            )
        else:
            cv2.putText(
                overlay,
                'Lane not confidently detected',
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

        return overlay, center_offset_px, waypoints


def main(args=None):
    rclpy.init(args=args)
    node = LaneDetectionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
