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
This code has been tested in python 2.7, 3.5, and 3.6.  I try very hard not to use any version dependant features when I write programs, so it will probably work on any subversion of python 3.  I think there is some weirdness in the python's numerical routines in versions 2.6 and below, so no guarantees it will work in anythin lower than 2.7.
      
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
	    
	OUTPUT_silhouettesegmentstats.txt

	OUTPUT_seg_XXXX_instate_YY.txt
	    This is a text file with one line per timepoint in the segment.  The value is 1 if the system is in state YY, 0 otherwise.
	    
	OUTPUT_seg_XXXX_statestats.txt
	    This is a text file with one line per cluster (state), with the following columns:
	    
                * percentage of segment spent in state
                * number of continuous runs in state
		* total number of TRs in state
                * minimum number of TRs spent in state
                * maximum number of TRs spent in state
                * average number of TRs spent in state
                * median number of TRs spent in state
                * standard deviation of the number of TRs spent in state
	    
	OUTPUT_seg_XXXX_statetimestats.txt
	    This is the equivalent of the statestats file, where the units are time in seconds rather than TRs
	     
	OUTPUT_seg_XXXX_statelabels.txt
	    This is a text file with one line per timepoint.  Each line is the assigned state for the given timepoint in the segment.
	    
	OUTPUT_seg_XXXX_silhouetteclusterstats.txt
	    This is a text file with one line per cluster.  Each line has four columns:
	    
	        * the mean silhouette score for that cluster in that segment.
	        * the median silhouette score for that cluster in that segment.
		* the minimum silhouette score for that cluster in that segment.
		* the maximum silhouette score for that cluster in thate segment.
		
	OUTPUT_seg_XXXX_rawtransmat.nii.gz
	    This is a NIFTI file with dimentions n_states by n_states.  The number of transitions from state a to state b is in location [a, b]

	OUTPUT_seg_XXXX_normtransmat.nii.gz
	    This is a NIFTI file containing the same information as the rawtransmat file, but each row is normalized to sum to 1, making, so the numbers represent the transition probabilities, rather than the total number of transitions.
	   
	OUTPUT_seg_XXXX_offdiagtransmat.nii.gz
	    his is a NIFTI file containing the same information as the normtransmat file, except that the diagonal elements have been set to zero.  This is therefore the relative probability transitioning to each possible destination state in the case where the state does not simply persist.
	
    
Usage:
^^^^^^

	::

		capfromtcs - calculate and cluster coactivation patterns for a set of timecourses

		usage: capfromtcs -i timecoursefile -o outputfile --samplefreq=FREQ --sampletime=TSTEP
				  [--nodetrend] [-s STARTTIME] [-D DURATION]
				  [-F LOWERFREQ,UPPERFREQ[,LOWERSTOP,UPPERSTOP]] [-V] [-L] [-R] [-C]
				  [-m] [-n NUMCLUSTER] [-b BATCHSIZE] [-S SEGMENTSIZE] [-I INITIALIZATIONS]
				  [--nonorm] [--pctnorm] [--varnorm] [--stdnorm] [--ppnorm] [--quality]

		required arguments:
		    -i, --infile=TIMECOURSEFILE  - text file mulitple timeseries
		    -o, --outfile=OUTNAME        - the root name of the output files

		    --samplefreq=FREQ            - sample frequency of all timecourses is FREQ 
			   or
		    --sampletime=TSTEP           - time step of all timecourses is TSTEP 
						   NB: --samplefreq and --sampletime are two ways to specify
						   the same thing.

		optional arguments:
		    --nodetrend                  - do not detrend the data before correlation
		    -s STARTTIME                 - time of first datapoint to use in seconds in the first file
		    -D DURATION                  - amount of data to use in seconds
		    -F                           - filter data and regressors from LOWERFREQ to UPPERFREQ.
						   LOWERSTOP and UPPERSTOP can be specified, or will be calculated automatically
		    -V                           - filter data and regressors to VLF band
		    -L                           - filter data and regressors to LFO band
		    -R                           - filter data and regressors to respiratory band
		    -C                           - filter data and regressors to cardiac band
		    -m                           - run MiniBatch Kmeans rather than conventional - use with very large datasets
		    -n NUMCLUSTER                - set the number of clusters to NUMCLUSTER (default is 8)
		    -b BATCHSIZE                 - use a batchsize of BATCHSIZE if doing MiniBatch - ignored if not.  Default is 1000
		    -S SEGMENTSIZE               - treat the timecourses as segments of length SEGMENTSIZE for preprocessing.
						   Default segmentsize is the entire length
		    -I INITIALIZATIONS           - Restart KMeans INITIALIZATIONS times to find best fit (default is 1000)
		    --nonorm                     - don't normalize timecourses
		    --pctnorm                    - scale each timecourse to it's percentage of the mean
		    --varnorm                    - scale each timecourse to have a variance of 1.0 (default)
		    --stdnorm                    - scale each timecourse to have a standard deviation of 1.0
		    --ppnorm                     - scale each timecourse to have a peak to peak range of 1.0
		    --quality                    - perform a silhouette test to evaluate fit quality
		    -v                           - turn on verbose mode
		    --dbscan                     - perform dbscan clustering
		    --pca                        - perform PCA analysis
		    --ica                        - perform ICA analysis
		    --GBR                        - apply gradient boosting regressor testing on clusters
		    -d                           - display some quality metrics
        
	These options are somewhat self-explanatory.  I will be expanding this section of the manual going forward, but I want to put something here to get this out here.


showxcorr
---------

Description:
^^^^^^^^^^^^

	Like rapidtide2, but for single time courses.  Takes two text files as input, calculates and displays 
	the time lagged crosscorrelation between them, fits the maximum time lag, and estimates
	the significance of the correlation.  It has a range of filtering,
	windowing, and correlation options.

Inputs:
^^^^^^^
	showxcorr requires two text files containing timecourses with the same sample rate, one timepoint per line, which are to be correlated, and the sample rate.

Outputs:
^^^^^^^^
	showxcorr outputs everything to standard out, including the Pearson correlation, the maximum cross correlation, the time of maximum cross correlation, and estimates of the significance levels (if specified).  There are no output files.

Usage:
^^^^^^

	::

		showxcorr - calculate and display crosscorrelation between two timeseries

		usage: showxcorr timecourse1 timecourse2 samplerate 
			[-l LABEL] [-s STARTTIME] [-D DURATION] [-d] [-F LOWERFREQ,UPPERFREQ[,LOWERSTOP,UPPERSTOP]] [-V] [-L] [-R] [-C] [-t] [-w] [-f] [-g] [-z FILENAME] [-N TRIALS]
	
		required arguments:
			timecoursefile1     - text file containing a timeseries
			timecoursefile2     - text file containing a timeseries
			samplerate          - the sample rate of the timecourses, in Hz

		optional arguments:
			-t 	     - detrend the data
			-w 	     - prewindow the data
			-g 	     - perform phase alignment transform (phat) rather than 
							standard crosscorrelation
			-l LABEL	     - label for the delay value
			-s STARTTIME  - time of first datapoint to use in seconds in the first file
			-D DURATION   - amount of data to use in seconds
			-r RANGE      - restrict peak search range to +/- RANGE seconds (default is 
							+/-15)
			-d            - turns off display of graph
			-F            - filter data and regressors from LOWERFREQ to UPPERFREQ.
							LOWERSTOP and UPPERSTOP can be specified, or will be 
							calculated automatically
			-V            - filter data and regressors to VLF band
			-L            - filter data and regressors to LFO band
			-R            - filter data and regressors to respiratory band
			-C            - filter data and regressors to cardiac band
			-T            - trim data to match
			-A            - print data on a single summary line
			-a            - if summary mode is on, add a header line showing what values 
							mean
			-f            - negate (flip) second regressor
			-z FILENAME   - use the columns of FILENAME as controlling variables and 
							return the partial correlation
			-N TRIALS     - estimate significance thresholds by Monte Carlo with TRIALS 
							repetition


tidepool
--------

Description:
^^^^^^^^^^^^
	This is a very experimental tool for displaying all of the various maps generated by rapidtide2 in one place, overlayed on an anatomic image.  This makes it a bit easier to see how all the maps are related to one another.  To use it, launch tidepool from the command line, and then select a lag time map - tidpool will figure out the root name and pull in all of the other associated maps.  Works in native or standard space.


Inputs:
^^^^^^^

Outputs:
^^^^^^^^

Usage:
^^^^^^

	::

		usage: tidepool [-h] [-o OFFSETTIME] [-r] [-n] [-t TRVAL] [-d DATAFILEROOT]
					[-a ANATNAME] [-m GEOMASKNAME]

		A program to display the results of a time delay analysis

		optional arguments:
		  -h, --help       show this help message and exit
		  -o OFFSETTIME    Set lag offset
		  -r               enable risetime display
		  -n               enable movie mode
		  -t TRVAL         Set correlation TR
		  -d DATAFILEROOT  Use this dataset (skip initial selection step)
		  -a ANATNAME      Set anatomic mask image
		  -m GEOMASKNAME   Set geometric mask image


tide_funcs.py
-------------

Description:
^^^^^^^^^^^^
	This is the library of the various helper routines that are used by pretty much every program in here for correlation, resampling, filtering, normalization, significance estimation, file I/O, etc.


Inputs:
^^^^^^^

Outputs:
^^^^^^^^

Usage:
^^^^^^

::


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

