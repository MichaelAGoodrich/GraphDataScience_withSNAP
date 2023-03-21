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

def main():
    manager = DataScienceManager('databases/IMDB Top 250 Movies.csv')
    #manager.ShowUnifiedGraph()
    #manager.ShowAllBipartiteGraphs()
    #manager.ShowBipartiteSubgraph('genre')
    manager.ShowProjection({'writers','directors'},biggest_component=False)
    manager.ShowProjection({'writers','directors'},biggest_component=True)
    #manager.ShowProjection({'casts','directors','writers'},save_subgraph=True)
main()