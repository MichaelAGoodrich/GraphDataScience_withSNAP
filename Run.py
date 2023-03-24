""" Main functions for extracting nodes and edges from movie database.

    Much of the code here is patterned after chapter 2 in
        Graph Data Science with Neo4j
        Estelle Scifo, Packt Publishing Ltd, 2023

    Code designed around kaggle dataset
        https://www.kaggle.com/datasets/themrityunjaypathak/imdb-top-100-movies

    Michael A. Goodrich
    CS 575
    Brigham Young University

    March 2023
"""
from DataScienceManager import DataScienceManager
from NetworkUtilities import networkHandler

def main():
    ###################################################
    # Demonstrate basic graph data science operations #
    ###################################################
    manager = DataScienceManager('databases/IMDB Top 250 Movies.csv')
    #manager.ShowUnifiedGraph()
    #manager.ShowAllBipartiteGraphs(pause=False)
    manager.ShowBipartiteSubgraph('directors',pause=False)
    writer_director_projection, writer_director_title = manager.GetProjection({'writers','directors'},biggest_component=True)
    writer_director_colormap = ['y' for node in writer_director_projection]
    manager.ShowProjection(writer_director_projection, colormap = writer_director_colormap, title=writer_director_title, pause=False)
    writer_director_cast_projection, writer_director_cast_title = manager.GetProjection({'casts','directors','writers'},biggest_component=True)
    #manager.ShowProjection(writer_director_cast_projection, title=writer_director_cast_title, pause=True, save_subgraph=True)

    ####################################
    # Demonstrate how to apply network #
    # analysis tools to graph database #
    ####################################
    wd_network_handler = networkHandler(writer_director_projection)
    wdc_network_handler = networkHandler(writer_director_cast_projection)
    wd_network_handler.showDendrogram(figureNumber = 4, wait_for_button = True)

    """ TODO: 
        • Get colors from the PartitionUtilities code base, and show graph with these colors.
        • Or, turn on the ability to view communities when projections are shown    
    """
main()