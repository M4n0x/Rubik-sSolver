# Rubik's Solver

Rubik's Solver is a little image processing project that aims to solve rubik's cubes by analysing the rubik's faces as images and yielding a solution.

# Installation

First of all you need to clone the entire project locally on your computer. Be sure to have a webcam connected to your computer hence the application need a connection to a camera in order to work !

The project uses virtual environnements to reduce the tole on your python installation. It should work with python >3.7, anterior versions have not been tested.
To install the dependencies, it is _recommended_ that you also use virtual environnements. It will create a folder for this project at its root and stock the dependencies there, acting as a local environnement. It will not pollute your python global installation/environnement.

### Installing v-env

To install the v-env library, you can use pip :
```python -m pip install virtualenv```
You can now create your environnement !

### creating a v-env

You are now ready to create the folder that represents the local virtual environnement.
Place yourself at the root of the project and type : ```python -m venv {name}```
For example : ```python -m venv .venv```
Using the command n°2, a .venv folder should now be present at the anchor of your terminal (ideally, the root of the project).

### Activating the environnement

The local environnement has to be __activated__ before you use it.
To do that, use the command ```. .\.venv\Scripts\activate``` (with the folder named .venv).
If the command is successfull, your terminal line should be preceded with a (.venv) chip indicating you are running it in a virtual environnement.

### Dependencies installation

The first time you use the project, you have to install the dependency once.
This step Can be done without a virtual env, but it will install the dependency in your global python installation, which can be harmfull.
To use the virtual environnement, please create it using the step above and __be carefull that the local environnement is activated :-)__
```python -m pip install -r requierements```

### Use Kyubi

To use kyubi once you have a camera connected to your computer and have installed all dependancies above, you can just run the main script

`.\kyubi.py`

And let's the magic do the trick !
