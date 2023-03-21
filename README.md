# Myhal580 dataset

## Install intructions

We use docker for running ros.

Current pipeline to install the hierarchy of docker images. 

```
make build-zed-compiled # Compiles zed ros libraries
make build-overlay # builds overlay 
```

## Vicon instructions
To create a new object, Press ALT and select all markers part of the object



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

-- [guide](https://roboticseabass.com/2021/04/21/docker-and-ros/) for the hierarchy of docker images.
