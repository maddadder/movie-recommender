"""
This is a helper function that renders the most popular movie and then
displays to the user those movies with the highest standard deviation of the rating.
It solves the cold start problem.
"""
import random
import numpy as np
import pandas as pd

from flask_app.reading_in_data import user_rating_matrix, movies

def input_movies(old, new, movies_with_title):
    """
    Returns a data frame with 15 movie titles and their movieId link
    ##Parameters##:
    old - MovieId of old movies 
    new - MovieIds of new movies
    movies_with_tile - data frame containing user ratings, movieId and title of the movies

    ##Returns##:
    Data frame of 15 movies containing MovieId and title

    """

    old_choice = np.random.choice(old, 17, replace=False)
    new_choice = np.random.choice(new, 18, replace=False)
    m1 = movies_with_title[movies_with_title["movieId"].isin(old_choice)]
    m2 = movies_with_title[movies_with_title["movieId"].isin(new_choice)]
    most_rated = pd.concat([m2,m1], ignore_index=True)
    return most_rated[['title', 'movieId']]

def get_most_rated():
    """
    get most rated
    """
    # data preparation

    user_rating_matrix["sum_rating"] = user_rating_matrix.groupby("movieId")["rating"].transform("sum")
    user_rating_matrix["std_rating"] = user_rating_matrix.groupby("movieId")["rating"].transform("std")

    # removes duplicates created by the transform function
    sorted_matrix = user_rating_matrix.groupby(["movieId"])[["std_rating", "sum_rating"]].mean().sort_values(by='sum_rating', ascending=False)

    # merges data frame with movies data frame containing titles
    movies_with_title = pd.merge(sorted_matrix, movies, on='movieId')

    # categorizes movies into old and new category, then selects those with highest standard dev
    old = movies_with_title[movies_with_title["year"] <= movies_with_title["year"].mean()].head(200)
    new = movies_with_title[movies_with_title["year"] > movies_with_title["year"].mean()].head(200)
    print(movies_with_title["year"].mean())
    old.sort_values(by="std_rating", ascending=False, inplace=True)
    new.sort_values(by="std_rating", ascending=False, inplace=True)
    old = old["movieId"].unique()
    new = new["movieId"].unique()
    return input_movies(old=old, new=new, movies_with_title=movies_with_title)
