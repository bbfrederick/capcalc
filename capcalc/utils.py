#!/usr/bin/env python
#
#   Copyright 2016-2019 Blaise Frederick
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
#       $Author: frederic $
#       $Date: 2016/06/14 12:04:51 $
#       $Id: showstxcorr,v 1.11 2016/06/14 12:04:51 frederic Exp $
#
from __future__ import division, print_function

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics


def statefilter(thestates, minlength, minhold, debug=False):
    print("state filtering with length", minlength)
    thefiltstates = np.zeros((len(thestates)), dtype=int)
    thefiltstates[0] = thestates[0]
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
    if debug:
        for state in range(len(thestates)):
            print(state, thestates[state], thefiltstates[state])
    return thefiltstates


def statestats(thestates, numlabels, minlabel, minout=1, minhold=1, debug=False):
    # returns statestats and transmat
    #
    # statestats file columns:
    #     percentage of TRs in state
    #     number of continuous runs in state
    #     total number of TRs in state
    #     minimum number of TRs in state
    #     maximum number of TRs in state
    #     average number of TRs in state
    #     median number of TRs in state
    #     standard deviation of the number of TRs in state
    #
    # transmat contains an n_states by n_states matrix:
    #     the number of transitions from state a to state b is in location [a, b]
    #
    minlabel = minlabel
    maxlabel = minlabel + numlabels - 1
    numlabels = maxlabel - minlabel + 1
    transmat = np.zeros((numlabels, numlabels), dtype="float")

    # prefilter
    thestates = statefilter(thestates, minout, minhold, debug=debug)

    # now tabulate states
    currentstate = thestates[0]
    currentlen = 1
    lenlist = [[]]
    for i in range(numlabels - 1):
        lenlist.append([])
    for state in range(1, len(thestates)):
        if thestates[state] == currentstate:
            currentlen += 1
        else:
            lenlist[currentstate - minlabel].append(currentlen)
            currentstate = thestates[state]
            currentlen = 1
        sourcestate = thestates[state - 1] - minlabel
        deststate = thestates[state] - minlabel
        transmat[sourcestate, deststate] += 1.0

    # for debugging - remove!
    # for i in range(numlabels):
    #    transmat[0, i] = i

    lenlist[currentstate - minlabel].append(currentlen)
    thestats = []
    for i in range(numlabels):
        lenarray = np.asarray(lenlist[i], dtype="float")
        if len(lenarray) > 2:
            thestats.append(
                [
                    100.0 * np.sum(lenarray) / len(thestates),
                    len(lenarray),
                    np.sum(lenarray),
                    np.min(lenarray),
                    np.max(lenarray),
                    np.mean(lenarray),
                    np.median(lenarray),
                    np.std(lenarray),
                ]
            )
        elif len(lenarray) > 1:
            thestats.append(
                [
                    100.0 * np.sum(lenarray) / len(thestates),
                    len(lenarray),
                    np.sum(lenarray),
                    np.min(lenarray),
                    np.max(lenarray),
                    np.mean(lenarray),
                    lenarray[1],
                    0.0,
                ]
            )
        elif len(lenarray) > 0:
            thestats.append(
                [
                    100.0 * np.sum(lenarray) / len(thestates),
                    len(lenarray),
                    np.sum(lenarray),
                    lenarray[0],
                    lenarray[0],
                    lenarray[0],
                    lenarray[0],
                    0.0,
                ]
            )
        else:
            thestats.append([0.0, len(lenarray), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    return transmat, np.asarray(thestats, dtype="float"), lenlist


def silhouette_test(X, kmeans, n_clusters, numsegs, segsize, summaryonly, display=False):
    print("generating cluster labels")
    cluster_labels = kmeans.predict(X)
    thesilavgs = np.zeros(numsegs, dtype="float")
    thesilclusterstats = np.zeros((numsegs, 4, n_clusters), dtype="float")
    print("calculating silhouette stats")
    for segment in range(numsegs):
        seg_X = X[segment * segsize : (segment + 1) * segsize]
        seg_cluster_labels = cluster_labels[segment * segsize : (segment + 1) * segsize]
        # do a quick sanity check to see if all the labels are present
        clusternums = np.zeros(n_clusters, dtype="int")
        for i in range(len(seg_cluster_labels)):
            clusternums[seg_cluster_labels[i]] += 1
        if np.min(clusternums) > 0:
            thesilavgs[segment] = metrics.silhouette_score(seg_X, seg_cluster_labels)
            print(
                "average silhouette score for segment",
                segment,
                "=",
                thesilavgs[segment],
            )

            if not summaryonly:
                print("doing silhouette samples")
                sample_silhouette_values = metrics.silhouette_samples(seg_X, seg_cluster_labels)
                if display:
                    # Create a subplot with 1 row and 2 columns
                    fig, (ax1) = plt.subplots(1, 1)
                    fig.set_size_inches(8, 4.5)

                    # The 1st subplot is the silhouette plot
                    # The silhouette coefficient can range from -1, 1 but in this example all
                    # lie within [-0.3, 1]
                    ax1.set_xlim([-0.3, 1])
                    # The (n_clusters+1)*10 is for inserting blank space between silhouette
                    # plots of individual clusters, to demarcate them clearly.
                    ax1.set_ylim([0, len(seg_X) + (n_clusters + 1) * 10])

                    y_lower = 10
                for i in range(n_clusters):
                    # Aggregate the silhouette scores for samples belonging to
                    # cluster i, and sort them
                    ith_cluster_silhouette_values = sample_silhouette_values[
                        seg_cluster_labels == i
                    ]

                    ith_cluster_silhouette_values.sort()
                    thesilclusterstats[segment, 0, i] = np.mean(ith_cluster_silhouette_values)
                    thesilclusterstats[segment, 1, i] = np.median(ith_cluster_silhouette_values)
                    thesilclusterstats[segment, 2, i] = ith_cluster_silhouette_values[0]
                    thesilclusterstats[segment, 3, i] = ith_cluster_silhouette_values[-1]

                    size_cluster_i = ith_cluster_silhouette_values.shape[0]

                    if display:
                        y_upper = y_lower + size_cluster_i
                        color = cm.spectral(float(i) / n_clusters)
                        ax1.fill_betweenx(
                            np.arange(y_lower, y_upper),
                            0,
                            ith_cluster_silhouette_values,
                            facecolor=color,
                            edgecolor=color,
                            alpha=0.7,
                        )

                        # Label the silhouette plots with their cluster numbers at the middle
                        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

                        # Compute the new y_lower for next plot
                        y_lower = y_upper + 10  # 10 for the 0 samples

                if display:
                    ax1.set_title("The silhouette plot for the various clusters.")
                    ax1.set_xlabel("The silhouette coefficient values")
                    ax1.set_ylabel("Cluster label")

                    # The vertical line for average silhouette score of all the values
                    ax1.axvline(x=thesilavgs[segment], color="red", linestyle="--")

                    ax1.set_yticks([])  # Clear the yaxis labels / ticks
                    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
                    plt.suptitle(
                        (
                            "Silhouette analysis for KMeans clustering on sample data "
                            "with n_clusters = %d" % n_clusters
                        ),
                        fontsize=14,
                        fontweight="bold",
                    )

                    plt.show()
        else:
            print("states are not fully populated - skipping stats")
    return thesilavgs, thesilclusterstats
