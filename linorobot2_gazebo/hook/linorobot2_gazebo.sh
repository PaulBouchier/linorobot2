# Prepend the models directory to GZ_SIM_RESOURCE_PATH
# This allows Gazebo Sim (Harmonic) to find models in the linorobot2_gazebo/models directory
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:$AMENT_CURRENT_PREFIX/share/linorobot2_gazebo/models
export IGN_GAZEBO_RESOURCE_PATH=$IGN_GAZEBO_RESOURCE_PATH:$AMENT_CURRENT_PREFIX/share/linorobot2_gazebo/models
