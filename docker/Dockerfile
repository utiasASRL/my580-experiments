# adapted from https://www.stereolabs.com/docs/docker/configure-ros-dockerfile/
FROM stereolabs/zed:3.8-gl-devel-cuda11.4-ubuntu20.04

ENV LOGNAME root
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV ROS_DISTRO "foxy"
ENV ROS2_WS "/home/ros/my580_ros2_ws"

RUN apt-get update || true && apt-get install -q -y --no-install-recommends \
    bash-completion \
    dirmngr \
    gnupg2 \
    lsb-release \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN echo "deb http://packages.ros.org/ros2/ubuntu focal main" > /etc/apt/sources.list.d/ros2-latest.list && \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    git \
    python3-colcon-common-extensions \
    python3-colcon-mixin \
    python3-rosdep \
    python3-vcstool \
    ros-foxy-desktop \
    && rm -rf /var/lib/apt/lists/*

RUN rosdep init \
    && rosdep update

# Install the zed-ros2 code.
# IMPORTANT: 
# - we need to check out the foxy version because that's what the zed2 docker file is built on 
#   (Ubuntu 20).
# - however, we still need certain libraries that are only created at runtime with the 
#   correct CUDA bindings (see commented below), which is why we need the Makefile command
#   make build-zed2_ros2
SHELL ["/bin/bash", "-c"] # change default from /bin/sh to /bin/bash
RUN sudo apt update && source /opt/ros/foxy/setup.bash \
  && mkdir -p "${ROS2_WS}/src" \
  && cd "${ROS2_WS}/src" \
  && git clone --recursive https://github.com/stereolabs/zed-ros2-wrapper.git \
  && git clone --recursive https://github.com/christianrauch/apriltag_msgs.git \
  && git clone --recursive https://github.com/christianrauch/apriltag_ros.git \
  && cd zed-ros2-wrapper \
  && git checkout foxy-humble-v3.8.2 \
  && cd ../.. \
  && rosdep install --from-paths src --ignore-src -r -y  \
  && cd "${ROS2_WS}/src" \
  && git clone --recursive https://github.com/utiasASRL/ros2-vicon-receiver.git \
  && cd ros2-vicon-receiver \
  && ./install_libs.sh \
  && cd "${ROS2_WS}/src" \
  && git clone --recursive https://github.com/CharlesCossette/uwb_ros2.git \
  && cd uwb_ros2/uwb_driver \
  && pip3 install . \
  && rm -rf "${ROS2_WS}/src"  \
  && rm -rf /var/lib/apt/lists/* 

# below is an attempt to fix CUDA dependencies, but it is easier to just compile 
# all packages at runtime instead, which is for now the preferred way (simply using 
# the make build-zed_ros2 command.

# for some reason, the library is now looking for libcuda.so.1 instead of libcuda.so.1, 
# so we temporarily create that symlink.
#&& ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/stubs/libcuda.so.1 \
#&& LD_LIBRARY_PATH=/usr/local/cuda/lib64/stubs/:/usr/lib/x86_64-linux-gnu/:$LD_LIBRARY_PATH \
#&& colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release --packages-select zed_interfaces zed_components \
#&& rm src/zed-ros2-wrapper/zed_wrapper/config/common.yaml \ 
#&& rm /usr/local/cuda/lib64/stubs/libcuda.so.1 \

# below doesn't work. we need to install zed_wrapper at runtime because of the CUDA dependency.
# (the file libnvidia-encode is just a link to something created by CUDA at runtime)
# SO INSTEAD OF DOING THIS HERE, WE JUST BUILD THEM ALL AT RUNTIME NOW. 
#&& ln -s /usr/lib/x86_64-linux-gnu/libnvidia-encoda.so.1 ... doesn't work

WORKDIR "${ROS2_WS}/workspace"
COPY ./ros_entrypoint.sh "/home/ros/ros_entrypoint.sh"

ENTRYPOINT ["/home/ros/ros_entrypoint.sh"]
