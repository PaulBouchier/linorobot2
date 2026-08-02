## Manual installation of linorobot2 package on robot computer

> **Note:** For most users, the automated installer is the recommended approach instead of following this guide manually:
>
>     source /opt/ros/<ros_distro>/setup.bash
>     cd /tmp
>     wget https://raw.githubusercontent.com/linorobot/linorobot2/${ROS_DISTRO}/install.bash
>     bash install.bash --base <robot_type> [--laser <laser_sensor>] [--depth <depth_sensor>]
>     source ~/.bashrc
>
> Follow the steps below only if you need a custom installation.

### 1. Install micro-ROS and its dependencies

#### 1.1 Source your ROS2 distro and workspace
If it's your first time using ROS2 and haven't created your ROS2 workspace yet, you can check out [ROS2 Creating a Workspace](https://docs.ros.org/en/jazzy/Tutorials/Workspace/Creating-A-Workspace.html) tutorial.

    source /opt/ros/<your_ros_distro>/setup.bash
    cd <your_ws>
    colcon build
    source install/setup.bash

#### 1.2 Install LIDAR ROS2 drivers:
YDLIDAR:

    cd /tmp
    git clone https://github.com/YDLIDAR/YDLidar-SDK.git
    cd YDLidar-SDK/build
    cmake ..
    make
    sudo make install
    cd <your_ws>
    git clone https://github.com/YDLIDAR/ydlidar_ros2_driver src/ydlidar_ros2_driver
    chmod 0777 src/ydlidar_ros2_driver/startup/*
    sudo sh src/ydlidar_ros2_driver/startup/initenv.sh
    colcon build --symlink-install
    source <your_ws>/install/setup.bash

XV11:
    
    cd <your_ws>
    git clone https://github.com/mjstn/xv_11_driver src/xv_11_driver
    colcon build
    source <your_ws>/install/setup.bash

LD06 LD19 STL27L:

    cd <your_ws>
    git clone https://github.com/hippo5329/ldlidar_stl_ros2.git src/ldlidar_stl_ros2
    colcon build
    source <your_ws>/install/setup.bash
    cd /tmp
    wget https://raw.githubusercontent.com/linorobot/ldlidar/ros2/ldlidar.rules
    sudo cp ldlidar.rules /etc/udev/rules.d

RPLIDAR (A1 A2 A3 C1 S1 S2 S3):

    cd <your_ws>
    git clone https://github.com/Slamtec/sllidar_ros2.git
    colcon build
    source  <your_ws>/install/setup.bash
    sudo cp sllidar_ros2/scripts/rplidar.rules /etc/udev/rules.d

#### 1.3 Install depth sensor drivers:
Intel RealSense:

    sudo apt install ros-$ROS_DISTRO-realsense2-camera

Zed Camera:

    cd /tmp
    wget https://download.stereolabs.com/zedsdk/3.5/jp45/jetsons -O zed_sdk #use Jetson SDK
    #wget https://download.stereolabs.com/zedsdk/3.5/cu111/ubuntu20 -O zed_sdk #use this for x86 machine with NVIDIA GPU
    chmod +x zed_sdk
    ./zed_sdk -- silent
    cd <your_ws>
    git clone https://github.com/stereolabs/zed-ros2-wrapper src/zed-ros2-wrapper
    git clone https://github.com/ros-perception/image_common -b $ROS_DISTRO src/image_common
    rosdep install --from-paths src --ignore-src -r -y
    colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release
    source <your_ws>/install/setup.bash

OAK-D Camera:

    sudo apt install ros-$ROS_DISTRO-depthai-ros
    
#### 1.4 Download and install micro-ROS:

    cd <your_ws>
    git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup src/micro_ros_setup
    sudo apt install python3-vcstool build-essential
    sudo apt update && rosdep update
    rosdep install --from-path src --ignore-src -y
    colcon build
    source install/setup.bash

#### 1.5 Setup micro-ROS agent:

    ros2 run micro_ros_setup create_agent_ws.sh
    ros2 run micro_ros_setup build_agent.sh
    source install/setup.bash

* You can ignore `1 package had stderr output: microxrcedds_agent` after building your workspace. 

### 2. Download linorobot2 and its dependencies:

#### 2.1 Download linorobot2:

    cd <your_ws> 
    git clone -b $ROS_DISTRO https://github.com/linorobot/linorobot2 src/linorobot2

#### 2.2 Ignore Gazebo Packages on robot computer (optional)

If you're installing this on the robot's computer or you don't need to run Gazebo at all, you can skip linorobot2_gazebo package by creating a COLCON_IGNORE file:

    cd src/linorobot2/linorobot2_gazebo
    touch COLCON_IGNORE

#### 2.3 Install linorobot2 package:
    
    cd <your_ws>
    rosdep update && rosdep install --from-path src --ignore-src -y --skip-keys microxrcedds_agent
    colcon build
    source install/setup.bash

* microxrcedds_agent dependency checks are skipped to prevent this [issue](https://github.com/micro-ROS/micro_ros_setup/issues/138) of finding its keys. This means that you have to always add `--skip-keys microxrcedds_agent` whenever you have to run `rosdep install` on the ROS2 workspace where you installed linorobot2.

## ENV Variables
### 1. Robot Type
Set LINOROBOT2_BASE env variable to the type of robot base that you want to use. This is not required if you're using a custom URDF. Available env variables are *2wd*, *4wd*, and *mecanum*. For example:

    echo "export LINOROBOT2_BASE=2wd" >> ~/.bashrc

### 2. Sensors
#### 2.1 Depth Sensor (Optional)
The Nav2 config file has been configured to support [Voxel Layer](https://navigation.ros.org/configuration/packages/costmap-plugins/voxel.html) for marking 3D obstacles in the Local Costmap using a depth sensor. To enable one of the tested depth sensor's launch files in bringup.launch.py, export the depth sensor you're using to `LINOROBOT2_DEPTH_SENSOR` env variable.

Tested sensors are:
- `realsense` - [Intel RealSense](https://www.intelrealsense.com/stereo-depth/) D435, D435i
- `astra` - [Orbec Astra](https://orbbec3d.com/product-astra-pro/)
- `zed` - [Zed](https://www.stereolabs.com/zed)
- `zed2` - [Zed 2](https://www.stereolabs.com/zed-2)
- `zed2i` - [Zed 2i](https://www.stereolabs.com/zed-2i)
- `zedm` - [Zed Mini](https://www.stereolabs.com/zed-mini)

For example:

    echo "export LINOROBOT2_DEPTH_SENSOR=realsense" >> ~/.bashrc

#### 2.2 Laser Sensor (Optional)
The launch files of the tested laser sensors have already been added in bringup.launch.py. You can enable one of these sensors by exporting the laser sensor you're using to `LINOROBOT2_LASER_SENSOR` env variable.

Tested Laser Sensors:
- `rplidar` - [RP LIDAR A1](https://www.slamtec.com/en/Lidar/A1)
- `ldlidar` - [LD06 LIDAR](https://www.inno-maker.com/product/lidar-ld06/)
- `ld06` - [LD06 LIDAR](https://www.ldrobot.com/ProductDetails?sensor_name=STL-06P)
- `ld19` - [LD19/LD300 LIDAR](https://www.ldrobot.com/ProductDetails?sensor_name=STL-19P)
- `stl27l` - [STL27L LIDAR](https://www.ldrobot.com/ProductDetails?sensor_name=STL-27L)
- `ydlidar` - [YDLIDAR](https://www.ydlidar.com/lidars.html)
- `realsense` - [Intel RealSense](https://www.intelrealsense.com/stereo-depth/) D435, D435i
- `astra` - [Orbec Astra](https://orbbec3d.com/product-astra-pro/)
- `zed` - [Zed](https://www.stereolabs.com/zed)
- `zed2` - [Zed 2](https://www.stereolabs.com/zed-2)
- `zed2i` - [Zed 2i](https://www.stereolabs.com/zed-2i)
- `zedm` - [Zed Mini](https://www.stereolabs.com/zed-mini)

For example:

    echo "export LINOROBOT2_LASER_SENSOR=rplidar" >> ~/.bashrc

If you export a depth sensor to `LINOROBOT2_LASER_SENSOR`, the launch file will run [depthimage_to_laserscan](https://github.com/ros-perception/depthimage_to_laserscan) to convert the depth sensor's depth image to laser.

#### 2.3 USB Camera (Optional)
A plain UVC USB camera (e.g. a webcam plugged into the Raspberry Pi) can be enabled by exporting its video device to the `LINOROBOT2_USB_CAMERA` env variable. This runs the [usb_cam](https://github.com/ros-drivers/usb_cam) driver as part of bringup.

    echo "export LINOROBOT2_USB_CAMERA=/dev/video0" >> ~/.bashrc

Two pipelines run on the Pi:

- **Full resolution, for local use.** `usb_cam` captures at full resolution/framerate (default 640x480 @ 30 fps) and publishes `/usb_camera/image_raw` (with `/usb_camera/camera_info`). Use this on the Pi itself where bandwidth is free.
- **Light, for slow networks.** An `image_proc` resize node downscales that feed (default 320x240) and `image_transport` auto-compresses it to JPEG on `/usb_camera/downscaled/image_raw/compressed`. This is what you subscribe to from a remote machine.

Do **not** subscribe to `/usb_camera/image_raw` over the network — raw video will saturate a slow link. Use the compressed downscaled stream from the remote machine, e.g.:

    ros2 run rqt_image_view rqt_image_view
    # pick the BASE topic /usb_camera/downscaled/image_raw, then set the
    # transport dropdown to "compressed"

Pick the **base** topic (`/usb_camera/downscaled/image_raw`) and let the transport dropdown select `compressed`. Do **not** select the `/compressed` sub-topic directly and do **not** also pass `_image_transport:=compressed` — doing both makes rqt_image_view subscribe to the compressed topic with the wrong message type and it crashes (`invalid allocator` / `incompatible type CompressedImage`).

If rqt_image_view is still flaky, the most reliable option is to decompress the stream to a plain raw topic once and view that (rqt then never touches compressed transport):

    # terminal 1 — decompress to a raw topic
    ros2 run image_transport republish compressed raw \
        --ros-args -r in/compressed:=/usb_camera/downscaled/image_raw/compressed \
                   -r out:=/usb_camera/view

    # terminal 2 — view the plain raw topic
    ros2 run rqt_image_view rqt_image_view /usb_camera/view

The network stream is on by default. If you only need the full-resolution local feed (and want to save CPU on the Pi), disable it:

    echo "export LINOROBOT2_USB_CAMERA_STREAM=false" >> ~/.bashrc

Tuning knobs in `linorobot2_bringup/config/usb_camera.yaml`:

- Full-res capture: `image_width`/`image_height`/`framerate` under `usb_cam_node`.
- Network stream size: `width`/`height` under `resize_node`.
- Network stream quality: `.downscaled.image_raw.compressed.jpeg_quality` (1-100; lower = smaller frames).

The camera is part of the mowberry robot's TF tree. The URDF adds a `usb_camera_link` (physical mount, positioned by `usb_camera_pose` in `mowberry_properties.urdf.xacro`) and a `usb_camera_optical_link` child that follows the REP-103 optical convention. The driver stamps images with `usb_camera_optical_link` (`frame_id` in `usb_camera.yaml`), so images/point clouds project correctly in RViz and perception. Adjust the mounting position by editing `usb_camera_pose`.

These frames are published by `robot_state_publisher`, **not** by the camera launch. The standalone `usb_camera.launch.py` only starts the camera driver — it does not publish TF. To get the camera TF you must run something that loads the URDF, with `LINOROBOT2_BASE=mowberry` set so the mowberry model (the one containing the camera links) is used:

    # full robot (starts robot_state_publisher via description.launch.py):
    LINOROBOT2_BASE=mowberry ros2 launch linorobot2_bringup bringup.launch.py base_serial_port:=/dev/ttyUSB0

    # or, TF only without the motor board:
    LINOROBOT2_BASE=mowberry ros2 launch linorobot2_description description.launch.py

If `ros2 run tf2_ros tf2_echo base_link usb_camera_optical_link` reports no transform, check that `robot_state_publisher` is running and that the loaded URDF actually contains the camera (i.e. `LINOROBOT2_BASE` was `mowberry` at launch):

    ros2 node list | grep robot_state_publisher
    ros2 param get /robot_state_publisher robot_description | grep -c usb_camera   # should be > 0

##### Building and testing the USB camera

After pulling the code, install the new dependencies (`usb_cam`, `image_proc`, `image_transport_plugins`) and rebuild:

    cd <your_ws>
    rosdep update && rosdep install --from-path src --ignore-src -y --skip-keys microxrcedds_agent
    colcon build
    source install/setup.bash

If `rosdep` doesn't resolve them, install directly:

    sudo apt install ros-$ROS_DISTRO-usb-cam ros-$ROS_DISTRO-image-proc ros-$ROS_DISTRO-image-transport-plugins

Plug in the camera and confirm the device node, then make sure your user can open it (one time; log out/in or reboot after):

    ls /dev/video*
    sudo usermod -aG video $USER

To identify which `/dev/video*` node is the USB camera (a UVC cam usually exposes several):

    sudo apt install v4l-utils
    v4l2-ctl --list-devices

Set the env variable and launch the camera standalone to test in isolation (or launch the full robot, which brings it up automatically):

    export LINOROBOT2_USB_CAMERA=/dev/video0
    ros2 launch linorobot2_bringup usb_camera.launch.py video_device:=/dev/video0

In another terminal, verify both feeds publish at a steady rate (~30 Hz):

    ros2 topic list | grep usb_camera
    ros2 topic hz /usb_camera/image_raw
    ros2 topic hz /usb_camera/downscaled/image_raw/compressed

Confirm the resize node subscribes to the right inputs (it should list `/usb_camera/image_raw` and `/usb_camera/camera_info`):

    ros2 node info /usb_camera/resize_node

View the light stream from a remote machine on the same ROS network (matching `ROS_DOMAIN_ID`):

    ros2 run rqt_image_view rqt_image_view
    # pick the BASE topic /usb_camera/downscaled/image_raw and set transport to
    # "compressed" (hit refresh if the dropdown is empty). Don't select the
    # /compressed sub-topic directly — see the viewing notes above if it crashes.

Finally, check the camera frame is in TF. This needs `robot_state_publisher` running with the mowberry model — the camera launch alone does not publish TF (see the TF note above):

    LINOROBOT2_BASE=mowberry ros2 launch linorobot2_description description.launch.py
    # then, in another terminal:
    ros2 run tf2_ros tf2_echo base_link usb_camera_optical_link

### 3. Save changes
Source your `~/.bashrc` to apply the changes you made:

    source ~/.bashrc

## Miscellaneous

### 1. Creating Jetson Nano Image 

- Create the custom image on your host machine by following this [tutorial](https://pythops.com/post/create-your-own-image-for-jetson-nano-board.html). Prepare an SD card and use the helper scripts found in the [repository](https://github.com/pythops/jetson-nano-image) mentioned in the tutorial to build and flash the custom image to the SD card.

- Before going through the tutorial, you can change the user name and password by modifying this [file](https://github.com/pythops/jetson-nano-image/blob/master/ansible/roles/jetson/defaults/main.yaml#L5-L7).

- If you encounter this problem: `Extend the fs... e2fsck: No such file or directory while trying to open /dev/sdcp1
` after flashing the image, you can check out this [issue](https://github.com/pythops/jetson-nano-image/issues/43) to resolve the problem.

- On your jetson nano, install the Nvidia Libraries:

    sudo apt install -y cuda-toolkit-10-2 libcudnn8 libcudnn8-dev

### 2. Running a launch file during boot-up.

This is a short tutorial on how to make your bringup launch files run during startup.

### 2.1 Create your env.sh

    sudo touch /etc/ros/env.sh
    sudo nano /etc/ros/env.sh 

and paste the following:

    #!/bin/sh

    export LINOROBOT2_BASE=<your_robot_type>
    export LINOROBOT2_LASER_SENSOR=<your_supported_sensor> #(optional)

### 2.2 Create systemd service

    sudo touch /etc/systemd/system/robot-boot.service
    sudo nano  /etc/systemd/system/robot-boot.service

and paste the following:

    [Unit]
    After=NetworkManager.service time-sync.target

    [Service]
    Type=simple
    User=<user>
    ExecStart=/bin/sh -c ". /opt/ros/<your_ros_distro>/setup.sh;. /etc/ros/env.sh;. /home/<user>/<your_ws>/install/setup.sh; ros2 launch linorobot2_bringup bringup.launch.py joy:=true"

    [Install]
    WantedBy=multi-user.target

Remember to replace:
- `user` with your machine's user name (`echo $USER`)
- `your_ros_distro` with the ros2 distro (`echo $ROS_DISTRO`) your machine is running on
- `your_ws` with the location of the ros2 ws where you installed linorobot2

### 2.3 Enable the service

    sudo systemctl enable robot-boot.service

You can check if the service you just created is correct by:

    sudo systemctl start robot-boot.service
    sudo systemctl status robot-boot.service

* You should see the ros2 logs that you usually see when running bringup.launch.py. Once successful, you can now reboot your machine. bringup.launch.py should start running once the machine finished booting up.

### 2.4 Removing the service

    systemctl stop robot-boot.service
    systemctl disable robot-boot.service
    sudo rm /etc/systemd/system/robot-boot.service


Source: https://blog.roverrobotics.com/how-to-run-ros-on-startup-bootup/
