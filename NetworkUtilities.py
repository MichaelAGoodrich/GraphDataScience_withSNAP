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
        self.color_map = ['y' for node in list(self.G.nodes)]
        self.pos = nx.nx_agraph.graphviz_layout(self.G,prog='neato')
        self.title = 'Network with' + str(len(self.G.nodes)) + ' agents'
        self.color_template = [v for k,v in mcolors.TABLEAU_COLORS.items()]
        self.figure_number = 1
        # For other color palettes see https://matplotlib.org/stable/gallery/color/named_colors.html 

    ###########################
    # Public Plotting Methods #
    ###########################
    def showNetwork(self, colormap = None, title = "Network", with_labels = False, pause = False):
        if colormap is None: colormap = self.color_map
        plt.figure(self.figure_number);plt.clf();plt.ion();self.figure_number += 1
        ax = plt.gca();ax.set_title(title)
        if with_labels:
            nx.draw(self.G,self.pos,node_color = colormap, alpha = 0.8, node_size = 700, with_labels = True)
        else:
            nx.draw(self.G,self.pos,node_color = colormap, alpha = 0.8, node_size = 30)
        if pause: plt.waitforbuttonpress()
        else: plt.show()     
    def showDendrogram(self,wait_for_button = False):
        ##### Don't run this for large graphs. 
        ##### The partitioning is done using Girvan-Newman
        myHandler = DendrogramHandler(self.G)
        Z = myHandler.getLinkMatrix()
        plt.figure(self.figure_number);plt.clf();self.figure_number += 1
        #ZLabels = myHandler.getLinkMatrixLabels()
        #dendrogram(Z, labels=ZLabels)
        dendrogram(Z)
        if wait_for_button == True: plt.waitforbuttonpress()
        else: plt.show()
        del myHandler
    def showSubgraph(self,subgraph):
        """ plot the subgraph of self.G, but use the positions
            colormap from self.
        """
        if set(subgraph.nodes()).issubset(set(self.G.nodes())) or set(subgraph.edges()).issubset(set(self.G.nodes())):
            raise ValueError
        subgraph_nodes = set(subgraph.nodes)
        pos_dict = dict()
        color_map = []
        for node_index in range(len(self.G.nodes)):
            node = self.G[node_index]
            if node in subgraph_nodes:
                pos_dict[node] = self.pos[node]
                color_map.append(self.color_map[node_index])
        nx.draw(subgraph,pos=pos_dict,node_color = color_map, alpha = 0.7, node_size = 30)
        plt.show()
            

        

    ##############################
    # Pubioc Getters and Setters #
    ##############################
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
        communities = self.__getCommunityWith_N_Partitions(comp,numPartitions)
        color_map = self.__getColorMapFromCommunities(communities)
        return color_map, communities
    def getKCoreSubgraph(self):
        H = nx.k_core(self.G) # when no value for k is given, the main core is returned
        return H
    def setAgentColors(self,colormap): self.color_map = colormap
    #############################
    # Under implemented Methods #
    #############################
    def getNetworkStatistics(self):
        # You should use this method to gather the network statistics
        # that you care about.
        print("Degree assortativity is ",nx.degree_assortativity_coefficient(self.G))
        print("\tA positive sign means the network is assortative,")
        print("\tand a negative sign means the network is disassortative")
        #raise NotImplementedError

    ##################
    # Private Methods #
    ##################
    def __getCommunityWith_N_Partitions(self,all_communities,numPartitions):
        for com in all_communities:
            if len(list(com)) == numPartitions:
                communities = list(com)
                break
        return communities
    def __getColorMapFromCommunities(self,communities):
        color_map = self.color_map
        partition_number = 0
        for partition in communities: 
            #print("***\n",partition)
            for node in partition:
                color_map[node] = self.color_template[partition_number%len(self.color_template)]
            partition_number += 1
        return color_map
    
    