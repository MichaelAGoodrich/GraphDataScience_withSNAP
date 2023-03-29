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
    wd_colormap_dict = wd_network_handler.getAgentColormapDict_from_LouvainCommunities()
    writer_director_title = "Louvain communities for " + writer_director_title
    #wd_colormap_dict = wd_network_handler.getAgentColormapDict_from_GirvanNewmanCommunities()
    #writer_director_title = "Girvan-Newman communities for " + writer_director_title
    wd_network_handler.setAgentColors(wd_colormap_dict)
    wd_network_handler.showNetwork(title=writer_director_title, pause=False,advanceFigure=False)
    #wd_network_handler.show_kCore_Subgraph(pause=True)
    #wd_network_handler.advanceFigureCounter()

    # Get information and plot largest k-core over the top of the previous figure
    xlim,ylim = wd_network_handler.getFigureData()
    writer_director_title = "Largest k-core for " + writer_director_title
    wd_network_handler.show_kCore_Subgraph(bigNodes = True,xlim = xlim, ylim = ylim)
    # Plot the k-core by itself
    wd_network_handler.advanceFigureCounter()
    wd_network_handler.show_kCore_Subgraph(title = writer_director_title, pause=False,xlim = xlim, ylim = ylim)
    
    
    ###################################################
    # Demonstrate basic graph data science operations #
    # For large graph                                 #
    ###################################################
    writer_director_cast_projection, writer_director_cast_title = manager.getProjection({'casts','directors','writers'},biggest_component=True)
    wdc_network_handler = networkHandler(writer_director_cast_projection)
    wdc_network_handler.setFigureNumber(5)
    wdc_network_handler.getNetworkStatistics()
    wdc_colormap_dict = wdc_network_handler.getAgentColormapDict_from_LouvainCommunities()
    writer_director_cast_title = "Louvain communities for " + writer_director_cast_title
    wdc_network_handler.setAgentColors(wdc_colormap_dict)
    wdc_network_handler.showNetwork(title=writer_director_cast_title, pause=False)
    xlim,ylim = wdc_network_handler.getFigureData()
    writer_director_cast_title = "Largest k-core for " + writer_director_cast_title
    wdc_network_handler.show_kCore_Subgraph(title = writer_director_cast_title, pause=True,xlim = xlim, ylim = ylim)

    
main()