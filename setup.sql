INSERT INTO public.movies
("timestamp", "movieId", title)
VALUES(now(), 1, 'The Matrix (1999)');

INSERT INTO public.link
("timestamp", "movieId", "tmdbId")
VALUES(now(), 1, 1);

INSERT INTO public.movies
("timestamp", "movieId", title)
VALUES(now(), 2, 'Star Wars - A New Hope (1977)');

INSERT INTO public.link
("timestamp", "movieId", "tmdbId")
VALUES(now(), 2, 2);

INSERT INTO public.movies
("timestamp", "movieId", title)
VALUES(now(), 3, 'Wreck it Ralph (2009)');

INSERT INTO public.link
("timestamp", "movieId", "tmdbId")
VALUES(now(), 3, 3);

INSERT INTO public.movies
("timestamp", "movieId", title)
VALUES(now(), 4, 'Avatar (2007)');

INSERT INTO public.link
("timestamp", "movieId", "tmdbId")
VALUES(now(), 4, 4);

INSERT INTO public.movie_ratings
("timestamp", "userId", "movieId", rating)
VALUES(now(), 1, 1, 5);

INSERT INTO public.movie_ratings
("timestamp", "userId", "movieId", rating)
VALUES(now(), 1, 2, 5);


INSERT INTO public.movie_ratings
("timestamp", "userId", "movieId", rating)
VALUES(now(), 2, 2, 5);

INSERT INTO public.movie_ratings
("timestamp", "userId", "movieId", rating)
VALUES(now(), 2, 3, 5);

INSERT INTO public.movie_ratings
("timestamp", "userId", "movieId", rating)
VALUES(now(), 3, 3, 5);

INSERT INTO public.movie_ratings
("timestamp", "userId", "movieId", rating)
VALUES(now(), 3, 4, 5);

