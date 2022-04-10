"""Use TMDB APIs to get the following information from TMDB:
- movie title
- movie overview
- movie popularity(avg rating)
- movie release date
- movie image
- movie trailer URL

"""
import tmdbv3api
from tmdbv3api import TMDb, Movie
import requests


class TMDBInfo:

    def __init__(self, movieId, api_key, tmdb):
        tmdb = TMDb()
        self.language = 'en'
        self.base = "https://api.themoviedb.org/3/movie/"
        self.append_to_response = "videos"
        self.key = []
        self.name = []
        self.site = []
        self.movieId = movieId
        self.api_key = api_key

    def get_details(self):
        """
        get movie details from TMDB 
        """
        movieId = self.movieId
        movie = Movie()
        print(movie)
        m = movie.details(movieId)
        image_base = 'http://image.tmdb.org/t/p/w185'
        poster_path = image_base
        if getattr(m, 'poster_path', 'n/a') is not None:
            poster_path = image_base+getattr(m, 'poster_path', 'n/a')
        return getattr(m, 'overview', 'n/a'), poster_path, getattr(m, 'title', 'n/a'), getattr(m, 'popularity', 'n/a'), getattr(m, 'release_date', 'n/a')

    def get_movie_trailer(self):
        """Get movie trailer from TMDB
        """

        url = "%s%s/%s?api_key=%s&language=%s" % (
            self.base,
            self.movieId,
            self.append_to_response,
            self.api_key,
            self.language,
        )
        key = []
        site = []
        name = []
        try:
            rec = requests.request('GET', url)
            rec = rec.json()["results"]
            
            for dict1 in rec:
                if dict1["type"] == "Trailer":
                    key.append(dict1["key"])
                    site.append(dict1["site"])
                    name.append(dict1["name"])
            self.key = key
            self.name = name
            self.site = site
        except:
            self.key = key
            self.name = name
            self.site = site

    def get_video_url(self):
        """Create correct URL to embed the movie trailer in HTML code
        """
        if len(self.site) > 0:
            movie_site = self.site[0]
            base_url = "https://www.youtube.com/embed/"
            base_url_vimeo = "https://vimeo.com/"
            if movie_site != "YouTube":
                base_url = base_url_vimeo

            trailer_url = "%s%s" % (
                base_url,
                str(self.key[0])
            )
            return trailer_url
        else:
            return []
