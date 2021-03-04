Getting started
===================

The main code is written in Python 3.6.8. We recommend using the Anaconda environment since most of the packages used in our code are installed in Anaconda. Please download the Python 3.6 Version of Anaconda here: https://www.anaconda.com/download/#linux and follow the installation steps. 

The directory **start** is a good place to get started with the code and run the tests. 

The file ``environment.yml`` contains anaconda environment, in which the project was created, create an instance by running the following command. It may take a while. If you want, you can change the first line in the file to rename your environment::

	conda env create -f environment.yml

Then, activate the environment by::

	source activate rec-mem (or the name you gave to the project)

You can perform all these steps automatically by running the file ```get_started```.

You can then bring up the spyder environment by simply typing ``spyder`` in the terminal. Feel free to use any other environment or run the code directly in the terminal.

For Matlab simulations, the ROC-Toolbox by Koen et al. 2017 (https://github.com/jdkoen/roc_toolbox) is used. Our current simulations run in Matlab17a. Depending on the Matlab version, there may be some issues with graphics, which sometimes annoyingly manifest themselves by freezing the code. In that case, we recommend using the OpenGL rendering. For that you can start the Matlab by entering ``matlab -softwareopengl`` in the command line (in Linux).

Once the virtual environment is set and Matlab installed, you can proceed to running the tests. 



