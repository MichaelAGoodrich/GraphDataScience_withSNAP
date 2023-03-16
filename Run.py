""" Main functions for extracting nodes and edges from movie database

    Michael A. Goodrich
    CS 575
    Brigham Young University

    March 2023
"""
from DatabaseManager import DatabaseManager
from GraphManager import GraphManager

def main():
    database = DatabaseManager('databases/IMDB Top 250 Movies.csv')
    graphManager = GraphManager(directed_graph=False)
    #database.showHead()
    #database.showInfo()
    figure_number = 1
    category_2 = 'name'
    for category_1 in {'genre','writers','directors','casts'}:
        edges = database.get_edges(category_1,category_2)
        print("There are ",len(edges)," edges between movies and ",category_1," in the database")
        graphManager.addEdges(edges)
        title = "Links between " + category_1 + " and " + category_2
        graphManager.showPlot(title = title, figure_number = figure_number,wait_for_button=False)
        figure_number +=1
    graphManager.pause()
main()