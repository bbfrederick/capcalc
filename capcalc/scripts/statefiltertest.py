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
import numpy as np
import pylab as plt


def statefilter(thestates, minlength, minhold, debug=False):
    print("state filtering with length", minlength)
    thefiltstates = np.zeros((len(thestates)), dtype=int)
    currentstate = thestates[0]
    laststate = currentstate + 0
    currentlen = 1
    lastlen = 1
    for state in range(1, len(thestates)):
        if thestates[state] == currentstate:
            currentlen += 1
            thefiltstates[state] = thestates[state]
            if debug:
                print("state", state, "(", thestates[state], "):continue")
        else:
            if (currentlen < minlength) and (thestates[state] == laststate):
                thefiltstates[state - currentlen : state + 1] = laststate
                currentstate = laststate + 0
                currentlen += lastlen
                if debug:
                    print("state", state, "(", thestates[state], "):patch")
            elif (currentlen < minhold) and (thestates[state] != laststate):
                thefiltstates[state - currentlen : state + 1] = laststate
                currentstate = laststate + 0
                currentlen += lastlen
                if debug:
                    print("state", state, "(", thestates[state], "):fill")
            else:
                lastlen = currentlen + 1
                currentlen = 1
                laststate = currentstate + 0
                currentstate = thestates[state]
                thefiltstates[state] = thestates[state]
                if debug:
                    print("state", state, "(", thestates[state], "):switch")
            """else:
                lastlen = currentlen + 1
                currentlen = 1
                laststate = currentstate + 0
                currentstate = thestates[state]
                thefiltstates[state] = thestates[state]
                if debug:
                    print('state', state, '(', thestates[state], '):shortswitch')
            """
    return thefiltstates


def main():
    thestates = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2, 1, 2, 0, 1, 1, 1, 1, 2, 2, 1, 1, 1])

    thefiltstates = statefilter(thestates, 2, 2, debug=1)
    plt.plot(thestates)
    plt.plot(thefiltstates + 1)
    plt.show()


def entrypoint():
    main()


if __name__ == "__main__":
    entrypoint()
