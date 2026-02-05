from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_qcar_nodes',
            executable='qcar_bridge',
            name='qcar_targets_bridge',
            output='screen'
        ),
        Node(
            package='my_qcar_nodes',
            executable='basic_move',
            name='basic_move',
            output='screen',
            parameters=[
                {'velocity': 0.5},
                {'steering': 0.0}
            ]
        )
    ])
