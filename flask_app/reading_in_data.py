import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine

try:
    import flask_app.config2 as config2
except ImportError:
    # this is not a flask app
    import config2 as config2
    config2.host = config2.host2
    config2.port = config2.port2

# establishing SQL connection
engine = create_engine(
    f"postgresql://{config2.database_user}:{config2.psql_pw}@{config2.host}:{config2.port}/{config2.database_name}")

# read in movie rating data
select_query = """
    SELECT * FROM movie_ratings ORDER BY "userId" LIMIT 300000;
    """
engine_output = engine.execute(select_query)

final_dict = []
for row in engine_output:
    dict1 = {"userId": int((row["userId"])), "movieId": int((row["movieId"])),
             "rating": float((row["rating"]))}
    final_dict.append(dict1)

user_rating_matrix = pd.DataFrame(final_dict)


# pivot data
user_rating = user_rating_matrix.pivot(
    index="userId", columns="movieId", values="rating")

# set the NANs to zero
ratings_pivot = user_rating.replace(np.nan, 0)

# read in data for movies and title
select_movies = """
    SELECT * FROM movies;
    """
engine_output_movies = engine.execute(select_movies)

movies_final = []
for row in engine_output_movies:
    dict1 = {"movieId": int((row["movieId"])),
             "title": str((row["title"]))}
    movies_final.append(dict1)

movies_df = pd.DataFrame(movies_final)

movies_df['year'] = 0
for i, data in movies_df.iterrows():
    try:
        movies_df.loc[i, 'year'] = int(
            data['title'].split('(')[-1].replace(')', ''))
    except:
        movies_df.loc[i, 'year'] = 0

movies = movies_df[['title', 'year', 'movieId']]

# read in the link data for IMDB and TMDB
select_link = """
    SELECT * FROM link;
    """
engine_output_link = engine.execute(select_link)

movies_link = []
for row in engine_output_link:
    dict1 = {"movieId": int((row["movieId"])),
             "tmdbId": str((row["tmdbId"]))}
    movies_link.append(dict1)

link = pd.DataFrame(movies_link)
