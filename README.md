# Movie-Recommendation-System


Using the https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata data, I have created a `Movie Recommendation System` and converted into `Streamlit` web app.


My App link: https://kousik-sasmal-movie-recommendation-system-app-46mgfp.streamlit.app/


All the analysis has been done in `Jupyter notebook`, and those files are kept in the `notebooks` folder. All the files generated after analysis are kept in the `artifacts` folder.

With the help of those analysis, created `app.py` which consists of mainly two functionality.
  - Shows Recommendation for Movies (`Content-based filtering`)
  - Shows Popular Movies (`Popularity-based filtering`)
      - Overall Popular Movies
      - Genre-wise Popular Movies


`utils.py`: Codes for fetching the Movie Poster from https://developer.themoviedb.org/ with the help of API, and for calculating cosine similarity.
            

`poster_image_url.json`: A temporary database.


`database.py`: Codes for searching and inserting `Poster image url` into the temporary database.
