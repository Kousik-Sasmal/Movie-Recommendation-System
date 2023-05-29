import streamlit as st
import numpy as np
import pandas as pd
import math
import pickle

from utils import similarity
from utils import poster_fetch

popular_df = pickle.load(open('artifacts/popular_df.pkl','rb'))
genres_group = pickle.load(open('artifacts/genres_group.pkl','rb'))
new_df = pd.read_csv('artifacts/new_df.csv')
google_url_df = pd.read_csv('artifacts/google_url_df.csv')


def recommend(movie):
    """
    Takes a title of a `movie` and recommend 6 movies include that movie.
    Returns the tuple of two lists  `movie_ids` and `movie_titles`.
    """
    movie_titles = []
    movie_ids = []
    index = new_df[new_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[:6]:
        movie_titles.append(new_df.iloc[i[0]].title)
        movie_ids.append(new_df.iloc[i[0]].movie_id)
        
    return movie_ids,movie_titles


def get_movie_details(genre):
    """"
    Takes any specific `genre`.
    Returns the tuple of two lists  `movie_ids` and `movie_titles`.
    """
    movie_ids = []
    movie_titles = []
    for i in range(len(genres_group[genre])):
        m_id = list(genres_group[genre][i].keys())[0]
        m_title = genres_group[genre][i][m_id]
        
        movie_ids.append(m_id)
        movie_titles.append(m_title)
    return movie_ids,movie_titles


def showing_movie_details(num_movies,movie_titles,movie_posters):
    """
    Takes 3 inputs: `num_movies`, `movie_titles`, `movie_posters`.
    Shows `movie_titles` and `movie_posters` to user.
    """
    num_columns = 5
    # if the number of available movies is not the multiple of 5 
    num_rows = math.ceil(num_movies / 5)

    for row_index in range(num_rows):
        cols = st.columns(num_columns)

        for col_index, col in enumerate(cols):
            movie_index = row_index * num_columns + col_index

            google_link = google_url_df[google_url_df['title'] == movie_titles[movie_index]]['google_url'].values[0]
            if movie_index < len(popular_df[:num_movies]):
                with col:
                    col.image(movie_posters[movie_index])
                    col.markdown(f"**{movie_titles[movie_index]}**")  # title
                    col.write(google_link)
            else:
                break



def load_recommended_movies():
    st.header('Recommended Movies')

    selected_movie = st.selectbox('Select a movie',new_df['title'].tolist())
    btn1 = st.button('Recommend')
    if btn1:
        ids,movies = recommend(selected_movie)
        poster_image_urls = poster_fetch(ids)

        cols = st.columns(6)
        for i in range(6):
            google_link = google_url_df[google_url_df['title'] == movies[i]]['google_url'].values[0]
                
            cols[i].image(poster_image_urls[i])
            cols[i].write(f"**{movies[i]}**")  #title
            cols[i].write(google_link)


def load_genre_wise_popular_movies():
    st.header('Genre-wise Popular Movies')
    
    unique_genres = list(set(popular_df['genres'].explode()))
    unique_genres.remove(np.nan)

    selected_genre = st.selectbox('Select Genre',unique_genres)
    num_movies = st.selectbox('Select the number of top Movies',[i for i in range(10,510,10)])
    btn2 = st.button('Submit')
    if btn2:
        movies_in_genre = len(genres_group[selected_genre])
        # if number of movies asked is greater than the available movies in a specific genre
        if movies_in_genre < num_movies:
            num_movies = movies_in_genre

        st.markdown(f'**{movies_in_genre} Movies** in the {selected_genre} genre, showing you **{num_movies} Movies**')
        movie_ids, movie_titles = get_movie_details(selected_genre)
        movie_ids, movie_titles = movie_ids[:num_movies], movie_titles[:num_movies]
        movie_posters = poster_fetch(movie_ids)
        showing_movie_details(num_movies,movie_titles,movie_posters)


def load_overall_popular_movies():
    st.header('Overall Popular Movies')

    num_movies = st.selectbox('Select the number of top Movies',[i for i in range(10,1010,10)])
    btn3 = st.button('Submit')
    if btn3:
        movie_titles, movie_ids = list(popular_df[:num_movies]['title']), list(popular_df[:num_movies]['movie_id'])
        movie_posters = poster_fetch(movie_ids)

        showing_movie_details(num_movies,movie_titles,movie_posters)




st.set_page_config(page_title='Movie Recommender')
st.title('Movie Recommendation System')

option = st.selectbox('Select what you want',['Get Recommendation for Movies','Popular Movies'])

if option == 'Get Recommendation for Movies':
    load_recommended_movies()

if option == 'Popular Movies':
    st.header('Popular Movies')
    option2 = st.selectbox('Select one',['Overall Popular Movies','Genre-wise Popular Movies'])

    if option2 == 'Genre-wise Popular Movies':
        load_genre_wise_popular_movies()

    if option2 == 'Overall Popular Movies':
        load_overall_popular_movies()


