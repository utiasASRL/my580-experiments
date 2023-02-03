# Myhal580 dataset

## Install intructions

We use docker for running ros.

Current pipeline to install the hierarchy of docker images. 

```
make build-core # creates zed_ros2
make build-base # creates zed_ros2_base
make build-zed-compiled # Compiles zed ros libraries
make build-overlay # builds overlay 
```

## Running instructions

The docker container to run for development is ros_terminal.

```
make run-ros-term
```

The image is run with the folder `src/my580_ros2/` mounted to the identical location
inside the docker image, so any changes are automatically in synch. 

The following command starts the ZED 2 node in a separate container (zed2_publish):

```
make run-zed2
```

The following command opens rviz for visualization in s aseparate container (rviz_container)
```
make run-rviz
```



## Credits

We followed [this](https://roboticseabass.com/2021/04/21/docker-and-ros/) helpful guide for the hierarchy of docker images.
