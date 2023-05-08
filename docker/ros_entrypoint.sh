#!/bin/bash

# Source ROS and Catkin workspaces
for FNAME in "/opt/ros/${ROS_DISTRO}/setup.bash" "/home/ros/my580_ros2_ws/workspace/install/local_setup.bash"
do
  if [ -f "${FNAME}" ]
  then 
    source "${FNAME}"
    echo "success: source ${FNAME}"
  else
    echo "Note: could not source ${FNAME}"
  fi
done 

# Execute the command passed into this entrypoint
exec "$@"
