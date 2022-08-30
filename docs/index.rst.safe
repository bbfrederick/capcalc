.. capcalc documentation master file, created by
   sphinx-quickstart on Thu Jun 16 15:27:19 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The pretty html version of this file can be found here: http://capcalc.readthedocs.io/en/latest/

Capcalc
==========
capcalc is a suite of python programs used to perform coactivation pattern analysis on time series data.  It uses K-Means clustering to find a set of "activation states" that represent the covarying patterns in the data.

.. toctree::
   :maxdepth: 2

Introduction
============
      
Python version compatibility: 
-----------------------------
This code has depends on the rapidtide package, which dropped support for Python 2.x a few years ago, so as of now, capcalc is python 3 only
      
How do I cite this?
-------------------
Good question!  I think the following will work, although I should probably get a DOI for this.
	Frederick, B, capcalc [Computer Software] (2017).  Retrieved from https://github.com/bbfrederick/capcalc.

What’s included in this package?
================================
For the time being, I’m including the following:

capfromtcs
----------

Description:
^^^^^^^^^^^^

	This scripts takes a file containing a number of timecourses, does some preprocessing on them, then calculates the coactivation patterns found in the data.

Inputs:
^^^^^^^
	There are three required inputs:

	The input file is a text file containing 2 or more timecourses in columns separated by whitespace.  Each row is a time point.

        The outputname is the prefix of all output files.

        The samplerate (or sampletime) is the frequency (or timestep) of the input data.
     
Outputs:
^^^^^^^^
	Outputs are space or space by time Nifti files (depending on the file), and some text files containing textual information, histograms, or numbers.  Output spatial dimensions and file type match the input dimensions and file type (Nifti1 in, Nifti1 out).  Depending on the file type of map, there can be no time dimension, a time dimension that matches the input file, or something else, such as a time lag dimension for a correlation map.
	OUTPUT_normalized.txt
	    This is a text file containing the input timecourses after applying the selected normalization.
	    
	OUTPUT_clustercenters.txt
	    This is a text file with NUMCLUSTER lines, one for each state, specifying the center location of the cluster (each line has the same number of columns as the number of input timecourses).
	    
	OUTPUT_statelabels.txt
	    This is a text file with one line per timepoint.  Each line is the assigned state for the given timepoint in the input data.
	    
	OUTPUT_silhouettesegmentstats.csv

	OUTPUT_overallsilhouettemean.csv
            This text file has one line per cluster, giving the mean of the mean silhouette score of all the segments that spent any time in that state.

	OUTPUT_pctsegsinstate.txt
            This text file has one line per cluster, indicating what percentage of subjects (segments) spent any time in this state.

	OUTPUT_seg_XXXX_instate_YY.txt
	    This is a text file with one line per timepoint in the segment.  The value is 1 if the system is in state YY, 0 otherwise.
	    
	OUTPUT_seg_XXXX_statestats.csv
	    This is a text file with one line per cluster (state), with the following columns:
	    
                * percentage of segment spent in state
                * number of continuous runs in state
		* total number of TRs in state
                * minimum number of TRs spent in state
                * maximum number of TRs spent in state
                * average number of TRs spent in state
                * median number of TRs spent in state
                * standard deviation of the number of TRs spent in state
	    
	OUTPUT_seg_XXXX_statetimestats.csv
	    This is the equivalent of the statestats file, where the units are time in seconds rather than TRs
	     
	OUTPUT_seg_XXXX_statelabels.txt
	    This is a text file with one line per timepoint.  Each line is the assigned state for the given timepoint in the segment.
	    
	OUTPUT_seg_XXXX_silhouetteclusterstats.csv
	    This is a text file with one line per cluster.  Each line has four columns:
	    
	        * the mean silhouette score for that cluster in that segment.
	        * the median silhouette score for that cluster in that segment.
		* the minimum silhouette score for that cluster in that segment.
		* the maximum silhouette score for that cluster in thate segment.
		
	OUTPUT_seg_XXXX_rawtransmat.nii.gz
	    This is a NIFTI file with dimensions n_states by n_states.  The number of transitions from state a to state b is in location [a, b]

	OUTPUT_seg_XXXX_normtransmat.nii.gz
	    This is a NIFTI file containing the same information as the rawtransmat file, but each row is normalized to sum to 1, making, so the numbers represent the transition probabilities, rather than the total number of transitions.
	   
	OUTPUT_seg_XXXX_offdiagtransmat.nii.gz
	    This is a NIFTI file containing the same information as the normtransmat file, except that the diagonal elements have been set to zero.  This is therefore the relative probability transitioning to each possible destination state in the case where the state does not simply persist.
	
    
	OUTPUT_seg_XXXX_rawtransmat.csv
	OUTPUT_seg_XXXX_normtransmat.csv
	OUTPUT_seg_XXXX_offdiagtransmat.csv
            The same data as the above NIFTI files, but as a csv file.
Usage:
^^^^^^

	::

		capfromtcs - calculate and cluster coactivation patterns for a set of timecourses

		usage: capfromtcs -i timecoursefile -o outputfile --samplefreq=FREQ --sampletime=TSTEP
				  [--nodetrend] [-s STARTTIME] [-D DURATION]
				  [-F LOWERFREQ,UPPERFREQ[,LOWERSTOP,UPPERSTOP]] [-V] [-L] [-R] [-C]
				  [-m] [-n NUMCLUSTER] [-b BATCHSIZE] [-S SEGMENTSIZE] [-E SEGMENTTYPE] [-I INITIALIZATIONS]
				  [--noscale] [--nonorm] [--pctnorm] [--varnorm] [--stdnorm] [--ppnorm] [--quality]
				  [--pca] [--ica] [-p NUMCOMPONENTS]

		required arguments:
		    -i, --infile=TIMECOURSEFILE  - text file mulitple timeseries
		    -o, --outfile=OUTNAME        - the root name of the output files

		    --samplefreq=FREQ            - sample frequency of all timecourses is FREQ 
			   or
		    --sampletime=TSTEP           - time step of all timecourses is TSTEP 
						   NB: --samplefreq and --sampletime are two ways to specify
						   the same thing.

		optional arguments:

		  Data selection/partition:
		    -s STARTTIME                 - time of first datapoint to use in seconds in the first file
		    -D DURATION                  - amount of data to use in seconds
		    -S SEGMENTSIZE,[SEGSIZE2,...SEGSIZEN]
						 - treat the timecourses as segments of length SEGMENTSIZE for preprocessing.
		    -E SEGTYPE,SEGTYPE2[,...SEGTYPEN]
						 - group subsegments for summary statistics.  All subsegments in the same group must be the same length
						   If there are multiple, comma separated numbers, treat these as subsegment lengths.
						   Default segmentsize is the entire length
		  Clustering:
		    -m                           - run MiniBatch Kmeans rather than conventional - use with very large datasets
		    -n NUMCLUSTER                - set the number of clusters to NUMCLUSTER (default is 8)
		    -b BATCHSIZE                 - use a batchsize of BATCHSIZE if doing MiniBatch - ignored if not.  Default is 1000
		    --dbscan                     - perform dbscan clustering
		    --hdbscan                    - perform hdbscan clustering
		    -I INITIALIZATIONS           - Restart KMeans INITIALIZATIONS times to find best fit (default is 1000)

		  Preprocessing:
		    -F                           - filter data and regressors from LOWERFREQ to UPPERFREQ.
						   LOWERSTOP and UPPERSTOP can be specified, or will be calculated automatically
		    -V                           - filter data and regressors to VLF band
		    -L                           - filter data and regressors to LFO band
		    -R                           - filter data and regressors to respiratory band
		    -C                           - filter data and regressors to cardiac band
		    --nodetrend                  - do not detrend the data before correlation
		    --noscale                    - don't perform vector magnitude scaling
		    --nonorm                     - don't normalize timecourses
		    --pctnorm                    - scale each timecourse to it's percentage of the mean
		    --varnorm                    - scale each timecourse to have a variance of 1.0 (default)
		    --stdnorm                    - scale each timecourse to have a standard deviation of 1.0
		    --ppnorm                     - scale each timecourse to have a peak to peak range of 1.0
		    --pca                        - perform PCA dimensionality reduction prior to analysis
		    --ica                        - perform ICA dimensionality reduction prior to analysis
		    -p NUMCOMPONENTS             - set the number of p/ica components to NUMCOMPONENTS (default is 8).  Set to -1 to estimate
		    --noscale                    - do not apply standard scaler befor cluster fitting

		  Other:
		    --GBR                        - apply gradient boosting regressor testing on clusters
		    -d                           - display some quality metrics
		    --quality                    - perform a silhouette test to evaluate fit quality
		    -v                           - turn on verbose mode
        
	These options are somewhat self-explanatory.  I will be expanding this section of the manual going forward, but I want to put something here to get this out here.


maptoroi
--------

Description:
^^^^^^^^^^^^

	maptoroi takes ROI values from a text file and maps them back onto a NIFTI image for display.

Inputs:
^^^^^^^
	maptoroi requires an input text file with 1 column per region giving the value of the ROI.  If there are multiple rows, each row corresponds to a time point.  It also requires a template NIFTI file.

Outputs:
^^^^^^^^
	showxcorr outputs everything to standard out, including the Pearson correlation, the maximum cross correlation, the time of maximum cross correlation, and estimates of the significance levels (if specified).  There are no output files.

Usage:
^^^^^^

	::

		usage: maptoroi inputfile templatefile outputroot

		required arguments:
		    inputfile        - the name of the file with the roi values to be mapped back to image space
		    templatefile     - the name of the template region file
		    outputfile       - the name of the output nifti file


::


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

