from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    image_topic_arg = DeclareLaunchArgument(
        'image_topic',
        default_value='/qcar/csi_front/image_raw',
        description='Input camera image topic for perception',
    )

    confidence_arg = DeclareLaunchArgument(
        'confidence_threshold',
        default_value='0.45',
        description='Minimum detection confidence for object detector',
    )

    base_velocity_arg = DeclareLaunchArgument(
        'base_velocity',
        default_value='0.55',
        description='Forward velocity for line follower',
    )

    return LaunchDescription([
        image_topic_arg,
        confidence_arg,
        base_velocity_arg,
        Node(
            package='my_qcar_nodes',
            executable='qcar_bridge',
            name='qcar_targets_bridge',
            output='screen',
        ),
        Node(
            package='my_qcar_nodes',
            executable='lane_detection_node',
            name='lane_detection_node',
            output='screen',
            parameters=[{
                'image_topic': LaunchConfiguration('image_topic'),
            }],
        ),
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
        Node(
            package='my_qcar_nodes',
            executable='lane_follower',
            name='lane_follower',
            output='screen',
            parameters=[{
                'base_velocity': LaunchConfiguration('base_velocity'),
            }],
        ),
        Node(
            package='my_qcar_nodes',
            executable='perception_viewer',
            name='perception_viewer',
            output='screen',
        ),
    ])
