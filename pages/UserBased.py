import streamlit as st
import pickle
import pandas as pd
import requests
def app():
    def fetch(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
        data = requests.get(url)
        data = data.json()
        poster ={ 'poster_path':"https://image.tmdb.org/t/p/w500/"+data['poster_path']}
        data.update(poster)
        return data
    def recommend(movie):
        movie_index = movies[movies['title'] == movie].index[0]
        movies_list=movies['recommendations'].iloc[movie_index]
        movies_name=[]
        movies_posters=[]
        genre_list=[]
        overview_list=[]
        release_date_list=[]
        vote_average_list=[]
        for i in movies_list:
            movie_id = movies['id'].iloc[i]
            data = fetch(movie_id)
            movies_name.append(data['title'])
            movies_posters.append(data['poster_path'])
            genre_list.append(data['genres'])
            overview_list.append(data['overview'])
            release_date_list.append(data['release_date'])
            vote_average_list.append(data['vote_average'])
        return movies_name , movies_posters, genre_list, overview_list, release_date_list, vote_average_list


    movies = pickle.load(open('userbased.pkl','rb'))
    movies = pd.DataFrame(movies)
    num=st.sidebar.slider('No. of recommendation', min_value=5, max_value=20)
    selected_movie = st.selectbox(
        ' Select Movies you like ',
        movies['title'].values)

    if st.button('Show Recommendation based on content'):
        recommended_movie_names, recommended_movie_posters, genre_list, overview_list, release_date_list, vote_average_list= recommend(selected_movie)
        movie_index = movies[movies['title'] == selected_movie].index[0]
        movies_id = movies['id'].iloc[movie_index]
        movie_data=fetch(movies_id)
        selected_movie_image_col,selected_movie_info_col= st.columns([1,2])
        with selected_movie_image_col:
            st.image(movie_data['poster_path'])
        with selected_movie_info_col:
            st.header(selected_movie)
            genre = ""
            for k in movie_data['genres']:
                genre = genre + k['name'] + ','
            genre=genre[0:-1]
            st.text('Genre: '+genre)
            st.text('release date:' + movie_data['release_date'])
            st.text('Rating:'+str(movie_data['vote_average']))
            st.header('overview')
            st.markdown("""<span style="word-wrap:break-word;">""" + movie_data['overview'] + """</span>""", unsafe_allow_html=True)

        for i in range(0, num):
            if i % 5 == 0:
                col = st.columns(5)
                counter = 0
            with col[counter]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])
                with st.expander("Read More"):
                    st.title(recommended_movie_names[i])
                    genre = ""
                    for k in genre_list[i]:
                        genre=genre+k['name']+','
                    genre=genre[0:-1]
                    st.text("Genre: "+genre)
                    st.text("release_date:" + release_date_list[i])
                    st.text("Rating: "+ str(vote_average_list[i]))
                    st.header("overview")
                    st.markdown("""<span style="word-wrap:break-word;">""" + overview_list[i] + """</span>""", unsafe_allow_html=True)
                counter = counter + 1
        st.snow()





