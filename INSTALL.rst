Installation
============

Required dependencies
---------------------

capcalc requires some external libraries to be installed first:

-  Python 3.x
-  numpy
-  scipy
-  matplotlib
-  scikit-learn
-  statsmodels
-  nibabel


Installing from pypi
--------------------

I've finally gotten pypi deployment working, so the new easiest way to
install capcalc is to simply type:

::

    pip install capcalc


That's it, I think.


Installing with conda
---------------------

The other simple way to get this all done is to use Anaconda python
from Continuum Analytics. It’s a free, curated scientific Python
distribution that is easy to maintain and takes a lot of headaches out
of maintaining a distribution. It also already comes with almost all of the
dependancies for capcalc installed by default. You can get it here:
https://www.continuum.io. You should download the most recent Python 3 version.

After installing Anaconda python, install the remaining dependency
To do this most easily, you should have
conda-forge as one of your source channels.  To add conda-forge, type:

::

   conda config --add channels conda-forge


Then install the additional dependencies:

::

   conda install pyqtgraph nibabel pillow



Done.

Installing capcalc
----------------------

Once you have installed the prerequisites, cd into the package
directory, and type the following:

::

   python setup.py install


to install all of the tools in the package. You should be able to run
them from the command line then (after rehashing).

Updating
--------

If you’ve previously installed capcalc and want to update, cd into the
package directory and do a git pull first:

::

   git pull
   python setup.py install


Docker installation
===================
There is a Docker container with a full capcalc installation.  To use this, first make
sure you have docker installed and properly configured, then run the following:
::

    docker pull fredericklab/capcalc:VERSIONNUMBER


This it will download the docker container from dockerhub.
It's around 2GB, so it may take some time, but it caches the file locally, so you won't have to do this again
unless the container updates.  To use a particular version, replace VERSIONNUMBER with the version of the
with container you want (currently the newest version is 1.0.0rc2).

If you like to live on the edge, just use:
::

    docker pull fredericklab/capcalc:latest


This will use the most recent version on dockerhub.  

Now that the file is downloaded, you can run any capcalc command in the Docker container.  For example, to run 
capfromtcs itself, you would use the following command (you can do this all in one step - it will just integrate the
first pull into the run time if the version you request hasn't already been downloaded).

Docker runs completely in it's own selfcontained environment.  If you want to be able to interact with disks outside of
container, you map the volume to a mount point in the container using the --volume=EXTERNALDIR:MOUNTPOINT[,ANOTHERDIR:ANOTHERMOUNTPOINT]
option to docker.

One complication of Docker - if you're running a program that displays anything (and we do), 
you'll have to add a few extra arguments to the docker call.  Docker is a little weird about X forwarding - the easiest thing to 
do is find the IP address of the machine you're running on (lets call it MYIPADDRESS), and do the following:

::

    xhost + 

This disables X11 security - this is almost certainly not the best thing to do, but I don't have a better solution
at this time, and it works.

If you're on a Mac using Xquartz, prior to this you'll also have to do three more things.

1) In Xquartz, go into the security preferences, and make sure "Allow connections from network hosts" is checked.
2) Tell Xquartz to listen for TCP connections (this is not the default).  Go to a terminal window and type:

::

    defaults write org.macosforge.xquartz.X11 nolisten_tcp 0

3) Log out and log back in again (you only need to do this once - it will stay that way until you change it.)


Then you should be good to go, with the following command:
::

    docker run \
        --network host\
        --volume=INPUTDIRECTORY:/data_in,OUTPUTDIRECTORY:/data_out \
        -it \
        -e DISPLAY=MYIPADDRESS:0 \
        -u capcalc \
        fredericklab/capcalc:VERSIONNUMBER \
            capfromtcs \
                -i manyfiles.txt \
                -o output/manyfiles \
                --sampletime=0.72 \
                --varnorm \
                -m \
                -b 4800 \
                -S 1200 \
                --quality \
                -E default \
                --minout=2 \
                [otheroptions]

You can replace the capfromtcs blah blah blah command with any other program in the package (currently only "grader", which classifies timecourses) - after the fredericklab/capcalc:latest, 
just specify the command and arguments as you usually would.


Singularity installation
========================

Many times you can't use Docker, because of security concerns.  Singularity, from LBL, offers containerized computing
that runs entirely in user space, so the amount of mischief you can get up to is significantly less.  Singularity
containers can be created from Docker containers as follows (stealing from the fMRIprep documentation):
::

    singularity build /my_images/capcalc-VERSIONNUMBER.simg docker://fredericklab/capcalc:VERSIONNUMBER


Running the container is similar to Docker.  The "-B" option is used to bind filesystems to mountpoints in the container. 

    singularity run \
        --cleanenv \
        -B INPUTDIRECTORY:/data_in,OUTPUTDIRECTORY:/data_out \
        capcalc-VERSIONNUMBER.simg \
            capfromtcs \
                -i manyfiles.txt \
                -o output/manyfiles \
                --sampletime=0.72 \
                --varnorm \
                -m \
                -b 4800 \
                -S 1200 \
                --quality \
                -E default \
                --minout=2 \
                [otheroptions]
