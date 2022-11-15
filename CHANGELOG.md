# Release history

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


