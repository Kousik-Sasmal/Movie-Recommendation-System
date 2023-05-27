import numpy as np
import pandas as pd
import requests
import database
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

new_df = pd.read_csv('artifacts/new_df.csv')

cv = CountVectorizer(max_features=5000,stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# since the size of `similarity.pkl` was almost 200 MB, we did not convert it into pickle file
# and if we write within `app.py` --> take significant time to load website during changing input
# for that, we made a different file to compute `similarity`
similarity = cosine_similarity(vectors)


def poster_fetch(movie_ids):
    """
    Takes a list of `movie_ids`, and fetches urls of poster-images for movies.
    Returns a list of urls of poster-images for movies.
    """

    # if any problem in image_url loading, we will load this image_url (url of an unload image)
    unload_image_url = 'https://static.vecteezy.com/system/resources/previews/004/141/669/non_2x/no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-coming-soon-sign-simple-nature-silhouette-in-frame-isolated-illustration-vector.jpg'
   
    full_paths = []
    for _id in movie_ids:
        if database.search(_id)!=0:
            full_paths.append(database.search(_id))
        else:
            try:
                url = "https://api.themoviedb.org/3/movie/{}?api_key=879d1be008918a158ad109a08fd6d820".format(_id)
                response = requests.get(url)
                data = response.json()
                
                path = data['poster_path']
                full_path = 'https://image.tmdb.org/t/p/w780' + path
                full_paths.append(full_path)

                database.insert(_id,full_path)

            except:
                full_paths.append(unload_image_url)         

    return full_paths