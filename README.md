pylaserkb
=========
Bascally, this project comes from team RoboPeak's project, [laserkbd](https://github.com/robopeak/laserkbd). 
In our project, we adopted the same hardware design as team RoboPeak's.
However, instead of C++, all of our code was written in pure Python.
This makes our code be able to run in all OS with Python and OpenCV.

- pylaserkb.py: A module provides core function for processing image, retriving characterstic point, and mapping coordinates between image and desktop surface.
- main.py: A simple program provide a simple GUI interference for users to setup environmental parameters and type with it.


## Dependence
### Ubuntu
```
sudo apt-get install libopencv-dev python-numpy
```

