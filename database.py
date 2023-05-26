import json
import streamlit as st


unload_image_url = 'https://static.vecteezy.com/system/resources/previews/004/141/669/non_2x/no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-coming-soon-sign-simple-nature-silhouette-in-frame-isolated-illustration-vector.jpg'

def search(movie_id):       
    try:
        with open('poster_image_url.json','r') as rf:
            images_data = json.load(rf)

        if str(movie_id) in images_data:
            return images_data[str(movie_id)]
        else:
            return 0
        
    except json.decoder.JSONDecodeError:
        st.write("DO NOT CHANGE input until get results")
        return unload_image_url

def insert(movie_id,image_url):
    with open('poster_image_url.json','r') as rf:
        images_data = json.load(rf)
        images_data[str(movie_id)] = image_url

    with open('poster_image_url.json','w') as wf:
        json.dump(images_data,wf,indent=4)
