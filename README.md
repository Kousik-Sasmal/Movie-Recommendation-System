# Movie-Recommendation-System

Using the https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata data, I have created a `Movie Recommendation System`.

All the analysis has been done in `Jupyter notebook`, and those files are kept in the `notebooks` folder.
All the files generated after analysis are kept in the `artifacts` folder.

From the analysis, created `app.py` which consists of mainly two functionality.
  - Shows Recommendation for Movies
  - Shows Popular Movies
      - Overall Popular Movies
      - Genre-wise Popular Movies


`utils.py`: Codes for fetching the Movie Poster from https://developer.themoviedb.org/ with the help of API. 
            Calculate `cosine similarity`.
            

`poster_image_url.json`: A `json` database.
`database.py`: Codes for searching and inserting `Poster image url` in the `poster_image_url.json` database.
