#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#
#   Copyright 2019-2025 Blaise Frederick
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#
# For converting Python 2 pickles to Python 3
import argparse
import os

import joblib
from sklearn.externals import joblib as scikitjoblib


def convert(joblib_name):
    """
    update a joblib file
    """
    # load the original joblib file
    themodel = scikitjoblib.load(joblib_name)

    # find the name of the output file
    newjoblib_name = os.path.splitext(os.path.basename(joblib_name))[0] + ".newjoblib"
    print("new joblibname", newjoblib_name)

    # save the model as a json
    joblib.dump(themodel, newjoblib_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a save file from joblib to json")

    parser.add_argument("infile", help="joblib file name")

    args = parser.parse_args()

    convert(args.infile)
