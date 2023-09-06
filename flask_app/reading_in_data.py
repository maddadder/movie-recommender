import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine, text

try:
    import flask_app.config2 as config2
except ImportError:
    # this is not a flask app
    import config2 as config2
    #config2.host = config2.host2
    #config2.port = config2.port2

# establishing SQL connection
engine = create_engine(
    f"postgresql://{config2.database_user}:{config2.psql_pw}@{config2.host}:{config2.port}/{config2.database_name}")

# read in movie rating data
select_query = text('SELECT * FROM movie_ratings ORDER BY "userId" LIMIT 400000;')
connection = engine.connect()

engine_output = connection.execute(select_query)

final_dict = []
column_names = list(engine_output.keys())  # Get the column names
for row in engine_output:
    dict1 = {"userId": int(row[column_names.index("userId")]), "movieId": int(row[column_names.index("movieId")]), "rating": float(row[column_names.index("rating")])}
    final_dict.append(dict1)

user_rating_matrix = pd.DataFrame(final_dict)


# pivot data
user_rating = user_rating_matrix.pivot(
    index="userId", columns="movieId", values="rating")

# set the NANs to zero
ratings_pivot = user_rating.replace(np.nan, 0)

# read in data for movies and title
select_movies = text('SELECT * FROM movies;')

engine_output_movies = connection.execute(select_movies)

movies_final = []
column_names_movies = list(engine_output_movies.keys())  # Get the column names
for row in engine_output_movies:
    dict1 = {"movieId": int(row[column_names_movies.index("movieId")]), "title": str(row[column_names_movies.index("title")])}
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
select_link = text('SELECT * FROM link;')

engine_output_link = connection.execute(select_link)

movies_link = []
column_names_link = list(engine_output_link.keys())  # Get the column names

for row in engine_output_link:
    dict1 = {"movieId": int(row[column_names_link.index("movieId")]), "tmdbId": str(row[column_names_link.index("tmdbId")])}
    movies_link.append(dict1)
    
link = pd.DataFrame(movies_link)
connection.close()