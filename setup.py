#!/bin/env python
"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import subprocess, re
import sys


GITTAG_PY = """
# This file is originally generated from Git information by running 'setup.py
# install'. Distribution tarballs contain a pre-generated copy of this file.
__gittag__ = '%s'
"""

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

script_list = ['capcalc/scripts/kmeans',
               'capcalc/scripts/capfromtcs',
               'capcalc/scripts/statematch',
               'capcalc/scripts/roidecompose',
               'capcalc/scripts/clusternifti',
               'capcalc/scripts/supercluster',
               'capcalc/scripts/maptoroi',
               'capcalc/scripts/fitglm',
               'capcalc/scripts/tcfrom3col',
               'capcalc/scripts/normtcs']

def update_gittag_py():
    if not path.isdir(".git"):
        print("This does not appear to be a Git repository.")
        f = open("capcalc/_gittag.py", "w")
        f.write(GITTAG_PY % "UNKNOWN-UNKNOWN")
        f.close()
        return
    try:
        p = subprocess.Popen(["git", "describe",
                              "--tags", "--dirty", "--always"],
                             stdout=subprocess.PIPE)
    except EnvironmentError:
        print("unable to run git, leaving capcalc/_gittag.py alone")
        return
    stdout = p.communicate()[0]
    if p.returncode != 0:
        print("unable to run git, leaving capcalc/_gittag.py alone")
        return
    # we use tags like "python-capcalc-0.5", so strip the prefix
    if sys.version_info[0] == 3:
        ver = str(stdout.strip(), "utf-8")
    else:
        ver = stdout.strip()
    print(ver)
    f = open("capcalc/_gittag.py", "w")
    f.write(GITTAG_PY % ver)
    f.close()


update_gittag_py()


setup(
    name='capcalc',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0.0',

    description='Tools for performing correlation analysis on fMRI data.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/bbfrederick/capcalc',

    # Author details
    author="Blaise Frederick",
    author_email="bbfrederick@mclean.harvard.edu",

    # Choose your license
    license='Apache Software License',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords=['fMRI', 
        'correlation',
        'clustering',
        'states'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    #packages=['capcalc'],

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],
    #py_modules=modules_list,

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['numpy', 'scipy', 'scikit-learn', 'matplotlib', 'statsmodels'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'jit': ['numba'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    include_package_data = False,
    zip_safe=False,
    package_data={
        'reference': ['reference/*.nii.gz'],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    scripts=script_list,
)
