# Release history

## Version 1.4.0 (11/18/23)
* (Docker) Made compatible with the new (small) basecontainer architecture.

## Version 1.3.9 (4/25/23)
* (package) Removed numba as a dependency.
* (package) Made pyfftw an optional dependency (it's no longer in basecontainer).
* (package) Made some proactive fixes for numpy 2.0.0 compatibility.
* (package) Accepted several dependabot PRs.
* (package) General cleanup of automated workflows to match updates to rapidtide.
* (Docker) Cleaned up and simplified Dockerfile.
* (Docker) Updated to basecontainer:latest-release (0.3.5 atm).

## Version 1.3.8 (12/11/23)
* (Docker) Updated to basecontainer 0.3.0.
* (Docker) Added caching to build.

## Version 1.3.7 (9/13/23)
* Mass merge of a bunch of dependabot PRs.
* (Docker) Updated to basecontainer 0.2.3.

## Version 1.3.6 (5/11/23)
* (Docker) Updated to python 3.11 basecontainer.
* (Docker) Fixed testdocker.sh.
* (package) Modernized install procedure.

## Version 1.3.5 (1/11/23)
* (capfromtcs) Fixed summary statistics outputs.

## Version 1.3.4 (1/10/23)
* (capfromtcs) Revert change to max_iter when specifying initialcenters.

## Version 1.3.3 (1/10/23)
* (capfromtcs) Changed intialization of kmeans from initialcenters, save more intermediate results.
* (utils.py) Factored out some transition array calculations.

## Version 1.3.2 (11/15/22)
* (capfromtcs) Fixed a typo in specifying the initial k-means++ method.
* (io) Updated libraries to match some changes in rapidtide.

## Version 1.3.1 (11/10/22)
* (capfromtcs) Added new option "--initialcenters" to allow specification of k-means cluster centers.  This lets you reuse the CAPS as previous runs, but gets around the difficulty of reading back old models run under a different version of python or scikit-learn.

## Version 1.3.0 (11/10/22)
* (package) Removed rapidtide as a dependency by copying over the necessary support routines.
* (Docker) Updated basecontainer to latest, switched over to using pip rather than mamba for env.
* (docs) Corrected a problem that was causing readthedocs build to fail.

## Version 1.2.3 (8/31/22)
* (capfromtcs, clustercomp) Used newer, non-deprecated method to access nifti files with nibabel.
* (package) Added docker and singularity test scripts.
* (package) Reformatted several files with black.
* (package) Made many (unsuccesful) attempts to get the documentation to build.

## Version 1.2.2.5 (8/30/22)
* (package) Bump to trigger github deployment.

## Version 1.2.2.4 (8/30/22)
* (package) Convert README.md to README.rst

## Version 1.2.2.3 (8/30/22)
* (package) Fixed Development status in setup.py

## Version 1.2.2.2 (8/30/22)
* (package) Syncing with rapidtide to try to get pypi deployment to work

## Version 1.2.2.1 (8/29/22)
* (package) Fixed versioneer installation.

## Version 1.2.2 (8/29/22)
* (package) Updated pyproject.toml and versioneer to try to fix pypi deployment.

## Version 1.2.1 (8/22/22)
* (Docker) Fixed Dockerfile error.
* (package) Updated pypi authentication information.

## Version 1.2.0 (8/22/22)
* (Docker) Added Docker compatibility.
* (package) Updated to match the current version of rapidtide.
* (package) Added "refresh" script to simplify updates.
* (package) Formatting changes.
* (capfromtcs) Fixed import of joblib, updated to new NonCausalFilter calling conventions.
* (clusternifti) Major overhaul.  Added normalization, PCA and ICA dimensionality reduction, switched to argparse, added repeats.
* (clustersort) New program to harmonize multiple cluster solutions.
* (clusternifti, clustersort, supercluster) Harmonized mask specification arguments and internal variable names.

## Version 1.1.0 (8/20/21)
* (package) Move to versioneer.

## Version 1.0.0 (2/15/17)
* First release


