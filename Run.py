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
    # For small graph first                           #
    ###################################################
    manager = DataScienceManager('databases/IMDB Top 250 Movies.csv')
    #manager.ShowUnifiedGraph()
    #manager.ShowAllBipartiteGraphs(pause=False)
    manager.ShowBipartiteSubgraph('directors',pause=False)
    writer_director_projection, writer_director_title = manager.GetProjection({'writers','directors'},biggest_component=True)
    manager.ShowProjection(writer_director_projection, title=writer_director_title, pause=False)
    
    ####################################
    # Demonstrate how to apply network #
    # analysis tools to graph database #
    ####################################
    wd_network_handler = networkHandler(writer_director_projection)
    #wd_network_handler.showDendrogram(figureNumber = 10, wait_for_button = False)
    wd_colormap = wd_network_handler.getAgentColors_from_LouvainCommunities()
    writer_director_title = "Louvain communities for\n" + writer_director_title
    manager.ShowProjection(writer_director_projection, colormap = wd_colormap, title=writer_director_title, pause=True)
    
    ###################################################
    # Demonstrate basic graph data science operations #
    # For large graph                                 #
    ###################################################
    writer_director_cast_projection, writer_director_cast_title = manager.GetProjection({'casts','directors','writers'},biggest_component=True)
    #manager.ShowProjection(writer_director_cast_projection, title=writer_director_cast_title, pause=True, save_subgraph=True)
    wdc_network_handler = networkHandler(writer_director_cast_projection)
    wdc_colormap = wdc_network_handler.getAgentColors_from_LouvainCommunities()
    writer_director_cast_title = "Louvain communities for\n" + writer_director_cast_title
    manager.ShowProjection(writer_director_cast_projection, colormap = wdc_colormap, title=writer_director_cast_title, pause=True)
    

    """ TODO: 
        • Get colors from the PartitionUtilities code base, and show graph with these colors.
        • Or, turn on the ability to view communities when projections are shown    
    """
main()