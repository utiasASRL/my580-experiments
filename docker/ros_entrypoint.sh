#!/bin/bash

# Source ROS and Catkin workspaces
source "/opt/ros/${ROS_DISTRO}/setup.bash"
echo "success: source /opt/ros/${ROS_DISTRO}/setup.bash"

if [ -f "${ROS2_WS}/install/local_setup.bash" ]
then
  source "${ROS2_WS}/install/local_setup.bash"
  echo "success: source ${ROS2_WS}/install/local_setup.bash"
else
  echo "Note: ${ROS2_WS}/install/local_setup.bash does not exist yet."
fi

# Execute the command passed into this entrypoint
exec "$@"
