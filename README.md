# Roguelike
A roguelike written using the python-tcod library. 
The main feature is a multiplayer component with x-com style movement and turn based combat. 


## Installation
Install it in a python virtual environment with Python 3.8 at the least. Recent updates have bumped the version to 3
.8 or higher. Specific development installations for different operating systems are detailed below. 

### Windows
Download a version of python 3.8+ from https://www.python.org/downloads/.
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

### Code points to fix
Problems in the codebase that need to be solved in order of importance go here for my own reference. 

#### Ui Code
* Opening a window from another window requires a reference to the screen object or requires a method calling back to
 the game client.
    * Possibly solved by using a singleton for the screen class.
* The Window class is sequentially coupled when it is created, the pack method of the container class has to be
 called before it's layer console is created.
* The pack method in the Container class takes in a widget to align itself to. This forces the implementors to pass
 themselves to their own method. This is ugly.
