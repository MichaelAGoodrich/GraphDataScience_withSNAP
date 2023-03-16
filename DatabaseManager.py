""" Database manager
        Reads .csv file into pandas dataframe
        Extracts genres, movies, MPAA ratings, actors, and directors
        Finds relationships between various elements.

        Michael A. Goodrich
        CS 575
        Brigham Young University

        March 2023
"""
import pandas as pd

class DatabaseManager:
    def __init__(self,file_name):
        self.dataframe = pd.read_csv(file_name)
        #print(file_name)
        #print(self.dataframe)
    
    ########################
    # Extraction Utilities #
    ########################
    def get_unique_genres(self):
        genres = self.dataframe["genre"]
        set_of_genres = set()
        for i in range(len(genres)):
            movie_genre_types = genres[i].split(',')
            for genre in movie_genre_types:
                set_of_genres.add(genre)
        print("There are ",len(set_of_genres)," genres in the database")
        return set_of_genres
    def get_movies(self):
        # Identify the movies by their ranking from the database rather than from the title"
        movie_rankings = self.dataframe["rank"] # The movies are identified by their popularity ranking
        set_of_rankings = set()
        for i in range(len(movie_rankings)):
            set_of_rankings.add(str(movie_rankings[i]))
        print("There are ",len(set_of_rankings),"movies in the database")
        return set_of_rankings
    def get_edges(self,category_1, category_2):
        """ Oh, this method is such ugly code! """
        ### Step 1: Error check
        if category_1 not in set(self.dataframe.columns) or category_2 not in set(self.dataframe.columns): raise ValueError
        if category_1 == category_2: raise ValueError
        if category_2 == 'name': category_2 = "rank"
        if category_1 == "name": category_1 = "rank"
        
        ### Step 2: Extract multiple entities from with a category if 
        ### the category is genre, writers, directors, or casts
        entries_1 = self.dataframe[category_1]
        entries_2 = self.dataframe[category_2]
        set_of_edges = set()
        for i in range(len(entries_1)):
            if category_1 in {'genre','writers','directors','casts'} and category_2 in {'genre','writers','directors','casts'}:
                refined_entries_1 = entries_1[i].split(',')
                refined_entries_2 = entries_2[i].split(',')
                for e1 in list(refined_entries_1):
                    for e2 in list(refined_entries_2):
                        set_of_edges.add((str(e1),str(e2)))
            elif category_1 in {'genre','writers','directors','casts'}:
                refined_entries_1 = entries_1[i].split(',')
                for e1 in list(refined_entries_1):
                    set_of_edges.add((str(e1),str(entries_2[i])))
            elif category_2 in {'genre','writers','directors','casts'}:
                refined_entries_2 = entries_2[i].split(',')
                for e2 in list(refined_entries_2):
                    set_of_edges.add((str(entries_1[i]),str(e2)))
            else: set_of_edges.add((str(entries_1[i]),str(entries_2[i])))
        return set_of_edges

    ####################
    # Public Utilities #
    ####################
    def showHead(self): 
        # This function returns the first n rows for the object based on position. 
        # It is useful for quickly testing if your object has the right type of data in it.
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.head.html
        print(self.dataframe.head())
    def showInfo(self):
        # This method prints information about a DataFrame including the index dtype and 
        # columns, non-null values and memory usage.
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.info.html
        print(self.dataframe.info())
    def showValueCounts(self,category = 'genre'):
        if category not in set(self.dataframe.columns): raise ValueError
        print(self.dataframe.value_counts(category))