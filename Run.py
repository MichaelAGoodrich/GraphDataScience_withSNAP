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
    writer_director_projection, writer_director_title = manager.getProjection({'writers','directors'},biggest_component=True)
    wd_network_handler = networkHandler(writer_director_projection)
    wd_network_handler.showNetwork(colormap = None, title=writer_director_title, pause=False)
    
    ####################################
    # Demonstrate how to apply network #
    # analysis tools to graph database #
    ####################################
    wd_network_handler.getNetworkStatistics()
    wd_network_handler.showDendrogram(wait_for_button = False)
    wd_colormap = wd_network_handler.getAgentColors_from_LouvainCommunities()
    writer_director_title = "Louvain communities for " + writer_director_title
    wd_network_handler.setAgentColors(wd_colormap)
    wd_network_handler.showNetwork(pause=False)
    wd_network_handler.show_kCore_Subgraph(pause=True)

    ###################################################
    # Demonstrate basic graph data science operations #
    # For large graph                                 #
    ###################################################
    #writer_director_cast_projection, writer_director_cast_title = manager.getProjection({'casts','directors','writers'},biggest_component=True)
    #wdc_network_handler = networkHandler(writer_director_cast_projection)
    #wdc_network_handler.getNetworkStatistics()
    #wdc_colormap = wdc_network_handler.getAgentColors_from_LouvainCommunities()
    #writer_director_cast_title = "Louvain communities for " + writer_director_cast_title
    #wdc_network_handler.showNetwork(colormap = wdc_colormap, title=writer_director_cast_title, pause=True)
    
main()