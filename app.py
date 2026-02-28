import pickle
import streamlit as st
import requests
import base64
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: contain;
             background-repeat: no-repeat;
            background-position: center center;
            background-attachment: fixed;
            background-size: 100% 100%;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call function
set_background("background.jpg")

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


st.markdown(
    "<h2 style='text-align: center;'>🎬 Movie Recommender System</h1>",
    unsafe_allow_html=True
)
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
st.markdown(
    "<h4 style='text-align: center; font-size: 21px;'>Type or select a movie from the dropdown</h3>",
    unsafe_allow_html=True
)

selected_movie = st.selectbox(
    "",
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



