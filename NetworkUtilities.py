""" Partition Handler class. Creates and manages graph partitioning.

    Michael A. Goodrich
    Brigham Young University
    July 2022 for CS 575.
    Updated March 2023 to interface with Graph Data Science
"""

from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
from ComputeAndPlotDendrogram import *
from scipy.cluster.hierarchy import dendrogram
import community as community_louvain
from networkx.algorithms.community.centrality import girvan_newman

class networkHandler:
    def __init__(self,G):
        self.G = G
        self.color_map = ['y' for node in self.G]
        self.pos = nx.nx_agraph.graphviz_layout(self.G,prog='neato')
        self.title = 'Network with' + str(len(self.G.nodes)) + ' agents'
        self.color_template = [v for k,v in mcolors.TABLEAU_COLORS.items()]
        # For other color palettes see https://matplotlib.org/stable/gallery/color/named_colors.html 

    """ Public Methods"""
    def showDendrogram(self,figureNumber = 1,wait_for_button = False):
        ##### Don't run this for large graphs. 
        ##### The partitioning is done using Girvan-Newman
        myHandler = DendrogramHandler(self.G)
        Z = myHandler.getLinkMatrix()
        ZLabels = myHandler.getLinkMatrixLabels()
        plt.figure(figureNumber);plt.clf()
        #dendrogram(Z, labels=ZLabels)
        dendrogram(Z)
        if wait_for_button == True: plt.waitforbuttonpress()
        else: plt.waitforbuttonpress(0.001)
        del myHandler
    
    
    """" Public community detection algorithms """
    def getAgentColors_from_LouvainCommunities(self):
        """ Use the Louvain partition method to break the graph into communities """
        # Louvain method pip install python-louvain
        # see https://arxiv.org/pdf/0803.0476.pdf
        # see https://github.com/taynaud/python-louvain
        color_map_dict = dict()
        partition = community_louvain.best_partition(self.G)
        #print(type(partition))
        for node in partition.keys():
            val = partition.get(node)
            color_map_dict[node] = self.color_template[val%len(self.color_template)]
        color_map = []
        for node in self.G:
            color_map.append(color_map_dict[node])
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
    
    