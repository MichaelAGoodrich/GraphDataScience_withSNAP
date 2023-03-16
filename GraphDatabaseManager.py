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
    def addNodes(self,node_set):
        self.G.add_nodes_from(node_set)
    def addEdges(self,edge_set):
        self.G.add_edges_from(edge_set)
    def showPlot(self,title = "Network", figure_number = 1, with_labels = False, wait_for_button = False):
        plt.figure(figure_number); plt.clf(); plt.ion()
        ax = plt.gca();ax.set_title(title)
        pos = nx.nx_agraph.graphviz_layout(self.G,prog='neato')
        if with_labels:
            nx.draw(self.G,pos,node_color = 'y', alpha = 0.8, node_size = 700, with_labels = True)
        else:
            nx.draw(self.G,pos,node_color = 'y', alpha = 0.8, node_size = 30)
        plt.show()
        if wait_for_button: plt.waitforbuttonpress()
    def pause(self):
        plt.waitforbuttonpress()