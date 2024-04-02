
# import streamlit as st
# import backend
# import pandas as pd
# import imdb
# import re

# ia = imdb.IMDb()

# @st.cache_data(show_spinner=False)
# def get_movie_image(movie_id):
#     movie = ia.get_movie(movie_id)
#     return movie['full-size cover url']

# @st.cache_data(show_spinner=False)
# def get_movie_info(movie_id):
#     movie = ia.get_movie(movie_id)
#     title = movie.get('title', 'N/A')
#     directors = ", ".join([director['name'] for director in movie.get('directors', [])])
#     writers = ", ".join([writer.get('name', 'N/A') for writer in movie.get('writers', [])[:1]])
#     stars = ", ".join([star['name'] for star in movie.get('cast', [])[:5]])
#     imdb_rating = movie.get('rating', 'N/A')
#     genre = ", ".join(movie.get('genres', ['N/A']))
#     runtime = movie.get('runtimes', ['N/A'])[0] if movie.get('runtimes') else 'N/A'
#     description = movie.get('plot outline', 'N/A')
#     return title, imdb_rating, genre, description, directors, writers, stars, runtime

# @st.cache_data(show_spinner=False)
# def split_into_sentences(text):
#     delimiters = ".", "!", "?"
#     regex_pattern = '|'.join(map(re.escape, delimiters))
#     sentences = re.split(regex_pattern, text)
#     sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
#     return sentences[:3]

# def findurl(genre, start_year=None, end_year=None, rating=None):
#     base_url = "https://www.imdb.com/search/title/?title_type=feature"
#     if genre:
#         base_url += f"&genres={genre.replace(' ', '+')}"
#     if start_year and end_year:
#         base_url += f"&release_date={start_year}-01-01,{end_year}-12-31"
#     if rating:
#         base_url += f"&user_rating={rating}"
#     return base_url

# genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western',""]

# st.markdown(
#     """
#     <style>
#     .sidebar .sidebar-content {
#         background-image: linear-gradient(#2e7bcf,#2e7bcf);
#         color: white;
#     }
#     .stApp {
#          background: #404040; /* Dark Grey */
#     }
#     .stMarkdown {
#         font-family: "Arial", sans-serif !important;
#         font-size: 16px;
#         color: white !important;
#     }
#     .heading {
#         font-family: Algerian;
#         color: white;
#         text-align: center;
#     }
#     </style>
# """,
#     unsafe_allow_html=True,
# )

# selected_genre = st.sidebar.selectbox("Select Genre:", genres)
# min_rating = st.sidebar.slider("Select Rating:", min_value=0.0, max_value=10.0, step=1.0)
# start_year = st.sidebar.slider("Select Start Year:", min_value=1980, max_value=2024)
# end_year = st.sidebar.slider("Select End Year:", min_value=1980, max_value=2024)

# st.markdown(
#     """
#     <div class='heading' style='color: white !important;'>
#         <h1 style='color: white;'>CineRecommend Wizard</h1>
#         <p>
#         Can't make up your mind with the plethora of movies accessible?
# </p>
#         <p>Answer four questions, and leave the decision-making to us!</p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# if end_year < start_year :
#     st.error("End year cannot be less than start year. Please select valid years.")
# elif not selected_genre:  
#     st.warning("Please select a genre.")
# else:
#     if st.sidebar.button("Suggest Movies"):
#         with st.spinner("Suggesting..."):  
#             imdb_url = findurl(selected_genre, start_year, end_year, min_rating)
#             df = backend.extractmovies(imdb_url)
            
#             num_movies = len(df)
#             if num_movies == 0:
#                 st.warning("No movies found.")
#             else:
               
#                 for index, row in df.iterrows():
#                     movie_id = row['id'][2:]
#                     
#                     title, imdb_rating, genre, description, directors, writers, stars, runtime = get_movie_info(movie_id)
#                     description_sentences = split_into_sentences(description)
#                     description_display = ' '.join(description_sentences)
                    
#                     st.markdown(
#                         f"""
#                         <div style='display: inline-block; margin: 10px; padding: 10px; border: 1px solid navy; border-radius: 10px; background-color: #f0f0f0 /* Light Grey */'>
#                             <h3><span style='color: black;'>{title}</span></h3>
#                             <img src="{get_movie_image(movie_id)}" style="width:250px;height:375px;">
#                             <div style='color: black;'>
#                                 <p><span style='font-weight: bold;'>IMDb Rating:</span> {imdb_rating}</p>
#                                 <p><span style='font-weight: bold;'>Genre:</span> {genre}</p>
#                                 <p><span style='font-weight: bold;'>Description:</span> {description_display}</p>
#                                 <p><span style='font-weight: bold;'>Directors:</span> {directors}</p>
#                                 <p><span style='font-weight: bold;'>Writers:</span> {writers}</p>
#                                 <p><span style='font-weight: bold;'>Stars:</span> {stars}</p>
#                                 <p><span style='font-weight: bold;'>Runtime:</span> {runtime} minutes</p>
#                             </div>
#                         </div>
#                         """,
#                         unsafe_allow_html=True
#                     )






import streamlit as st
import backend
import pandas as pd
import imdb
import re

ia = imdb.IMDb()

@st.cache_data(show_spinner=False)
def get_movie_image(movie_id):
    movie = ia.get_movie(movie_id)
    return movie['full-size cover url']

@st.cache_data(show_spinner=False)
def get_movie_info(movie_id):
    movie = ia.get_movie(movie_id)
    title = movie.get('title', 'N/A')
    directors = ", ".join([director['name'] for director in movie.get('directors', [])])
    writers = ", ".join([writer.get('name', 'N/A') for writer in movie.get('writers', [])[:1]])
    stars = ", ".join([star['name'] for star in movie.get('cast', [])[:5]])
    imdb_rating = movie.get('rating', 'N/A')
    genre = ", ".join(movie.get('genres', ['N/A']))
    runtime = movie.get('runtimes', ['N/A'])[0] if movie.get('runtimes') else 'N/A'
    description = movie.get('plot outline', 'N/A')
    return title, imdb_rating, genre, description, directors, writers, stars, runtime

@st.cache_data(show_spinner=False)
def split_into_sentences(text):
    delimiters = ".", "!", "?"
    regex_pattern = '|'.join(map(re.escape, delimiters))
    sentences = re.split(regex_pattern, text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences[:3]

def findurl(genre, start_year=None, end_year=None):
    base_url = "https://www.imdb.com/search/title/?title_type=feature"
    if genre:
        base_url += f"&genres={genre.replace(' ', '+')}"
    if start_year and end_year:
        base_url += f"&release_date={start_year}-01-01,{end_year}-12-31"
    return base_url

genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western', ""]

st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
    }
    .stApp {
         background: #404040; /* Dark Grey */
    }
    .stMarkdown {
        font-family: "Arial", sans-serif !important;
        font-size: 16px;
        color: white !important;
    }
    .heading {
        font-family: Algerian;
        color: white;
        text-align: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)

selected_genre = st.sidebar.selectbox("Select Genre:", genres)
start_year = st.sidebar.slider("Select Start Year:", min_value=1980, max_value=2024)
end_year = st.sidebar.slider("Select End Year:", min_value=1980, max_value=2024)

st.markdown(
    """
    <div class='heading' style='color: white !important;'>
        <h1 style='color: white;'>CineRecommend Wizard</h1>
        <p>
        Can't make up your mind with the plethora of movies accessible?
</p>
        <p>Answer three questions, and leave the decision-making to us!</p>
    </div>
    """,
    unsafe_allow_html=True
)

if end_year < start_year:
    st.error("End year cannot be less than start year. Please select valid years.")
elif not selected_genre:  
    st.warning("Please select a genre.")
else:
    if st.sidebar.button("Suggest Movies"):
        with st.spinner("Suggesting..."):  
            imdb_url = findurl(selected_genre, start_year, end_year)
            df = backend.extractmovies(imdb_url)
            
            num_movies = len(df)
            if num_movies == 0:
                st.warning("No movies found.")
            else:
                for index, row in df.iterrows():
                    movie_id = row['id'][2:]
                    if not movie_id:
                        continue  # Skip this movie if movie_id is not valid
                    
                    title, imdb_rating, genre, description, directors, writers, stars, runtime = get_movie_info(movie_id)
                    description_sentences = split_into_sentences(description)
                    description_display = ' '.join(description_sentences)
                    
                    st.markdown(
                        f"""
                        <div style='display: inline-block; margin: 10px; padding: 10px; border: 1px solid navy; border-radius: 10px; background-color: #f0f0f0 /* Light Grey */'>
                            <h3><span style='color: black;'>{title}</span></h3>
                            <img src="{get_movie_image(movie_id)}" style="width:250px;height:375px;">
                            <div style='color: black;'>
                                <p><span style='font-weight: bold;'>IMDb Rating:</span> {imdb_rating}</p>
                                <p><span style='font-weight: bold;'>Genre:</span> {genre}</p>
                                <p><span style='font-weight: bold;'>Description:</span> {description}</p>
                                <p><span style='font-weight: bold;'>Directors:</span> {directors}</p>
                                <p><span style='font-weight: bold;'>Writers:</span> {writers}</p>
                                <p><span style='font-weight: bold;'>Stars:</span> {stars}</p>
                                <p><span style='font-weight: bold;'>Runtime:</span> {runtime} minutes</p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )






