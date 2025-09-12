# IMPORTANT
- PS1 file is intended to use on windows only, as this is the first push of this version I am not going to get into much details on how to set up for linux and MacOS, but it was already done, just not documented, so will be implemented in future work
- In order to run this you MUST have installed an [X Server](https://sourceforge.net/projects/xming/), otherwise, you will be able to open the docker container, but you won't see any app opening from it
- Note that `example.ps1` requires you to modify the path on the 2nd line to the path to your `config.xlaunch` file
- The app takes a while to run the gazebo model, so don't worry if it seems frozen
- The model used cames from an open-source repo called [autonomus-driving](https://github.com/bchampp/autonomous-driving)
- Remember to create the container using `docker build -t qcar-sim .` (use that code inside this folder)
- In order to run nodes you would need to run another terminal using `docker exec -it qcar bash`
- To start running a node/bridge use `rosrun my_qcar_nodes <node_name.py>` inside scripts folder (src/nodes/scripts/)
- To start running gazebo + rviz simulation use `roslaunch qcar_ngazebo qcar_world.launch` inside qcar_gazebo folder (src/qcar/src/qcar_gazebo/launch/)