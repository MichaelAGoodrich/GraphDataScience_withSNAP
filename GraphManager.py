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
    def __init__(self):
        self.G = nx.empty_graph(create_using=nx.DiGraph)
    def addNodes(self,node_set):
        self.G.add_nodes_from(node_set)
    def addEdges(self,edge_set):
        self.G.add_edges_from(edge_set)
    def showPlot(self,with_labels = False):
        plt.figure(1); plt.clf(); plt.ion()
        pos = nx.nx_agraph.graphviz_layout(self.G,prog='neato')
        if with_labels:
            nx.draw(self.G,pos,node_color = 'y', alpha = 0.8, node_size = 700, with_labels = True)
        else:
            nx.draw(self.G,pos,node_color = 'y', alpha = 0.8, node_size = 100)
        plt.show()