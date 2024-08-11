import pandas as pd
import streamlit as st
import pickle
import requests
import bz2file as bz2

movies_dict= pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
# similirity=pickle.load(open('similirity.pkl','rb'))

# to unzip piclefile
similirity=bz2.BZ2File('similirity.pbz2', 'rb')
similirity = pickle.load(similirity)

recommeded_movies=[]
recommeded_movies_poster=[]

# to fetch the movie poster from TMDB
def fetch_poster(movie_id):
    # get the jeson url details
    response=requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=b847a9ecf17a15c2781364b547dbbf05')
    data=response.json()
    # st.text(data)
    return 'https://image.tmdb.org/t/p/original' + data['poster_path']

def recommend(movie):
    movies_index=movies[movies['title']==movie].index[0]
    distance=similirity[movies_index]
    movies_list=sorted(list(enumerate(distance)),reverse=True,key= lambda x:x[1])[1:6] #top five movies

    recommeded_movies = []
    recommeded_movies_poster = []

    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id

        recommeded_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommeded_movies_poster.append(fetch_poster(movie_id))
    return recommeded_movies,recommeded_movies_poster


st.title('Movie Recommendation System')

selected_movie = st.selectbox(
    "How would you like to be watched?",
    movies['title'].values
    )

# to display the recommended movies
if st.button("Recommend", type="primary"):
    names,posters =recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])

    # for m in names:
    #     st.write(m)