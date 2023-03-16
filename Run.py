""" Main functions for extracting nodes and edges from movie database

    Michael A. Goodrich
    CS 575
    Brigham Young University

    March 2023
"""
from DataScienceManager import DataScienceManager

def main():
    manager = DataScienceManager('databases/IMDB Top 250 Movies.csv')
    #manager.ShowAllBipartiteGraphs()
    manager.ShowUnifiedGraph()
main()