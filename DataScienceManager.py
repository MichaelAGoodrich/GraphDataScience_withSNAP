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
        for category_1 in {'genre','writers','directors','casts'}:
            graphManager = GraphManager(directed_graph=False)
            edges = self.database.get_edges(category_1,category_2)
            print("There are ",len(edges)," edges between movies and ",category_1," in the database")
            graphManager.addEdges(edges)
            title = "Links between " + category_1 + " and " + category_2
            graphManager.showPlot(title = title, figure_number = self.figure_number,wait_for_button=False)
            self.figure_number +=1
        graphManager.pause()

    ###################
    # Private Methods #
    ###################
    def __initialize_graphDatabaseManager(self):
        category_2 = 'name'
        graphManager = GraphManager(directed_graph=False)
        for category_1 in {'genre','writers','directors','casts'}:
            edges = self.database.get_edges(category_1,category_2)
            graphManager.addEdges(edges)
        return graphManager
