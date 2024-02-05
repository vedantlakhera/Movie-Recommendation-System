import streamlit as st
import pickle
import pandas as pd
import requests

# Define your API key
API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()
    return {
        'poster_url': "https://image.tmdb.org/t/p/original" + data['poster_path'],
        'overview': data['overview'],
        'rating': data['vote_average'],
        'genres': [genre['name'] for genre in data['genres']],
        'release_date': data['release_date']
    }

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_details = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch movie details from API
        movie_details = fetch_movie_details(movie_id)
        recommended_movies_details.append(movie_details)
    return recommended_movies, recommended_movies_details

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Main title
st.title('🎬 Movie Recommender System')

# Background and sidebar color
st.markdown(
    """
    <style>
    body {
        background-color: #f6f7f9;
        color: #333333;
        font-family: Arial, sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #3498db;
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    .sidebar .sidebar-content select {
        background-color: #2980b9;
        color: white;
    }
    .sidebar .sidebar-content button {
        background-color: #2ecc71;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
    }
    .sidebar .sidebar-content button:hover {
        background-color: #27ae60;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.title('Options')
selected_movie_name = st.sidebar.selectbox('Select a movie:', movies['title'].values)
button_clicked = st.sidebar.button('Get Recommendations')

if button_clicked:
    # Get recommendations
    names, details = recommend(selected_movie_name)

    # Display recommendations
    for i, movie_name in enumerate(names):
        st.write('---')
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(details[i]['poster_url'], use_column_width=True)
        with col2:
            st.write(f"**Movie Name:** {movie_name}")
            st.write(f"**Rating:** {details[i]['rating']}")
            st.write(f"**Genres:** {', '.join(details[i]['genres'])}")
            st.write(f"**Release Date:** {details[i]['release_date']}")
            st.write(f"**Overview:** {details[i]['overview']}")
















