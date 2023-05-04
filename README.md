# Myhal580 dataset

Software stack for recording stereo camera datasets in Myhal 580 with Vicon ground truth and apriltags.

## High-level overview

1. Standalone dockerfiles 

To retrieve data from the stereo camera (zed2), we use a standalone docker image that runs foxy and the correct CUDA versions compatible with this laptop. To build this image, you need to run:
```
cd docker
make build-zed2_ros
```
because of CUDA runtime dependencies the make command is used rather than building the image directly from the dockerfile.

To retrieve data from the UWB modules, run
```
cd docker
make build-uwb_ros
```

2. local ROS environment


## Local install instructions

Can either use docker (see below), or a local install of robostack (ros environment that comes with nice python integrations)

- install ros-humble-desktop using the [instructions](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)
- install ros-dev-tools


## Docker install intructions

You can also use docker for running ros.

Current pipeline to install the hierarchy of docker images. 

```
make build-zed-compiled
make build-overlay
```

## Vicon instructions

- To create a new object, Press ALT and select all markers part of the object
- Need to create one object for the camera rig, and one object for all the apriltag markers. 
- Export the apriltag markers as a vsk file in the end of the trial. This will be used to 
get the individual marker locations (cannot be recovered from the gt poses published in ros)  

## Running instructions

For default running, just run
```
docker/tmux_setup.sh
```

The docker container to run for development is ros_terminal.
```
make run-ros-term
```

The following command starts the ZED 2 node in a separate container (zed2_publish):
```
make run-zed2
```

The following command opens rviz for visualization in s aseparate container (rviz_container)
```
make run-rviz
```

## Credits

- [guide](https://roboticseabass.com/2021/04/21/docker-and-ros/) for the hierarchy of docker images.
