from flask import Flask 
from recommender import input_movies
from flask import render_template
from recommender import ratings_pivot, movies_df

import pandas as pd
most_rated = pd.DataFrame(ratings_pivot.isin([0.0]).sum().sort_values().head(10))
most_rated = pd.merge(most_rated, movies_df, on='movieId')

app = Flask(__name__)

@app.route('/')
def index():
    top10 = input_movies()
    return render_template(
        'main.html',
        title="Movie Recommender",
        movie0=most_rated['title'][0],
        movie1=most_rated['title'][1],
        movie2=most_rated['title'][2],
        movie3=most_rated['title'][3],
        movie4=most_rated['title'][4],
        movie5=most_rated['title'][5],
        movie6=most_rated['title'][6],
        movie7=most_rated['title'][7],
        movie8=most_rated['title'][8],
        movie9=most_rated['title'][9]
        )

@app.route('/recommender')
def recommender():
    recs = input_movies()
    return render_template('recommendations.html', movies=recs)