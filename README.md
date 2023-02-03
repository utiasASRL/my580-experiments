# Myhal580 dataset

## Install intructions

We use docker for running ros.

Current pipeline to install the hierarchy of docker images. 

```
make build-core # creates zed_ros2
make build-base # creates zed_ros2_base
make run-base
```

Run inside container (to build zed ros2 packages):
```
colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release
exit
```

Run outside container:
```
sudo docker ps | grep zed_ros2_base # find CONTAINER_ID (first element of line)
sudo docker commit [CONTAINER_ID] zed_ros2_built # save image
make build-overlay # build overlay image
```

## Running instructions

The docker container to run for development is zed_ros2_overlay.

```
make run-overlay 
```

The image is run with the folder `src/my580_ros2/` mounted to the identical location
inside the docker image, so any changes are automatically in synch. 

## Credits

We followed [this](https://roboticseabass.com/2021/04/21/docker-and-ros/) helpful guide for the hierarchy of docker images.
