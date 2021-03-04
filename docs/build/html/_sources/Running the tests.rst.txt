Running the tests
===================

Once you are all set up and ready, you can test whether the extended code actually runs by executing the ``recognition-memory/start/test`` file in the terminal. This file activates the virtual environment::

	cd ../OOC/Code
	source activate rec-mem

and runs the main simulation routine for 20 trials and saves the data in the corresponding directories::

	python main_test.py


After the Python simulations are finished, the Yonelinas model is used to fit the data. This part of the code is performed in Matlab::

	matlab --nodisplay <  utils/dpsd_fit_test.m> out.log

Finally, the results are analyzed and the plots are saved in the directory ``recognition-memory/OOC/Figures``::

	python analysis_test.py

.. note::

	Currently the matlab output plotting is disable to avoid problems with the rednering. If you want to explore the output figure, please enable it by uncommenting the corresponding section at the end of the following file:  ``recognition-memory/roc-toolbox/main/roc_solver1.m`` and use ``matlab -softwareopengl`` to start  matlab.  
