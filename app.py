import pickle
import streamlit as st
import requests

@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a91241d81d4c5b78ff1c6f496a11df61&language=en-US"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("poster_path"):
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
        return "no_poster.png"

    except:
        return "no_poster.png"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('🎬Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button("Show Recommendation"):
    st.session_state.recommendations = recommend(selected_movie)

if "recommendations" in st.session_state:
    names, posters = st.session_state.recommendations
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])



