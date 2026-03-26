from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    image_topic_arg = DeclareLaunchArgument(
        'image_topic',
        default_value='/qcar/csi_front/image_raw',
        description='Input camera image topic',
    )

    confidence_arg = DeclareLaunchArgument(
        'confidence_threshold',
        default_value='0.45',
        description='Minimum detection confidence',
    )

    return LaunchDescription([
        image_topic_arg,
        confidence_arg,
        Node(
            package='my_qcar_nodes',
            executable='object_detection_node',
            name='object_detection_node',
            output='screen',
            parameters=[{
                'image_topic': LaunchConfiguration('image_topic'),
                'confidence_threshold': LaunchConfiguration('confidence_threshold'),
            }],
        ),
    ])
