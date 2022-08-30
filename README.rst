Capcalc
=======

capcalc is a suite of python programs used to perform coactivation
pattern analysis on time series data. It uses K-Means clustering to find
a set of “activation states” that represent the covarying patterns in
the data.

HTML documentation is here: http://capcalc.readthedocs.io/en/latest/

NOTE
====

This is an evolving code base. I’m constantly tinkering with it. That
said, now that I’m releasing this to the world, I’m being somewhat more
responsible about locking down stable release points. In between
releases, however, I’ll be messing with things. **It’s very possible I
could break something while doing this, so check back for status updates
if you download the code in between releases**. I’ve finally become a
little more modern and started adding automated testing, so as time goes
by hopefully the “in between” releases will be somewhat more reliable.
Check back often for exciting new features and bug fixes!

Ok, I’m sold. What’s in here?
=============================

-  **roidecompose** - This program uses an atlas to extract timecourses
   from a 4D nifti file, producing a text file with the averaged
   timecourse from each region in the atlas (each integral value in
   file) in each column. This can be input to capfromtcs. There are
   various options for normalizing the timecourses.

-  **capfromtcs** - This does the actual CAP calculation, performing a
   k-means cluster analysis on the set of timecourses to find the best
   representitive set of “states” in the file. Outputs the states found
   and the dominant state in each timepoint of the timecourse.

-  **maptoroi** - The inverse of roidecompose. Give it a set of cluster
   timecourses and a template file, and it maps the values back onto the
   rois

-  **statematch** - Use this for aligning two state output files. Takes
   two state timecourse files, and determines which states in the second
   correspond to which states in the first. Generates a new ‘remapped’
   file with the states in the second file expressed as states in the
   first.
