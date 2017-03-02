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
Why do I want to know about time lagged correlations?
-----------------------------------------------------
This comes out of work by our group (The Opto-Magnetic group at McLean Hospital - http://www.nirs-fmri.net) looking at the correlations between neuroimaging data (fMRI) and NIRS data recorded simultaneously, either in the brain or the periphery.  We found that a large fraction of the "noise" we found at low frequency in fMRI data was due to real, random[*] fluctuations of blood oxygenation and volume (both of which affect the intensity of BOLD fMRI images) in the blood passing through the brain. More interestingly, because these characteristics of blood move with the blood itself, this gives you a way to determine blood arrival time at any location in the brain. This is interesting in and of itself, but also, this gives you a method for optimally modelling (and removing) in band physiological noise from fMRI data (see references below).
 
After working with this for several years we've also found that you don't need to used simultaneous NIRS to find this blood borne signal - you can get it from blood rich BOLD voxels for example in the superior sagittal sinus, or bootstrap it out of the global mean signal in the BOLD data. You can also track exogenously applied waveforms, such as hypercarbic and/or hyperoxic gas challenges to really boost your signal to noise.  So there are lots of times when you might want to do this type of correlation analysis.  This package provides the tools to make that easier.
      
As an aside, some of these tools are just generally useful for looking at correlations between timecourses from other sources – for example doing PPI, or even some seed based analyses.
      
Why are you releasing your code?
--------------------------------
For a number of reasons.
    #.    I want people to use it!  I think if it were easier for people to do time delay analysis, they’d be more likely to do it.  I don’t have enough time or people in my group to do every experiment that I think would be interesting, so I’m hoping other people will, so I can read their papers and learn interesting things.
      
    #.    It’s the right way to do science – I can say lots of things, but if nobody can replicate my results, nobody will believe it (we’ve gotten that a lot, because some of the implications of what we’ve seen in resting state data can be a little uncomfortable).  We’ve reached a stage in fMRI where getting from data to results involves a huge amount of processing, so part of confirming results involves being able to see how the data were processed. If you had to do everything from scratch, you’d never even try to confirm anybody’s results.
      
    #.    In any complicated processing scheme, it’s quite possible (or in my case, likely) to make dumb mistakes, either coding errors or conceptual errors, and I almost certainly have made some (although hopefully the worst ones have been dealt with at this point).  More users and more eyes on the code make it more likely that they will be found.  As much as I’m queasy about somebody potentially finding a mistake in my code, I’d rather that they did so, so I can fix it[‡].
      
    #.    It’s giving back to the community.  I benefit from the generosity of a lot of authors who have made the open source tools I use for work and play, so I figure I can pony up too.
      
Python version compatibility: 
-----------------------------
This code has been tested in python 2.7 and 3.5.  I try very hard not to use any version dependant features when I write programs, so it will probably work on any subversion of python 3.  I think there is some weirdness in the python's numerical routines in versions 2.6 and below, so no guarantees it will work in anythin lower than 2.7.
      
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
    
Usage:
^^^^^^

	::

		capfromtcs - calculate and cluster coactivation patterns for a set of timecourses

		usage: capfromtcs -i timecoursefile -o outputfile --samplefreq=FREQ --sampletime=TSTEP
                  		[--nodetrend] [-s STARTTIME] [-D DURATION]
                  		[-F LOWERFREQ,UPPERFREQ[,LOWERSTOP,UPPERSTOP]] [-V] [-L] [-R] [-C]
                  		[-m] [-n NUMCLUSTER] [-b BATCHSIZE] [-S SEGMENTSIZE] [-I INITIALIZATIONS]
                  		[--nonorm] [--pctnorm] [--varnorm] [--stdnorm] [--ppnorm]
		
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
    		-b BATCHSIZE                 - use a batchsize of BATCHSIZE if doing MiniBatch - ignored if not.  Default is 100
    		-S SEGMENTSIZE               - treat the timecourses as segments of length SEGMENTSIZE for preprocessing.
                                   		Default segmentsize is the entire length
    		-I INITIALIZATIONS           - Restart KMeans INITIALIZATIONS times to find best fit (default is 1000)
    		--nonorm                     - don't normalize timecourses
    		--pctnorm                    - scale each timecourse to it's percentage of the mean
    		--varnorm                    - scale each timecourse to have a variance of 1.0
    		--stdnorm                    - scale each timecourse to have a standard deviation of 1.0 (default)
    		--ppnorm                     - scale each timecourse to have a peak to peak range of 1.0

        
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


rapidtide2std
-------------

Description:
^^^^^^^^^^^^

	This is a utility for registering rapidtide output maps
	to standard coordinates.  It's usually much faster to run rapidtide
	in native space then transform afterwards to MNI152 space.  NB: this 
	will only work if you have a working FSL installation.

Inputs:
^^^^^^^

Outputs:
^^^^^^^^
	New versions of the rapidtide output maps, registered to either MNI152 space or to the hires anatomic images for the subject.  All maps are named with the specified root name with '_std' appended.

Usage:
^^^^^^

	::

		usage: rapidtide2std INPUTFILEROOT OUTPUTDIR FEATDIRECTORY [--all] [--hires]

		required arguments:
			INPUTFILEROOT      - The base name of the rapidtide maps up to but not including the underscore
			OUTPUTDIR          - The location for the output files
			FEADDIRECTORY      - A feat directory (x.feat) where registration to standard space has been performed

		optional arguments:
			--all              - also transform the corrout file (warning - file may be huge)
			--hires            - transform to match the high resolution anatomic image rather than the standard
			--linear           - only do linear transformation, even if warpfile exists


showtc
------

Description:
^^^^^^^^^^^^
	A very simple command line utility that takes a text file
	and plots the data in it in a matplotlib window.  That's it.  A
	good tool for quickly seeing what's in a file.  Has some options
	to make the plot prettier.

Inputs:
^^^^^^^
	Text files containing time series data

Outputs:
^^^^^^^^
	None

Usage:
^^^^^^

	::

		showtc - plots the data in text files

		usage: showtc texfilename [textfilename]... [--nolegend] [--pspec] [--phase] [--samplerate] [--sampletime]

		required arguments:
			textfilename	- a text file containing whitespace separated timecourses, one timepoint per line

		optional arguments:
			--nolegend               - turn off legend label
			--pspec                  - show the power spectra magnitudes of the input data instead of the timecourses
			--phase                  - show the power spectra phases of the input data instead of the timecourses
			--samplerate             - the sample rate of the input data (default is 1Hz)
			--sampletime             - the sample time (1/samplerate) of the input data (default is 1s)


histnifti
--------

Description:
^^^^^^^^^^^^
	A command line tool to generate a histogram for a nifti file


Inputs:
^^^^^^^
	A nifti file

Outputs:
^^^^^^^^
	A text file containing the histogram information

None

Usage:
^^^^^^

	::

		usage: histnifti inputfile outputroot

		required arguments:
			inputfile	- the name of the input nifti file
			outputroot	- the root of the output nifti names



showhist
--------

Description:
^^^^^^^^^^^^
	Another simple command line utility that displays the histograms generated by rapidtide2.

Inputs:
^^^^^^^
	A textfile generated by rapidtide2 containing histogram information

Outputs:
^^^^^^^^
	None

Usage:
^^^^^^

	::

		usage: showhist textfilename
			plots xy histogram data in text file

		required arguments:
			textfilename	- a text file containing one timepoint per line


resamp1tc
---------

Description:
^^^^^^^^^^^^
	This takes an input text file at some sample rate and outputs a text file resampled to the specified sample rate.


Inputs:
^^^^^^^

Outputs:
^^^^^^^^

Usage:
^^^^^^

	::

		resamp1tc - resample a timeseries file

		usage: resamp1tc infilename insamplerate outputfile outsamplerate [-s]

		required arguments:
			inputfile        - the name of the input text file
			insamplerate     - the sample rate of the input file in Hz
			outputfile       - the name of the output text file
			outsamplerate    - the sample rate of the output file in Hz

		 options:
			-s               - split output data into physiological bands (LFO, respiratory, cardiac)


resamplenifti
-------------

Description:
^^^^^^^^^^^^
	This takes an input nifti file at some TR and outputs a nifti file resampled to the specified TR.
 

Inputs:
^^^^^^^

Outputs:
^^^^^^^^

Usage:
^^^^^^

	::

		usage: resamplenifti inputfile inputtr outputname outputtr [-a]

		required arguments:
			inputfile	- the name of the input nifti file
			inputtr		- the tr of the input file in seconds
			outputfile	- the name of the output nifti file
			outputtr	- the tr of the output file in seconds

		options:
			-a		- disable antialiasing filter (only relevant if you are downsampling in time)


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

