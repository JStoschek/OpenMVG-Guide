# Summary of OpenMVG

OpenMVG (Open Multiple View Geometry) is an open-source library designed for photogrammetry and computer vision, focusing on Structure from Motion (SfM) and 3D reconstruction. Written in C++, it supports feature extraction, matching, robust estimation, and camera modeling to build accurate 3D models from 2D images. OpenMVG offers both incremental and global SfM pipelines, integrates with tools like OpenMVS for dense reconstruction, and supports various export formats for visualization and further processing.

# Instructions 

Required tools:
 
 - Git
 - Docker

Clone repository into folder and build the docker image:
```shell
$ git clone https://github.com/JStoschek/OpenMVG-Guide.git
$ cd OpenMVG-Guide/
$ git clone --recursive https://github.com/openMVG/openMVG.git
$ cd openMVG/
$ docker build . -t openmvg
```

Run docker container:
```shell
$ docker run -it --rm -v /Path/To/OpenMVG-Guide:/files openmvg
EXAMPLE: $ docker run -it --rm -v /Users/jstoschek/Documents/GitHub/OpenMVG-Guide:/files openmvg
```

Run Python Script:
```shell
$ cd files/
$ python3 run_OpenMVG_SfM.py
```






