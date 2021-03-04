.. An algorithmic model of recognition memory documentation master file, created by
   sphinx-quickstart on Tue Jul 31 19:43:56 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Background
======================================================================

Recognition memory refers to the ability to distinguish between novel and familiar information. There are many experimental paradigms studying recognition memory, including the so-called yes/know task, remember/know paradigm, spontaneous novel recognition in rodents etc. In its current form, our model focuses on the yes/no task. In this task, the participants first study a list of items (words or images) one at a time. In the subsequent test phase, same items (called targets) are presented together with the new items (lures).
The task of the participants is to indicate whether each item is old or new together with a confidence rating (usually on a 6-point scale, where 1 is sure new and 6 reflect sure old responses). The confidence ratings are used to build Receiver Operating Characteristic (ROC)-curves (see below). 

.. figure:: /fig-rec_test.png
   :scale: 15 %
   :align: center

   A graphical representation of  the yes/no task



Signal detection theory and ROC analysis
-----------------------------------------

Signal detection theory attempts to explain decision making under uncertainty (Green and Swets, 1966). In this theory, decisions are thought to depend on subject's sensitivity to the stimulus and the so-called response bias or response criterion. The notion of sensitivity is typically demonstrated by  overlapping normal distributions of noise (N) and signal+noise (S+N), where signal refers to the representation of a stimulus, while everything else constitutes the noise. The sensitivity of a participant to the stimulus is given by the separation between these two distributions (the distance between the means). The response criterion is conceptualized as a threshold: whenever the perceived effect exceeds the cutoff value, a positive response is given (see the figure below). There are four possible response outcomes: hits (yes to present stimulus), correct rejections (no to absent stimulus), misses (no to present stimulus) and false alarms (yes to absent stimulus). 

.. figure:: /ROC_explained.png
   :scale: 70%
   :align: center
Recognition memory tests are quite similar to sensory detection experiments in that in recognition memory, participants judge whether or not an item was presented in the preceding study phase (Yonelinas et al., 2010; Yonelinas and Parks,2007). Signal detection theory was therefore used to model recognition memory aswell. The studied and novel items presented during the testing phase are referred to as targets and lures, respectively. Rather than inducing the subjects to use different response criteria, in a recognition memory study, participants are simply
asked to indicate how sure they are in their response in addition to each yes/no (old/new) response. 
In the figure above, a scenario is described where 25 items have been studied and then presented with 25 lures in the study phase. For each confidence rate, the **cumulative** hit and false alarm rates are calculated. The performance is measured by ROC-curves, where the hit rate is plotted against the false alarm  rate for different criteria. The leftmost data points reflect the most conservative criteria, and the criteria are relaxted from left to right. 


Single and dual process models of recognition memory
-----------------------------------------------------

Traditional signal detection theory predicts that the hit and false alarm rates are low both for conservative criteria and increase when the criteria are relaxed. Recognition memory experiments, however, have consistently shown ROC-curves with a pronounced y-intercept, meaning high hit rate at conservative criterion, while the false alarm rate is at floor. This pattern suggests that recognition memory may not be a pure signal detection process. Two prominent theories have attempted to explain the above-mentioned phenomenon. 
The single-process models of recognition memory have proposed that the y-intercept of the ROC-curves reflects strong memory signal (see the left figure). In particular, these models assume that the memory strength of studied and novel items can be represented as two overlapping distributions. Since the studied items have been seen recently, their memory strength is higher, i.e. the distribution has higher mean. In addition, it also has a higher variance since some items are encoded better than the others. According to the single-process models, the difference between the means of the two distributions reflects the curvilinearity of recognition ROCs, while th e variance of the target distribution gives rise to the y-intercept. 

.. figure:: /single_process.jpg
   :scale: 50%
   :align: center
   
   Single process view of recognition memory (reproduced from Squire et al. 2007)


By contrast, the dual-process models assume that the y-intercept and curvilinearity of the ROC-curves reflect two distinct processes: recollection and familiarity, respectively (see the right figure). Recollection refers to the recall of contextual information, such as when or where something happened, while familiarity is the vague knowledge of a previous encounter. In this view, familiarity can be modeled by classical signal detection theory, where target and noise distributions have equal variances. Recollection is believed to be a threshold
process meaning that there is a high recollective threshold that can be passed only by some target items. According to this theory, recognition judgments only rely on familiarity if recollection has failed.

.. figure:: /dual_process.jpg
   :scale: 50%
   :align: center
   
   Dual process view of recognition memory (reproduced from Squire et al. 2007)

Neural signature of recognition memory
-------------------------------------------

In the context of recognition memory, two brain areas have been discussed extensively: the hippocampus and the adjacent perirhinal cortex. These structures are situated in the medial temporal cortex, a region generally thought to be critical for memory. The above-mentioned single and dual process models also differ in their assumptions about the involvement of these brain regions in recognition memory. The dual-process proponents take a strong stance on the involvement of hippocampus in recollection and perirhinal cortex in familiarity. The single-process advocates, by contrast, argue that hippocampus and perirhinal cortex operate on qualitatively similar information differing only in the memory strength. 

.. figure:: /medial_temporal_lobe.png
   :scale: 50%
   :align: center
   
   The main structures in the medial temporal lobe (Reproduced from Kessels and Kopelman 2012)

In addition to their role in recognition memory, hippocampus and perirhinal cortex are part of the ventral stream of visual perception responsible for object identification (rescognizing a cup as a cup). According to the standard view, the parirhinal cortex receives mainly object information (identity and other features), while the hippocampus also receives spatial information. This seems to support the dual-process view assuming that the hippocampus adds contextual details to memory. However, the reality is much more complicated because the perirhinal cortex is reciprocally connected to the parahippocampal gyrus that also receives spatial information. 

Pattern separation in the hippocampus
--------------------------------------

Pattern separation refers to the sparse encoding of similar items, i.e. that dissimilar representations are assigned for similar stimuli/experiences. We have highly overlapping experiences (e.g all birthday parties share some features) and if no pattern separation was at play, novel information would overwrite the old ones (you wouldn't remember your birthday 2 years ago). 

.. figure:: /Yassa2011.png
   :scale: 50%
   :align: center
   
   Reproduced from Yassa et al. 2011

A widely accepted view claims that the unique circuitry of the hippocampus allows to support pattern separation. In particular, the hippocampus is divided into three subregions called cornu ammonis: CA1, CA2 and CA3. It is part of a larger structure called hippocampal formation further including dentate gyrus (DG), subiculum (S) and entorhinal cortex (EC). There is a distinguished feedforward connectivity in the hippocampus called trisynaptic loop. In particular, the projections from II layer cells of EC are sent to the granule cells in the DG. The axons from these cells reach the CA3 neurons through the so-called mossy fibers. Finally, the CA3 projections innervate the CA1 area via Schaffer collaterals. In addition, there are extensive recurrent connections within CA3 region.

The key part relevant for pattern separation is supposedely the DG. In particular, the neurons in the DG  employ sparse coding,  each neuron in the dentate gyrus projects to only a dozen CA3 cells (Amaral et al., 2007). Additionally, DG is one of the few brain regions where adult neurogenesis takes place. The addition of novel cells into the network is suggested to contribute to the representation of novel information and thus, avoid interference with previously encoded representations. 

 


