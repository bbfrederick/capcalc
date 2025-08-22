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
import getopt

from pylab import *
from sklearn.cluster import KMeans, MiniBatchKMeans

import capcalc.io as ccalc_io


def usage():
    print("usage: kmeans inputfile outputroot [-m] [-n NUMCLUSTER]")
    print("")
    print("required arguments:")
    print("    inputfile        - the name of the input nifti file")
    print("    outputroot       - the root of the output nifti names")
    print("")
    print("optional arguments:")
    print(
        "     -m              - run MiniBatch Kmeans rather than conventional - use with very large datasets"
    )
    print("     -n NUMCLUSTER   - set the number of clusters to NUMCLUSTER (default is 8)")
    print(
        "     -b BATCHSIZE    - use a batchsize of BATCHSIZE if doing MiniBatch - ignored if not.  Default is 100"
    )
    print("")
    return ()


def progressbar(thisval, end_val, label="Percent", barsize=60):
    percent = float(thisval) / end_val
    hashes = "#" * int(round(percent * barsize))
    spaces = " " * (barsize - len(hashes))
    sys.stdout.write("\r{0}: [{1}] {2:.3f}%".format(label, hashes + spaces, 100.0 * percent))
    sys.stdout.flush()


def main():
    # set default variable values
    minibatch = False
    histlen = 101
    n_clusters = 8
    batch_size = 100
    thepercentiles = [0.95, 0.99, 0.995, 0.999]

    # get the command line parameters
    if len(sys.argv) < 3:
        usage()
        exit()

    # handle required args first
    inputfilename = sys.argv[1]
    outputroot = sys.argv[2]

    # now scan for optional arguments
    try:
        opts, args = getopt.getopt(sys.argv[3:], "mn:b:", ["help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -x not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == "-m":
            minibatch = True
            print("will perform MiniBatchKMeans")
        elif o == "-b":
            batch_size = int(a)
            print("will use", batch_size, "as batch_size (if doing MiniBatchKMeans)")
        elif o == "-n":
            n_clusters = int(a)
            print("will use", n_clusters, "clusters")
        else:
            assert False, "unhandled option"

    print("loading data")
    input_img, input_data, input_hdr, thedims, thesizes = ccalc_io.readfromnifti(inputfilename)
    tr = thesizes[4]
    Fs = 1.0 / tr
    print("tr from header =", tr, ", sample frequency is ", Fs)

    xsize = thedims[1]
    ysize = thedims[2]
    numslices = thedims[3]
    numtrials = thedims[4]

    numspatiallocs = int(xsize) * int(ysize) * int(numslices)
    corr_data = input_data.reshape((numspatiallocs, numtrials))
    print("corr_data shape:", corr_data.shape)

    print("calculating kmeans")
    if minibatch:
        kmeans = MiniBatchKMeans(n_clusters=n_clusters, batch_size=batch_size).fit(
            np.nan_to_num(np.transpose(corr_data))
        )
    else:
        kmeans = KMeans(n_clusters=n_clusters).fit(np.nan_to_num(np.transpose(corr_data)))

    theheader = input_hdr
    theheader["dim"][4] = n_clusters
    theclusters = np.transpose(kmeans.cluster_centers_)
    print("clusters shape:", theclusters.shape)
    ccalc_io.savetonifti(
        theclusters.reshape((xsize, ysize, numslices, n_clusters)),
        theheader,
        outputroot + "_states",
    )

    ccalc_io.writenpvecs(kmeans.labels_, outputroot + "_statelabels.txt")


def entrypoint():
    main()


if __name__ == "__main__":
    entrypoint()
