#!/usr/bin/env python3
import json
import os
import urllib.request

import cv2

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import String


class ObjectDetectionNode(Node):
    CLASSES = [
        'background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle',
        'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog',
        'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa',
        'train', 'tvmonitor'
    ]

    def __init__(self):
        super().__init__('object_detection_node')

        self.declare_parameter('image_topic', '/qcar/csi_front/image_raw')
        self.declare_parameter('overlay_topic', '/perception/object/overlay')
        self.declare_parameter('detections_topic', '/perception/object/detections')
        self.declare_parameter('confidence_threshold', 0.45)
        self.declare_parameter('model_dir', '/tmp/mobilenet_ssd')
        self.declare_parameter('auto_download_model', True)

        self.image_topic = self.get_parameter('image_topic').value
        self.overlay_topic = self.get_parameter('overlay_topic').value
        self.detections_topic = self.get_parameter('detections_topic').value
        self.confidence_threshold = float(self.get_parameter('confidence_threshold').value)
        self.model_dir = self.get_parameter('model_dir').value
        self.auto_download_model = bool(self.get_parameter('auto_download_model').value)

        self.bridge = CvBridge()
        self.net = self._load_model()

        self.image_sub = self.create_subscription(
            Image,
            self.image_topic,
            self.image_callback,
            qos_profile_sensor_data,
        )

        self.overlay_pub = self.create_publisher(Image, self.overlay_topic, 10)
        self.detections_pub = self.create_publisher(String, self.detections_topic, 10)

        self.get_logger().info(f'Object detection subscribed to: {self.image_topic}')

    def _download_file(self, url: str, path: str) -> None:
        self.get_logger().info(f'Downloading model file: {url}')
        urllib.request.urlretrieve(url, path)

    def _load_model(self):
        os.makedirs(self.model_dir, exist_ok=True)

        prototxt = os.path.join(self.model_dir, 'deploy.prototxt')
        model = os.path.join(self.model_dir, 'mobilenet_iter_73000.caffemodel')

        if self.auto_download_model:
            if not os.path.isfile(prototxt):
                self._download_file(
                    'https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/deploy.prototxt',
                    prototxt,
                )
            if not os.path.isfile(model):
                self._download_file(
                    'https://github.com/chuanqi305/MobileNet-SSD/raw/master/mobilenet_iter_73000.caffemodel',
                    model,
                )

        if not os.path.isfile(prototxt) or not os.path.isfile(model):
            raise RuntimeError(
                'MobileNet-SSD model files are missing. Set auto_download_model:=true or provide files in model_dir.'
            )

        self.get_logger().info('Loading MobileNet-SSD model')
        return cv2.dnn.readNetFromCaffe(prototxt, model)

    def image_callback(self, msg: Image) -> None:
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        h, w = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)),
            scalefactor=0.007843,
            size=(300, 300),
            mean=127.5,
        )

        self.net.setInput(blob)
        detections = self.net.forward()

        results = []
        for i in range(detections.shape[2]):
            confidence = float(detections[0, 0, i, 2])
            if confidence < self.confidence_threshold:
                continue

            class_id = int(detections[0, 0, i, 1])
            if class_id < 0 or class_id >= len(self.CLASSES):
                continue

            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            xmin, ymin, xmax, ymax = box.astype('int').tolist()

            xmin = max(0, xmin)
            ymin = max(0, ymin)
            xmax = min(w - 1, xmax)
            ymax = min(h - 1, ymax)

            class_name = self.CLASSES[class_id]
            results.append({
                'class': class_name,
                'confidence': confidence,
                'xmin': xmin,
                'ymin': ymin,
                'xmax': xmax,
                'ymax': ymax,
            })

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 200, 255), 2)
            cv2.putText(
                frame,
                f'{class_name}: {confidence:.2f}',
                (xmin, max(0, ymin - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 200, 255),
                2,
                cv2.LINE_AA,
            )

        overlay_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        overlay_msg.header = msg.header
        self.overlay_pub.publish(overlay_msg)

        detections_msg = String()
        detections_msg.data = json.dumps(results)
        self.detections_pub.publish(detections_msg)


def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetectionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
