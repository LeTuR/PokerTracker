# PokerTracker

Main objectives are :
- Create parsers for the main online poker platform.
- Create a hand player based on the hands played on online platform.
- Generate stats with a player hand history of a player.
- Develop a HUD giving stats on villain players on the min poker platform.

Secondary objectives :
- The UI/UX design should not be put aside. 
- Improve your coding
- Making a cross-platform application
- Making a web version of the application

And then what ?
- Making some reinforcement learning (IA) experiments to create a bot. (DO NOT USE THIS AGAINST REAL PLAYER WITH REAL MONEY)


Any help is welcome.

## Setting up the environment

### PyCharm and Anaconda

If you want to use PyCharm follow the following instruction.

Download PyCharm : https://www.jetbrains.com/pycharm/

Download Anaconda : https://www.anaconda.com


Create a clone of the github project :

````
git clone https://github.com/LeTuR/PokerTracker.git
````

Open the project with PyCharm. Set the project interpreter in "Setting" -> "Project".
Add a new conda environment.

### PySide2

The project UI/UX is based on the Qt framework so make sure you install the framework : 

````
pip install PySide2
````

### Tips

If you are not using an IDE such as PyCharm, it is recommended to set your python path to the repertory. With anaconda you can easily do it with :
`````
conda develop /path/to/PokerTracker
`````

for more documentation on the command please check https://docs.conda.io/projects/conda-build/en/latest/resources/commands/conda-develop.html .

## Documentation Rules

Documentation must be the most complete as possible as always...

In this project all the in-code python documentation must follow the google style python Docstrings (for more information check : https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html ).

### Documentation of a Class

A class must be documented with this style :

````python
class ExampleError(Exception):
    """This style must be used to document a class.

    The __init__ method is documented in the class level
    docstring, and NOT as a docstring on the __init__ method itself.

    Note:
        Do not include the `self` parameter in the ``Args`` section.

    Args:
        arg (str): Human readable string describing the arguments.
    
    Attributes:
        att (int): Human readable string describing the attributes.


    """

    def __init__(self, arg):
        self.att = arg
````

### Documentation of a function

Try to use the most often possible multiline document such as :

````python
def function(param):
    """ Here resume in one sentence the function use.

        More details here

        Args:
            param (type): description of the argument

        Returns:
            Describe the result returned by the function
    """
    return function_example()
````
