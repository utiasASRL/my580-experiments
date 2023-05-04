from launch import LaunchDescription
from launch_ros.actions import Node
import launch


def generate_launch_description():
    return LaunchDescription([
        launch.actions.ExecuteProcess(
          cmd=['ros2', 'bag', 'play', 'output/april-trial2'],
          output='screen'  
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments = ['0', '0', '0', '0', '0', '0', 'odom', 'vicon_object']
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments = ['0', '0', '1', '0', '0', '0', 'odom', 'zed2_left_camera_frame']
        ),
    ])
