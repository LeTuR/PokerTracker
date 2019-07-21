# PokerTracker

## Setting up the environment

### PyCharm and Anaconda

Download PyCharm : https://www.jetbrains.com/pycharm/

Download Anaconda : https://www.anaconda.com


Create a clone of the github project :

````
git clone https://github.com/LeTuR/PokerTracker.git
````

Open the project with PyCharm. Set the project interpreter in "Setting" -> "Project".
Add a new conda environment.

#### Installing Kivy

Kivy is an open source library for developing multi-touch applications see
https://kivy.org/#home. In order to install
it on anaconda download it via conda package manager. Open the terminal, if conda environment 
is not activated launch :

```
conda activate PokerTracker
```
Then install the kivy library with :

```
conda install kivy -c conda-forge
```
Kivy also need PyGame library :
```
pip install pygame
```
The environment should now be ready !

##### Adding syntax highlight for kv files

If you want syntax highlight for .kv file, the import setting for PyCharm can be found
here : https://github.com/Zen-CODE/kivybits/tree/master/IDE.

> ###### KV Lang File Type Support

>Download [this file](https://github.com/Zen-CODE/kivybits/blob/master/IDE/PyCharm_kv_completion.jar?raw=true): 

>On Pycharm’s main menu, click "File"-> "Import" (or Import Settings)

>Select this file and PyCharm will present a dialog with filetypes ticked. Click OK.

>You are done. Restart PyCharm.



