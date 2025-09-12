cmake_minimum_required(VERSION 3.0.2)
project(my_qcar_nodes)
find_package(catkin REQUIRED COMPONENTS
  rospy std_msgs geometry_msgs sensor_msgs ackermann_msgs gazebo_msgs
)
catkin_package()
install(PROGRAMS
  scripts/move_cmd_vel.py
  scripts/move_ackermann.py
  scripts/print_joint_states.py
  scripts/print_model_states.py
  scripts/basic_move.py
  scripts/qcar_targets_bridge.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)