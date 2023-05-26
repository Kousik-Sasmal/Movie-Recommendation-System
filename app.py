import streamlit as st
import numpy as np
import pandas as pd
import pickle

from utils import similarity
from utils import poster_fetch

popular_df = pickle.load(open('artifacts/popular_df.pkl','rb'))
genres_group = pickle.load(open('artifacts/genres_group.pkl','rb'))
new_df = pd.read_csv('artifacts/new_df.csv')


def recommend(movie):
    movies = []
    movie_id = []
    index = new_df[new_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[:6]:
        movies.append(new_df.iloc[i[0]].title)
        movie_id.append(new_df.iloc[i[0]].movie_id)
        
    return movies,movie_id


def get_movie_details(genre):
    movie_ids = []
    movie_titles = []
    for i in range(len(genres_group[genre])):
        m_id = list(genres_group[genre][i].keys())[0]
        m_title = genres_group[genre][i][m_id]
        
        movie_ids.append(m_id)
        movie_titles.append(m_title)
    return movie_ids,movie_titles


def showing_movie_details(num_movies,movie_titles,movie_posters):
    num_columns = 5
    num_rows = num_movies // 5

    for row_index in range(num_rows):
        cols = st.columns(num_columns)

        for col_index, col in enumerate(cols):
            movie_index = row_index * num_columns + col_index

            if movie_index < len(popular_df[:num_movies]):
                with col:
                    col.image(movie_posters[movie_index])
                    col.markdown(f"**{movie_titles[movie_index]}**")  # title
            else:
                break


def load_recommended_movies():
    st.header('Recommended Movies')

    selected_movie = st.selectbox('Select a movie',new_df['title'].tolist())
    btn1 = st.button('Recommend')
    if btn1:
        movies,ids = recommend(selected_movie)
        poster_image_urls = poster_fetch(ids)

        cols = st.columns(6)
        for i in range(6):
            cols[i].image(poster_image_urls[i])
            cols[i].write(f"**{movies[i]}**")  #title


def load_genre_wise_popular_movies():
    st.header('Genre-wise Popular Movies')
    unique_genres = list(set(popular_df['genres'].explode()))
    unique_genres.remove(np.nan)

    selected_genre = st.selectbox('Select Genre',unique_genres)
    num_movies = st.selectbox('Select the number of top Movies',[i for i in range(10,510,10)])
    btn2 = st.button('Submit')
    if btn2:
        movies_in_genre = len(genres_group[selected_genre])

        if movies_in_genre > num_movies:
            st.markdown(f'**{movies_in_genre} Movies** in this genre, showing you **{num_movies} Movies**')
        else:
            st.markdown(f'**{movies_in_genre} Movies** in this genre, showing you **{movies_in_genre} Movies**')

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


