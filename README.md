# Myhal580 dataset

Software stack for recording stereo camera datasets in Myhal 580 with Vicon ground truth and apriltags.

Make sure to clone all the submodules (in [workspace/src](./workspace/src/)) by running

```
git clone --recurse-submodules git@github.com:utiasASRL/my580-experiments
```

## High-level overview

We provide a docker image with all the basic dependencies, including CUDA support, the stereolabs libraries, and an install of ros2 foxy. It can be installed using
```
cd docker
make build-zed_ros2
```
During the image build, all submodules (see [workspace/src](./workspace/src/)) are cloned, their required rosdeps and other dependencies are installed (but not the packages themselves!)

This base image is then run with all of the workspace folder mounted, and all the ros packages are built during run-time. Because the install/ and build/ folders are also shared, this process only takes long the first time. Also, because we use symlink-install, most code changes do not require a rebuild at all. When a rebuilt is required, simply run `make build-zed_ros2` again and the build will be incremental. When the rosdep dependencies change, the changes need to be pushed to github so that they can be pulled in during the initial image build. 

Finally, the UWB is built using

```
cd docker
make build-uwb
```

## Vicon instructions
- To create a new object, Press ALT and select all markers part of the object
- Need to create one object for the camera rig, and one object for all the apriltag markers. 
- Export the apriltag markers as a vsk file in the end of the trial. This will be used to 
get the individual marker locations (cannot be recovered from the gt poses published in ros)  

## Running instructions

For default experiments, just run
```
docker/tmux_setup.sh
```

This will create a nice layout of all different ros nodes. They can also be run individually by calling `make TARGET` where TARGET is the desired node, e.g. `make run-vicon`. See `[docker/Makefile](./docker/Makefile)` for all options.


## Credits
- [guide](https://roboticseabass.com/2021/04/21/docker-and-ros/) for the hierarchy of docker images.
