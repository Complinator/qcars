cmake_minimum_required(VERSION 3.5)
project(qcar_gazebo)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch models meshes rviz worlds urdf
  DESTINATION share/${PROJECT_NAME}
)

ament_export_dependencies(gazebo_ros)

ament_package()
