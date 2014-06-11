pylaserkbd
=========
Bascally, this project comes from team RoboPeak's project, [laserkbd](https://github.com/robopeak/laserkbd). 
In our project, we adopted the same hardware design as team RoboPeak's.
However, instead of C++, all of our code was written in pure Python.
This makes our code be able to run on OS with Python and OpenCV.

- pylaserkb.py: A module provides core function for processing image, retriving characterstic point, and mapping coordinates between image and desktop surface.
- main.py: A simple program provides a simple GUI interference for users to setup environmental parameters and type with it.

## Dependence
### Ubuntu
```
sudo apt-get install libopencv-dev python-numpy
```

### python packages
#### [PyUserInput](https://github.com/SavinaRoja/PyUserInput)
```
git clone https://github.com/SavinaRoja/PyUserInput.git
cd PyUserInput
python setup.py install
```
You may also want to check the dependencies of PyUserInput.
- Linux: Xlib
```
pip install svn+https://python-xlib.svn.sourceforge.net/svnroot/python-xlib/trunk/
```
## Flow Chart
![Flow Chart](https://docs.google.com/drawings/d/1k_QXaa3FdJokMQoF_Lo1fDbnYydQrn7BCmn4QK0cIOw/pub?w=960&h=720)
