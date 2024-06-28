import streamlit as st
import pickle
import requests

# Load data
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['original_title'].values

# Set page config and title
st.set_page_config(page_title="CineQuest", page_icon=":clapper:", layout="wide")

# Custom CSS to enhance design
st.markdown("""
    <style>
    
    body {
        background-color: #1c1c1c;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #219C90;
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
        cursor: pointer;
    }
    .stSelectbox {
        background-color: #333;
        color: #fff;
        border-radius: 8px;
    }
    .stImage {
        border-radius: 10px;
    }
    .stTextInput {
        border-radius: 12px;
        background-color: #333;
        color: white;
    }
    .movie-title {
        font-size: 18px;
        font-weight: bold;
        text-align: center;
    
    }
    .movie-poster {
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🎬 CineQuest")

# Dropdown menu for movie selection
selectvalue = st.selectbox("Select a movie to get recommendations", movies_list, key="movie_select")

# Function to fetch poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    
    # Return a placeholder image if the movie poster is not available
    return "https://via.placeholder.com/500x750?text=No+Poster"

# Function to get recommendations
def recommend(movie):
    index = movies[movies['original_title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []

    for i in distances[1:6]:  # Top 5 recommendations
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].original_title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters

# Show recommendations on button click
if st.button("Show Recommendations", key="recommend_button"):
    movie_names, movie_posters = recommend(selectvalue)
    
    cols = st.columns(5)
    
    for idx, col in enumerate(cols):
        with col:
            # Debugging: Print the URLs to ensure they are correct
           
            
            st.text(movie_names[idx])
            st.image(movie_posters[idx], width=150, use_column_width=True)

# Make sure to replace 'YOUR_API_KEY' with your actual TMDb API key.
