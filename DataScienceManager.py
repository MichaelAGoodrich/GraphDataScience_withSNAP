""" Data Science Manager 
    Run a series of graph database queries to gather information
    about the database.

    Michael A. Goodrich
    CS 575
    Brigham Young University

    March 2023
"""

from DatabaseManager import DatabaseManager
from GraphDatabaseManager import GraphManager


class DataScienceManager:
    def __init__(self,file_name):
        self.database = DatabaseManager(file_name)
        self.graphDatabase = self.__initialize_graphDatabaseManager()
        self.figure_number = 1
    ###########################
    # Visualization Utilities #
    ###########################
    def ShowUnifiedGraph(self):
        title = "Relationships with Movies"
        self.graphDatabase.showPlot(title = title, figure_number = self.figure_number,wait_for_button=False)
        self.figure_number +=1
        self.graphDatabase.pause()
    
    def ShowAllBipartiteGraphs(self):
        category_2 = 'name'
        #for category_1 in {'genre','writers','directors','casts'}:
        for category_1 in {'genre','writers','directors'}:
            title = "Links between " + category_1 + " and movie"
            self.graphDatabase.plotSubgraph(category_1,'rank',title = title, figure_number = self.figure_number,with_labels=False)
            self.figure_number +=1
        #for category_1 in {'genre','writers','directors','casts'}:
        #    graphManager = GraphManager(directed_graph=False)
        #    edges = self.database.getEdges(category_1,category_2)
        #    print("There are ",len(edges)," edges between movies and ",category_1," in the database")
        #    graphManager.addEdges(edges)
        #    title = "Links between " + category_1 + " and " + category_2
        #    graphManager.showPlot(title = title, figure_number = self.figure_number)
        #    self.figure_number +=1
        self.graphDatabase.pause()
    def ShowSubGraph(self,category):
        #for category in {'genre','writers','directors','casts'}:
        self.graphDatabase.plotSubgraph(category,'rank',with_labels=False)
        self.graphDatabase.pause()
    def ShowProjection(self,category,biggest_component = True):
        title = "Relationships between movie " + str(category)
        self.graphDatabase.plotProjection(category,title=title,figure_number = self.figure_number,biggest_component=True)
        self.figure_number +=1
        self.graphDatabase.pause()

    ###################
    # Private Methods #
    ###################
    def __initialize_graphDatabaseManager(self):
        graphManager = GraphManager(directed_graph=False)
        # Step 1: Initialize node set
        for category in {'genre','writers','directors','casts','rank'}:
            node_set = self.database.getNodesOfType(category)
            graphManager.addNodes(node_set,category)
        
        # Step 2: Initialize edge set
        category_2 = 'rank'
        for category_1 in {'genre','writers','directors','casts'}:
            edges = self.database.getEdges(category_1,category_2)
            graphManager.addEdges(edges)
        return graphManager
    