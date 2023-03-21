""" Partition Handler class. Creates and manages graph partitioning.

    Michael A. Goodrich
    Brigham Young University
    July 2022 for CS 575.
    Updated March 2023 to interface with Graph Data Science
"""

from matplotlib import pyplot as plt
import networkx as nx
from ComputeAndPlotDendrogram import *
from scipy.cluster.hierarchy import dendrogram
import community as community_louvain
from networkx.algorithms.community.centrality import girvan_newman

class partitionHandler:
    def __init__(self,G):
        self.G = G
        self.color_map = ['y' for node in self.G]
        self.pos = nx.nx_agraph.graphviz_layout(self.G,prog='neato')
        self.title = 'Network with' + str(len(self.G.nodes)) + ' agents'

        #print(self.G.nodes())
    """ Public Methods"""
    def showDendrogram(self,figureNumber = 1,wait_for_button = False):
        myHandler = DendrogramHandler(self.G)
        Z = myHandler.getLinkMatrix()
        ZLabels = myHandler.getLinkMatrixLabels()
        plt.figure(figureNumber);plt.clf()
        dendrogram(Z, labels=ZLabels)
        if wait_for_button == True: plt.waitforbuttonpress()
        else: plt.waitforbuttonpress(0.001)
        del myHandler
    

    """" Public community detection algorithms """
    def getAgentColors_from_LouvainCommunities(self):
        """ Use the Louvain partition method to break the graph into communities """
        # Louvain method pip install python-louvain
        # see https://arxiv.org/pdf/0803.0476.pdf
        # see https://github.com/taynaud/python-louvain
        color_map = self.color_map
        partition = community_louvain.best_partition(self.G)
        for node in partition:
            val = partition.get(node)
            color_map[node-1] = self.color_template[val%len(self.color_template)]
        return color_map
    def getAgentColors_from_GirvanNewmanCommunities(self,numPartitions = 4):
        """ Use the Girvan Newman betweeness-based algorithm to partition graph """
        # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.centrality.girvan_newman.html#networkx.algorithms.community.centrality.girvan_newman
        comp = girvan_newman(self.G)
        communities = self._getCommunityWith_N_Partitions(comp,numPartitions)
        color_map = self._getColorMapFromCommunities(communities)
        return color_map, communities

    """ Private methods """
    def _getCommunityWith_N_Partitions(self,all_communities,numPartitions):
        for com in all_communities:
            if len(list(com)) == numPartitions:
                communities = list(com)
                break
        return communities
    def _getColorMapFromCommunities(self,communities):
        color_map = self.color_map
        partition_number = 0
        for partition in communities: 
            #print("***\n",partition)
            for node in partition:
                color_map[node] = self.color_template[partition_number%len(self.color_template)]
            partition_number += 1
        return color_map
    def __getAdjacencyMatrix(self):
        """ Return the adjacency matrix for the graph as a sparse scipy matrix """
        return nx.adj_matrix(self.G)
    