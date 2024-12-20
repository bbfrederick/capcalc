#!/bin/env python
"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# To use a consistent encoding
from codecs import open
from os import path

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

import versioneer

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()


# Write version number out to VERSION file
version = versioneer.get_version()
try:
    with open(path.join(here, "VERSION"), "w", encoding="utf-8") as f:
        f.write(version)
except PermissionError:
    print("can't write to VERSION file - moving on")


modules_list = [
    "capcalc/fit",
    "capcalc/filter",
    "capcalc/io",
    "capcalc/miscmath",
    "capcalc/niftidecomp",
    "capcalc/parser_funcs",
    "capcalc/stats",
    "capcalc/util",
    "capcalc/utils",
    "capcalc/_version",
]


script_list = [
    "capcalc/scripts/behavioralprediction",
    "capcalc/scripts/capcalc_dispatcher",
    "capcalc/scripts/capfromtcs",
    "capcalc/scripts/capfromany",
    "capcalc/scripts/clustercomp",
    "capcalc/scripts/clustersort",
    "capcalc/scripts/clusternifti",
    "capcalc/scripts/fitglm",
    "capcalc/scripts/kmeans",
    "capcalc/scripts/maptoroi",
    "capcalc/scripts/ccspatialdecomp",
    "capcalc/scripts/normtcs",
    "capcalc/scripts/roidecompose",
    "capcalc/scripts/statefiltertest",
    "capcalc/scripts/statematch",
    "capcalc/scripts/statlasgen",
    "capcalc/scripts/supercluster",
    "capcalc/scripts/tcfrom3col",
    "capcalc/scripts/updatemodel",
]


setup(
    name="capcalc",
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Tools for performing coactivation pattern analysis on fMRI data.",
    long_description=long_description,
    # The project's main homepage.
    url="https://github.com/bbfrederick/capcalc",
    # Author details
    author="Blaise Frederick",
    author_email="bbfrederick@mclean.harvard.edu",
    # Choose your license
    license="Apache Software License",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        # Indicate who your project is intended for
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: Apache Software License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    # What does your project relate to?
    keywords=["fMRI", "correlation", "clustering", "states"],
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=["contrib", "docs"]),
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],
    py_modules=modules_list,
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        "numpy",
        "scipy",
        "scikit-learn",
        "matplotlib",
        "statsmodels",
        "nibabel",
        "versioneer",
    ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        "doc": [
            "sphinx>=1.8.0",
            "sphinx_rtd_theme",
            "sphinx-argparse",
            "sphinx-gallery",
            "m2r",
            "numpydoc",
            "recommonmark",
            "mistune==0.8.4",
        ],
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    include_package_data=False,
    zip_safe=False,
    package_data={
        "reference": ["reference/*.nii.gz"],
    },
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    scripts=script_list,
)
