-- get movies ordered by rating
SELECT m."movieId", m.title, m.genres, COUNT(r.rating) AS rating_count
FROM public.movies AS m
LEFT JOIN public.movie_ratings AS r ON m."movieId" = r."movieId"
GROUP BY m."movieId", m.title, m.genres
ORDER BY rating_count DESC;
