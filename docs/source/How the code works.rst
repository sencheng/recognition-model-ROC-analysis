How the code works
===================

The file ``toy_example.py`` is a good start to get intuitive understanding of the model. After importing all the relevant modules, the simulation parameters are initialized by::

	params=sim_params()

The default parameters can be inspected in ``utils/set_params.py``. However, you can modify the parameters the way you want using a dictionary containing the attribute names and values::

	params_change={'noise':[0.3],'trials':5,'notes':'awesome simulation, the parameters of which should be remembered'}
	params.update_params(params_change)

For instance, the code above changes the memory ``noise`` value to 0.3 and sets the number of ``trials`` to 5.  If provided, the attribute ``notes`` makes sure that the simulation ID is stored in ``/Log/notes.csv``. This allows to reanalyze important simulations, access and compare their parameters. Also, these are the simulations that are **not** subject to regular clean-ups performed using the file ``/utils/clean_up.py``, which removes data and figures for simulations that are older than N days. 

Once the parameters are set, it's time to load the stimuli. The PCA-reduced image representations from the neural net are stored in ``/Input/dataset_faces.npy``. The class ``input_patterns`` loads the dataset, chooses the specified number of the stimuli and assigns them to target and lure probes::

	input_patterns = inp.probes(params)
	probes = input_patterns.probe_faces()
	input_patterns.probe_assignment([-1]) 


Next, a memory system is initialized and scaling is performed for studied and test items::

	mem_system=mem.memory_system(params,1)
	mem_system.perform_scaling(input_patterns.study_all, 'study') 
	mem_system.perform_scaling(input_patterns.test, 'test')


Finally, the recognition memory test is performed on the loaded stimuli for all noise levels. The memory tests is done for memory systems with different scaling values, for lures with different degrees of similarity to the targets (params.offset)::

	for nn in params.noise:
    	   memory_test_basic(params,mem_system,params.offset[0],nn)   

If the ``params.save_metadata`` attribute is True, metadata will be stored. This basically means that the ``params`` object is pickled, so that we can later load it and have the exact parameter configuration of the given simulation::
	
	if params.save_metadata:
           save_data(params,'metadata_'+params.simID,file_format='pkl',folder=params.path+'/Log')

This is extremely helpful when trying to replicate the results. In addition, the file ``utils/compare_params`` can actually compare two simulations and point out what has changed. 


Note that the simulation data is always stored in ``/Data/simID`` and the metdata are stored in ``/Log/``.
Obviously, the full model has more conditions and operations but this example should give you a fist glance on some of the core functions. 

Good luck with the tests and have fun exploring the code! :)












