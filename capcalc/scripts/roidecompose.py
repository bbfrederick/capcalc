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

import capcalc.io as ccalc_io
import capcalc.miscmath as ccalc_math


def usage():
    print(
        "usage: roidecompose fmrifile templatefile outputfile [--stdnorm] [--pctnorm] [--ppnorm] [--varnorm] [--nonorm]"
    )
    print("")
    print("required arguments:")
    print("    inputfile        - the name of the file with the kmeans cluster centers")
    print("    templatefile     - the name of the template region file")
    print("    outputfile       - the name of the output text file")
    print("")
    print("optional arguments:")
    print("    --nonorm         - don't normalize timecourses (default)")
    print("    --pctnorm        - scale each timecourse to it's percentage of the mean")
    print("    --varnorm        - scale each timecourse to have a variance of 1.0")
    print("    --stdnorm        - scale each timecourse to have a standard deviation of 1.0")
    print("    --ppnorm         - scale each timecourse to have a peak to peak range of 1.0")
    print("")
    return ()


def main():  # get the command line parameters
    if len(sys.argv) < 4:
        usage()
        exit()

    # handle required args first
    inputfilename = sys.argv[1]
    templatefile = sys.argv[2]
    outputfile = sys.argv[3]

    normmethod = "none"

    # now scan for optional arguments
    try:
        opts, args = getopt.getopt(
            sys.argv[4:], "h", ["nonorm", "pctnorm", "varnorm", "stdnorm", "ppnorm", "help"]
        )
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -x not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == "--nonorm":
            normmethod = "none"
        elif o == "--pctnorm":
            normmethod = "pctnorm"
        elif o == "--stdnorm":
            normmethod = "stdnorm"
        elif o == "--varnorm":
            normmethod = "varnorm"
        elif o == "--ppnorm":
            normmethod = "ppnorm"
        elif o == "-h" or o == "--help":
            usage()
            exit()
        else:
            assert False, "unhandled option"

    if normmethod == "none":
        print("will not normalize timecourses")
    elif normmethod == "pctnorm":
        print("will normalize timecourses to percentage of mean")
    elif normmethod == "stdnorm":
        print("will normalize timecourses to standard deviation of 1.0")
    elif normmethod == "varnorm":
        print("will normalize timecourses to variance of 1.0")
    elif normmethod == "ppnorm":
        print("will normalize timecourses to p-p deviation of 1.0")

    print("loading fmri data")
    input_img, input_data, input_hdr, thedims, thesizes = ccalc_io.readfromnifti(inputfilename)
    print("loading template data")
    (
        template_img,
        template_data,
        template_hdr,
        templatedims,
        templatesizes,
    ) = ccalc_io.readfromnifti(templatefile)

    print("checking dimensions")
    if not ccalc_io.checkspacematch(input_hdr, template_hdr):
        print("template file does not match spatial coverage of input fmri file")
        sys.exit()

    print("reshaping")
    xsize = thedims[1]
    ysize = thedims[2]
    numslices = thedims[3]
    numtimepoints = thedims[4]
    numvoxels = int(xsize) * int(ysize) * int(numslices)
    templatevoxels = np.reshape(template_data, numvoxels).astype(int)
    inputvoxels = np.reshape(input_data, (numvoxels, numtimepoints))
    numregions = np.max(templatevoxels)
    timecourses = np.zeros((numregions, numtimepoints), dtype="float")

    if numtimepoints > 1:
        for theregion in range(1, numregions + 1):
            thevoxels = inputvoxels[np.where(templatevoxels == theregion), :]
            print("extracting", thevoxels.shape[1], "voxels from region", theregion)
            if thevoxels.shape[1] > 0:
                regiontimecourse = np.nan_to_num(np.mean(thevoxels, axis=1))
            else:
                regiontimecourse = timecourses[0, :] * 0.0
            if normmethod == "none":
                timecourses[theregion - 1, :] = regiontimecourse - np.mean(regiontimecourse)
            elif normmethod == "pctnorm":
                timecourses[theregion - 1, :] = ccalc_math.pcnormalize(regiontimecourse)
            elif normmethod == "varnorm":
                timecourses[theregion - 1, :] = ccalc_math.varnormalize(regiontimecourse)
            elif normmethod == "stdnorm":
                timecourses[theregion - 1, :] = ccalc_math.stdnormalize(regiontimecourse)
            elif normmethod == "ppnorm":
                timecourses[theregion - 1, :] = ccalc_math.ppnormalize(regiontimecourse)
            else:
                print("illegal normalization method")
                usage()
                sys.exit()
        ccalc_io.writenpvecs(timecourses, outputfile)
    else:
        outputvoxels = np.reshape(input_data, (numvoxels, numtimepoints))
        for theregion in range(1, numregions + 1):
            regionval = np.nan_to_num(np.mean(inputvoxels[np.where(templatevoxels == theregion)]))
            outputvoxels[np.where(templatevoxels == theregion)] = regionval
        template_hdr["dim"][4] = numregions
        ccalc_io.savetonifti(
            outputvoxels.reshape((xsize, ysize, numslices, numregions)),
            template_hdr,
            outputfile,
        )


def entrypoint():
    main()


if __name__ == "__main__":
    entrypoint()
