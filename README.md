# Roguelike
A roguelike written using the python-tcod library. 
The main feature is a multiplayer component with x-com style movement and turn based combat. 


## Installation
Install it in a python virtual environment with Python 3.5+, newest preferred. 
Specific development installations for different operating systems are detailed below. 

### Windows
Download a version of python 3.5+ from https://www.python.org/downloads/.
Make sure you the python binaries are in the Windows PATH variable.

Clone this repository and install the requirements using the following command, 
making sure the pip executable links to a python version 3.5 or higher.

Install the requirements file by running the following command from the root directory of the project:

```shell script
pip install -r requirements.txt
```

You should then be able to run the game by running the following command:

```shell script
python main.py
```

### Ubuntu


Follow the instructions for Windows for installing the requirements file.
Additionally, install the SDL2 development library by running the following command:

```shell script
sudo apt install libsdl2-dev
``` 