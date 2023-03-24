""" Represents the database as a graph.
    Construct the graph database
    Utilities for viewing graphs and subgraphs.
    Utilities for performing projections.   

    Michael A. Goodrich
    Brigham Young University

    March 2023
"""
import networkx as nx
from matplotlib import pyplot as plt

from DatabaseManager import DatabaseManager


class GraphManager:
    def __init__(self,file_name,directed_graph = False):
        self.database = DatabaseManager(file_name)
        if directed_graph:
            self.G = nx.empty_graph(create_using=nx.DiGraph)
        else: self.G = nx.empty_graph()
        self.nodes_by_attribute_dict = dict()
        self.__initalizeGraph()
        self.colormap = ['y' for node in self.G.nodes]
        
    ############################################
    # Public Extraction and Projection Methods #
    ############################################
    def extractBipartiteGraph(self,category_1,category_2):
        edge_set = self.database.getEdges(category_1,category_2)
        H = self.__edgesetToSubgraph(edge_set)
        return H
    def extractProjectionGraph(self,categories):
        """ Project out the movie to see relationships
            between other database categories
        """
        edge_set = self.__extractProjectionEdges(categories)
        H = self.__edgesetToSubgraph(edge_set)
        return H
    def extractLargestComponent(self,subgraph):
        largest_cc = max(nx.connected_components(subgraph),key=len)
        subgraph = subgraph.subgraph(largest_cc).copy()
        return subgraph

    #############################
    # Public Plotting Methods   #
    #############################
    def plotGraphDatabase(self,title = "Network", figure_number = 1, with_labels = False):
        """ Only use for small databases.
            For large databases, export to .gexf
            and view using GEPHI
        """
        plt.figure(figure_number); plt.clf(); plt.ion()
        ax = plt.gca();ax.set_title(title)
        pos = nx.nx_agraph.graphviz_layout(self.G,prog='neato')
        if with_labels:
            nx.draw(self.G,pos,node_color = self.colormap, alpha = 0.8, node_size = 700, with_labels = True)
        else:
            nx.draw(self.G,pos,node_color = self.colormap, alpha = 0.8, node_size = 30)
        plt.show()                           
    def plotSubgraph(self, subgraph, colormap = 'y', title = "Network", figure_number = 1, with_labels = False):
        plt.figure(figure_number); plt.clf(); plt.ion()
        ax = plt.gca();ax.set_title(title)
        pos = nx.nx_agraph.graphviz_layout(subgraph,prog='neato')
        if with_labels:
            nx.draw(subgraph,pos,node_color = colormap, alpha = 0.8, node_size = 700, with_labels = True)
        else:
            nx.draw(subgraph,pos,node_color = colormap, alpha = 0.8, node_size = 30)
        plt.show()        
       
        return subgraph
    def pause(self):
        plt.waitforbuttonpress()

    ##################################
    # Miscellaneous Public Utilities #
    ##################################
    def exportToGephi(self,gephi_filename):
        #nx.write_gexf(G,gephi_filename)
        nx.write_gexf(self.G,"/Users/mike/Dropbox/Mac/Documents/Classes/CS 575/Winter 2023/Code/GraphDataScience_withSNAP/figures/MoviePersonnelGraph.gexf")   
    def exportSubgraphToGephi(self,H,gephi_filename):
        #nx.write_gexf(G,gephi_filename)
        nx.write_gexf(H,"/Users/mike/Dropbox/Mac/Documents/Classes/CS 575/Winter 2023/Code/GraphDataScience_withSNAP/figures/MoviePersonnelGraph.gexf")   
    
    ##########################
    # Private Helper Methods #
    ##########################
    def __initalizeGraph(self):
        # Step 1: Initialize node set
        for category in {'genre','writers','directors','casts','rank'}:
            node_set = self.database.getNodesOfType(category)
            self.__addNodes(node_set,category)
        
        # Step 2: Initialize edge set
        category_2 = 'rank'
        for category_1 in {'genre','writers','directors','casts'}:
            edges = self.database.getEdges(category_1,category_2)
            self.__addEdges(edges)
    def __addNodes(self,node_set,node_type):
        if node_type == 'name': node_type = 'rank'
        self.G.add_nodes_from(node_set)
        self.nodes_by_attribute_dict[node_type] = node_set
    def __addEdges(self,edge_set):
        self.G.add_edges_from(edge_set)
    def __edgesetToSubgraph(self,edge_set):
        H = nx.empty_graph()
        for edge in edge_set:
            H.add_edge(edge[0],edge[1])
        return H
    def __extractProjectionEdges(self,categories):
        """ Project out the movie to see relationships
            between other database categories
        """
        # The projections is performed by finding all paths two steps or fewer
        two_step_paths = dict(nx.all_pairs_shortest_path_length(self.G,cutoff=2))
        node_set = set()
        # Extract all the node types of interest
        for node_type in categories:
            node_set = node_set.union(self.database.getNodesOfType(node_type))
        # Select only two step paths between nodes of interest
        edge_set = set()
        for node_source in node_set:
            destination_dictionary = two_step_paths[node_source]
            node_destinations = set([k for k,v in destination_dictionary.items() if v == 2])
            node_destinations = node_destinations.intersection(node_set)
            for node_destination in node_destinations:
                edge_set.add((node_source,node_destination))
        return edge_set
