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
    # Getters and Setters     #
    ###########################
    def getProjection(self,categories,biggest_component = True):
        projection_graph = self.graphDatabase.extractProjectionGraph(categories)
        title = "Relationships between movie " + str(categories)
        if biggest_component:
            title = "Largest component of\n" + title
            projection_graph = self.graphDatabase.extractLargestComponent(projection_graph)
        return projection_graph, title
    def getGraphDatabase(self,biggest_component = True):
        graph = self.graphDatabase.getGraph_of_Database()
        title = "Entire graph database"
        if biggest_component:
            title = "Largest component of\n" + title
            projection_graph = self.graphDatabase.extractLargestComponent(projection_graph)
        return graph, title
    def getBipartiteGraph(self,category):
        title = "Links between " + category + " and movie"
        graph = self.graphDatabase.extractBipartiteGraph(category,'rank')
        return graph, title    