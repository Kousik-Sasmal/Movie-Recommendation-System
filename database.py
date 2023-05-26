import json


def search(movie_id):       
    with open('poster_image_url.json','r') as rf:
        images_data = json.load(rf)

        if str(movie_id) in images_data:
            return images_data[str(movie_id)]
        else:
            return 0
    

def insert(movie_id,image_url):
    with open('poster_image_url.json','r') as rf:
        images_data = json.load(rf)
        images_data[str(movie_id)] = image_url

    with open('poster_image_url.json','w') as wf:
        json.dump(images_data,wf,indent=4)
    

     