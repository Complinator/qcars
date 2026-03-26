from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
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

    overlay_topic_arg = DeclareLaunchArgument(
        'overlay_topic',
        default_value='/perception/object/overlay',
        description='Annotated object detection image topic',
    )

    show_viewer_arg = DeclareLaunchArgument(
        'show_viewer',
        default_value='true',
        description='If true, opens a live OpenCV window for object overlay',
    )

    return LaunchDescription([
        image_topic_arg,
        confidence_arg,
        overlay_topic_arg,
        show_viewer_arg,
        Node(
            package='my_qcar_nodes',
            executable='object_detection_node',
            name='object_detection_node',
            output='screen',
            parameters=[{
                'image_topic': LaunchConfiguration('image_topic'),
                'confidence_threshold': LaunchConfiguration('confidence_threshold'),
                'overlay_topic': LaunchConfiguration('overlay_topic'),
            }],
        ),
        Node(
            package='my_qcar_nodes',
            executable='camera_visualizer',
            name='object_overlay_viewer',
            output='screen',
            condition=IfCondition(LaunchConfiguration('show_viewer')),
            parameters=[{
                'image_topic': LaunchConfiguration('overlay_topic'),
            }],
        ),
    ])
