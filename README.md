# SIC data analysis

## Run the IPython Notebooks

There is a requirements.txt file to run the IPython Notebooks from a virtual environment.

### Pip Package Manager
First, you should have pip. If you have Ubuntu, one option is to use apt:

```
sudo apt-get install python3-pip
```

Some other options are available following this link:
[Install pip on Linux](https://packaging.python.org/guides/installing-using-linux-tools/).

### Install virtualenv
Once you have pip installed, you are able to install virtualenv:

```
sudo pip3 install virtualenv 
```

### Create the virtual environment
Using virtualenv, you can create a new virtual environment:

```
virtualenv --python=python3 ipythonenv
```

You can use any name instead of ```ipythonenv```.


### Activate the environment
Now you have a clean virtual environment, but it is not activated. So, you have to activate it:

```
source ipythonenv/bin/activate
```

Again, if you have used another name for the environment, repeat it here.


### Install the dependences
We provide a ```requirements.txt``` file containing the dependences to serve a IPython Notebook. With the environment activated, you can install the dependences inside it running:

```
pip install -r requirements.txt
```

### Run the Notebooks
The analysis notebooks are in the ```/src``` folder. So, you should set it as the current directory, and run some notebook you want. For example:

```
cd src
ipython notebook mtie.ipynb
```

It will serve the notebook and open your default browser.
If the browser does not open automatically, you will see several log messages in the console. One of them contains a link that you can open using the browser you want.

## Useful links
[Great explanation about MTIE and TDEV meanings](http://users.rcn.com/wpacino/jitwtutr/jitwtutr.htm).
[David W. Allan Website](http://www.allanstime.com/).
[SIC Protocol Implementation on Github](https://github.com/CoNexDat/SIC).
