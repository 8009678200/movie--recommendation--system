import streamlit as st
import pickle

# Page Config
st.set_page_config(
    page_title="AI Movie Recommendation",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
.big-title {
    text-align: center;
    color: #00BFFF;
    font-size: 50px;
    font-weight: bold;
}
.movie-card {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    color: white;
    border-left: 5px solid #00BFFF;
}
</style>
""", unsafe_allow_html=True)

# Load Data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
import requests

def fetch_poster(movie_id):
    api_key = "YOUR_TMDB_API_KEY"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"

    data = requests.get(url).json()

    poster_path = data['poster_path']

    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

    return full_path

# Recommendation Function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for i in movies_list:
        recommended_movies.append(
            movies.iloc[i[0]].title
        )

    return recommended_movies
    # Sidebar
with st.sidebar:
    st.header("🎬 Movie Recommender")
    st.write("Find movies similar to your favorite movies.")

    st.markdown("---")

    st.info("""
    AI Movie Recommendation System

    Developed By:
    Swati Kosta
    """)

# Title
st.markdown(
    "<h1 class='big-title'>🎬 AI Movie Recommendation System</h1>",
    unsafe_allow_html=True
)

st.write("Find movies similar to your favorite ones!")

selected_movie = st.selectbox(
    "🎥 Select a Movie",
    movies['title'].values
)


st.image(
    "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba",
    width=250
)

if st.button("🚀 Recommend"):
    recommendations = recommend(selected_movie)
    st.success("🎉 Recommendations:")

    st.subheader("Recommended Movies")
    cols = st.columns(5)

    for idx, movie in enumerate(recommendations):
        with cols[idx]:
            st.success(movie)

    for movie in recommendations:
        st.markdown(
            f"""
            <div class="movie-card">
                ⭐ {movie}
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")
st.markdown(
    "<center>Developed by <b>Swati Kosta</b> | AI/ML Project</center>",
    unsafe_allow_html=True
)
