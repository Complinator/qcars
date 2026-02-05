cmake_minimum_required(VERSION 3.5)
project(qcar_interface)

find_package(ament_cmake REQUIRED)

install(FILES cameras.yaml cameras_simulation.yaml
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
