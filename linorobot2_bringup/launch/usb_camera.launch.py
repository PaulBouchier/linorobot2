# Copyright (c) 2021 Juan Miguel Jimeno
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node


def generate_launch_description():
    usb_camera_config_path = PathJoinSubstitution(
        [FindPackageShare('linorobot2_bringup'), 'config', 'usb_camera.yaml']
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            name='video_device',
            default_value='/dev/video0',
            description='USB camera video device'
        ),

        DeclareLaunchArgument(
            name='namespace',
            default_value='usb_camera',
            description='Namespace/topic prefix for the camera feed'
        ),

        DeclareLaunchArgument(
            name='stream',
            default_value='true',
            description='Publish a downscaled, JPEG-compressed stream for slow networks'
        ),

        # Full-resolution capture for local use on the Pi.
        Node(
            package='usb_cam',
            executable='usb_cam_node_exe',
            name='usb_cam_node',
            namespace=LaunchConfiguration('namespace'),
            output='screen',
            parameters=[
                usb_camera_config_path,
                {'video_device': LaunchConfiguration('video_device')}
            ]
        ),

        # Downscale + JPEG-compress a light copy for streaming over slow links.
        # Output base topic 'downscaled/image_raw' carries the whole
        # image_transport family, so the network stream is
        # '<namespace>/downscaled/image_raw/compressed'.
        Node(
            condition=IfCondition(LaunchConfiguration('stream')),
            package='image_proc',
            executable='resize_node',
            name='resize_node',
            namespace=LaunchConfiguration('namespace'),
            output='screen',
            parameters=[usb_camera_config_path],
            remappings=[
                # image_proc's ResizeNode names its raw topics <base>/image_raw
                # and <base>/camera_info, so remap the full sub-topic names
                # (matching how the 'resize' output side is remapped below).
                ('image/image_raw', 'image_raw'),
                ('image/camera_info', 'camera_info'),
                ('resize/image_raw', 'downscaled/image_raw'),
                ('resize/camera_info', 'downscaled/camera_info'),
            ]
        )
    ])
