import streamlit as st
import pickle
import pandas as pd
import requests
from model.ratingDB import insert_rating,fetch_rating

def app(user_id):
    def fetch_trailer(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}/videos?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
        data = requests.get(url)    
        data = data.json()
        data_list=data['results']
        key=""
        for i in data_list:
            if i['type']=="Trailer":
                key=i['key']
        if key=="":
            return ""
        trailer ="https://www.youtube.com/watch?v={}".format(key)
        return trailer


    def fetch(movie_id):
        '''fetching data from TMBD api
            using TMDB ID in the recommedation list
        '''
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
        data = requests.get(url)    
        data = data.json()      
        poster ={ 'poster_path':"https://image.tmdb.org/t/p/w500/"+data['poster_path']}
        data.update(poster)
        return data
    def recommend(selected_movie):
        ''' takes movie name as arguement and returns the
            details of the recommend movie 
            using fetch() function
            '''
        movie_index = movies[movies['title'] == selected_movie].index[0] #finding the index of selected_movie from movies dataframe
        movies_list=movies['BagOfWords'].iloc[movie_index] #returning the index of recommended movie
        movies_name=[]
        movies_posters=[]
        genre_list=[]
        overview_list=[]
        release_date_list=[]
        vote_average_list=[]
        trailer_list=[]
        for i in movies_list:   # iterating the movies_list and storing different details
            movie_id = movies['id'].iloc[i] 
            data = fetch(movie_id)
            trailer_list.append(fetch_trailer(movie_id))
            movies_name.append(data['title'])
            movies_posters.append(data['poster_path'])
            genre_list.append(data['genres'])
            overview_list.append(data['overview'])
            release_date_list.append(data['release_date'])
            vote_average_list.append(data['vote_average'])
        return movies_name , movies_posters, genre_list, overview_list, release_date_list, vote_average_list,trailer_list
    def rating_system(movie_id):
        movie_id=int(movie_id)
        def trigger():
            insert_rating(user_id,movie_id,st.session_state.myslider)
        old_rating=fetch_rating(user_id,movie_id)
        st.slider('Your rating',key='myslider',min_value=1,max_value=10,value= old_rating , 
            on_change= trigger )    
        stars=""
        for i in range(st.session_state.myslider):
            stars=stars+":star:"
        st.write(stars)
        

    movies = pickle.load(open('content_based.pkl','rb')) # reads the processed data from content_based.pkl
    movies = pd.DataFrame(movies)       # converts processed data into Dataframe from which the recommendation will be read by recommend() function
  

    col_selected_movies,col_slider=st.columns(2)
    with col_selected_movies:
        selected_movie = st.selectbox(' Select Movies you like ',movies['title'].values)
    with col_slider:
        num=st.slider('No. of recommendation', min_value=5, max_value=20)

        
    if st.checkbox('Show Recommendation based on content'):
        recommended_movie_names, recommended_movie_posters, genre_list, overview_list, release_date_list, vote_average_list,trailer_list= recommend(selected_movie)
        movie_index = movies[movies['title'] == selected_movie].index[0] #finding the index of selected_movie from movies dataframe
  
        #Printing different details of the recommended movie list in home
        for i in range(0, num):
            if i % 5 == 0:
                col = st.columns(5)
                counter = 0
            with col[counter]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])
                with st.expander("Read More"):
                    st.title(recommended_movie_names[i])
                    st.markdown("""<span style="word-wrap:break-word;">""" + overview_list[i] + """</span>""", unsafe_allow_html=True)
                    genre = ""
                    for k in genre_list[i]:
                        genre=genre+k['name']+','
                    genre=genre[0:-1]
                    st.text("Genre: "+genre)
                    st.text("release_date: " + release_date_list[i])
                    st.text("Rating: "+ str(vote_average_list[i]))
                    st.write("Click here for [Trailer]({})".format(trailer_list[i]))
                counter = counter + 1
        #storing different details of the selected movie to be printed in home
        movie_id = movies['id'].iloc[movie_index]
        movie_data=fetch(movie_id)
        selected_movie_image_col,selected_movie_info_col= st.columns([1,2])
        with selected_movie_image_col:
            st.image(movie_data['poster_path'])
        with selected_movie_info_col:
            st.header(selected_movie)
            rating_system(movie_id)  
            st.markdown("""<span style="word-wrap:break-word;">""" + movie_data['overview'] + """</span>""", unsafe_allow_html=True)
            genre = ""
            for k in movie_data['genres']:
                genre = genre + k['name'] + ','
            genre=genre[0:-1]
            st.text('Genre: '+genre)
            st.text('release date:' + movie_data['release_date'])
            st.text('Rating:'+str(movie_data['vote_average']))
            st.write("Click here for [Trailer]({})".format(fetch_trailer(movie_id)))

        
         





