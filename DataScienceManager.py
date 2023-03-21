""" Data Science Manager 
    Run a series of graph database queries to gather information
    about the database.

    Michael A. Goodrich
    CS 575
    Brigham Young University

    March 2023
"""

from GraphDatabaseManager import GraphManager


class DataScienceManager:
    def __init__(self,file_name):
        self.graphDatabase = GraphManager(file_name)
        self.figure_number = 1
    ###########################
    # Visualization Utilities #
    ###########################
    def ShowUnifiedGraph(self,pause=True):
        title = "Relationships with Movies"
        self.graphDatabase.plotGraphDatabase(title = title, figure_number = self.figure_number,wait_for_button=False)
        self.figure_number +=1
        if pause:
            self.graphDatabase.pause()
    
    def ShowAllBipartiteGraphs(self,pause=True):
        for category_1 in {'genre','writers','directors','casts'}:
            title = "Links between " + category_1 + " and movie"
            edge_set = self.graphDatabase.extractBipartiteGraph(category_1,'rank')
            self.graphDatabase.plotSubgraph(edge_set,title = title, figure_number = self.figure_number,with_labels=False)
            self.figure_number +=1
        if pause:
            self.graphDatabase.pause()
    def ShowBipartiteSubgraph(self,category,pause=True):
        #for category in {'genre','writers','directors','casts'}:
        title = "Links between " + category + " and movie"
        bipartite_graph = self.graphDatabase.extractBipartiteGraph(category,'rank')
        self.graphDatabase.plotSubgraph(bipartite_graph,title = title, figure_number = self.figure_number,with_labels=False)
        self.figure_number +=1
        if pause:
            self.graphDatabase.pause()
    def ShowProjection(self,categories,biggest_component = True, save_subgraph = False, pause=True):
        projection_graph = self.graphDatabase.extractProjectionGraph(categories)
        title = "Relationships between movie " + str(categories)
        if biggest_component:
            title = "Largest component of\n" + title
            projection_graph = self.graphDatabase.extractLargestComponent(projection_graph)
        self.graphDatabase.plotSubgraph(projection_graph,title=title,figure_number = self.figure_number)
        self.figure_number +=1
        if save_subgraph:
            self.graphDatabase.exportSubgraphToGephi(projection_graph,'filename')
        if pause:
            self.graphDatabase.pause()

    