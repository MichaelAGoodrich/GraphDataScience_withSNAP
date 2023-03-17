""" Graph manager tools 

    For use with GraphDataScience_Practice.ipynb

    Michael A. Goodrich
    Brigham Young University

    March 2023
"""
import networkx as nx
import matplotlib as mpl
from matplotlib import pyplot as plt

class GraphManager:
    def __init__(self,directed_graph = False):
        if directed_graph:
            self.G = nx.empty_graph(create_using=nx.DiGraph)
        else: self.G = nx.empty_graph()
        self.nodes_by_attribute_dict = dict()
    def addNodes(self,node_set,node_type):
        if node_type == 'name': node_type = 'rank'
        self.G.add_nodes_from(node_set)
        self.nodes_by_attribute_dict[node_type] = node_set
    def addEdges(self,edge_set):
        self.G.add_edges_from(edge_set)
    def plotSubgraph(self,node_type_1, node_type_2, title = "Network", figure_number = 1, with_labels = False):
        type_1_nodes = self.nodes_by_attribute_dict[node_type_1]
        type_2_nodes = self.nodes_by_attribute_dict[node_type_2]
        H = nx.empty_graph()
        for node_1 in type_1_nodes:
            neighbors = set(self.G.neighbors(str(node_1)))
            for node_2 in type_2_nodes:
                if str(node_2) in neighbors:
                    H.add_edge(str(node_1),str(node_2))
        plt.figure(figure_number); plt.clf(); plt.ion()
        ax = plt.gca();ax.set_title(title)
        pos = nx.nx_agraph.graphviz_layout(H,prog='neato')
        if with_labels:
            nx.draw(H,pos,node_color = 'y', alpha = 0.8, node_size = 700, with_labels = True)
        else:
            nx.draw(H,pos,node_color = 'y', alpha = 0.8, node_size = 30)
        plt.show()
        #print(node_type_1, " node ids: {}".format(type_1_nodes),"\n\n")
    def plotProjection(self,node_types,title = "Network", figure_number = 1, with_labels = False,biggest_component = False):
        two_step_paths = dict(nx.all_pairs_shortest_path_length(self.G,cutoff=2))
        node_set = set()
        for node_type in node_types:
            node_set = node_set.union(self.nodes_by_attribute_dict[node_type])
        node_set = [str(i) for i in node_set]
        H = nx.empty_graph()
        for node_source in node_set:
            H.add_node(node_source)
            destination_dictionary = two_step_paths[node_source]
            node_destinations = set([k for k,v in destination_dictionary.items() if v == 2])
            node_destinations = node_destinations.intersection(node_set)
            for node_destination in node_destinations:
                H.add_edge(node_source,node_destination)
            #print(f"{node_source} can reach {node_destinations}")
        if biggest_component:
            largest_cc = max(nx.connected_components(H),key=len)
            H = H.subgraph(largest_cc).copy()
            title = "Largest component of\n" + title
        
        plt.figure(figure_number); plt.clf(); plt.ion()
        ax = plt.gca();ax.set_title(title)
        pos = nx.nx_agraph.graphviz_layout(H,prog='neato')
        if with_labels:
            nx.draw(H,pos,node_color = 'y', alpha = 0.8, node_size = 700, with_labels = True)
        else:
            nx.draw(H,pos,node_color = 'y', alpha = 0.8, node_size = 30)
        plt.show() 
        nx.write_gexf(H,"/Users/mike/Dropbox/Mac/Documents/Classes/CS 575/Winter 2023/Code/GraphDataScience_withSNAP/figures/MoviePersonnelGraph.gexf")   
            #break

    def showPlot(self,title = "Network", figure_number = 1, with_labels = False):
        plt.figure(figure_number); plt.clf(); plt.ion()
        ax = plt.gca();ax.set_title(title)
        pos = nx.nx_agraph.graphviz_layout(self.G,prog='neato')
        if with_labels:
            nx.draw(self.G,pos,node_color = 'y', alpha = 0.8, node_size = 700, with_labels = True)
        else:
            nx.draw(self.G,pos,node_color = 'y', alpha = 0.8, node_size = 30)
        plt.show()
    def pause(self):
        plt.waitforbuttonpress()