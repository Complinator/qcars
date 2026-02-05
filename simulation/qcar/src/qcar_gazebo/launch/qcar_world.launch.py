import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler, DeclareLaunchArgument
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    qcar_gazebo = get_package_share_directory('qcar_gazebo')
    qcar_control = get_package_share_directory('qcar_control')
    
    # Launch Args
    x_arg = DeclareLaunchArgument('x', default_value='0.5')
    y_arg = DeclareLaunchArgument('y', default_value='-0.4')
    z_arg = DeclareLaunchArgument('z', default_value='0.1')
    roll_arg = DeclareLaunchArgument('roll', default_value='0.0')
    pitch_arg = DeclareLaunchArgument('pitch', default_value='0.0')
    yaw_arg = DeclareLaunchArgument('yaw', default_value='0.5')

    # Convert Xacro
    xacro_file = os.path.join(qcar_gazebo, 'urdf', 'qcar_model.xacro')
    robot_description_doc = xacro.process_file(xacro_file)
    robot_description = {'robot_description': robot_description_doc.toxml()}

    # Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ]),
        launch_arguments={'verbose': 'true', 'world': os.path.join(qcar_gazebo, 'worlds', 'qcar.world')}.items()
    )

    # Spawn Entity
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'qcar',
                                   '-x', LaunchConfiguration('x'),
                                   '-y', LaunchConfiguration('y'),
                                   '-z', LaunchConfiguration('z'),
                                   '-R', LaunchConfiguration('roll'),
                                   '-P', LaunchConfiguration('pitch'),
                                   '-Y', LaunchConfiguration('yaw')],
                        output='screen')

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )
    
    # Joint State Broadcaster
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    # Spawners
    rr_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["rr_controller", "--controller-manager", "/controller_manager"],
    )
    rl_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["rl_controller", "--controller-manager", "/controller_manager"],
    )
    fr_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["base_fr_controller", "--controller-manager", "/controller_manager"],
    )
    fl_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["base_fl_controller", "--controller-manager", "/controller_manager"],
    )

    return LaunchDescription([
        x_arg, y_arg, z_arg, roll_arg, pitch_arg, yaw_arg,
        gazebo,
        robot_state_publisher,
        spawn_entity,
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=spawn_entity,
                on_exit=[
                    joint_state_broadcaster_spawner,
                    rr_spawner,
                    rl_spawner,
                    fr_spawner,
                    fl_spawner
                ],
            )
        ),
    ])
