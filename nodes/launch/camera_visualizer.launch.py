from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_qcar_nodes',
            executable='camera_visualizer',
            name='camera_visualizer',
            output='screen',
            parameters=[
                # Default to CSI Front camera found in logs: /qcar/csi_front/image_raw
                # Alternative: /camera/cameracolor/image_raw (RealSense)
                {'image_topic': '/qcar/csi_front/image_raw'}
            ]
        )
    ])
