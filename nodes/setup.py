from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'my_qcar_nodes'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='you',
    maintainer_email='you@example.com',
    description='Basic QCar demo nodes (cmd, sensors) - ROS 2 Migration',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'qcar_bridge = my_qcar_nodes.qcar_bridge:main',
            'basic_move = my_qcar_nodes.basic_move:main',
            'basic_read_joint = my_qcar_nodes.basic_read_joint:main',
            'basic_read_pose = my_qcar_nodes.basic_read_pose:main',
            'camera_visualizer = my_qcar_nodes.camera_visualizer:main',
            'lidar_visualizer = my_qcar_nodes.lidar_visualizer:main',
            'keyboard_teleop = my_qcar_nodes.keyboard_teleop:main',
            'lane_detection_node = my_qcar_nodes.lane_detection_node:main',
            'object_detection_node = my_qcar_nodes.object_detection_node:main',
            'lane_follower = my_qcar_nodes.lane_follower:main',
            'perception_viewer = my_qcar_nodes.perception_viewer:main',
        ],
    },
)
