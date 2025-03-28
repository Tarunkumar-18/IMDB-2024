import streamlit as st
import pandas as pd

df = pd.read_csv("C:/Users/staru/Desktop/imdb project/web_scrap/modified_file.csv")

df['Duration'] = df['Duration'] * 60

st.title("Interactive Movie Filtering")

duration = st.selectbox("Select Duration (in Minutes)", ["< 60 min", "60-90 min", "> 90 min"])

rating = st.slider("Minimum IMDb Rating", 0.0, 10.0, 8.0, 0.1)

votes = st.number_input("Minimum Votes", min_value=0, value=10000, step=100)

genre = st.multiselect("Select Genre(s)", df['Genre'].unique())

def apply_filters(duration, rating, votes, genre):
    filtered_df = df.copy()

    if duration == "< 60 min":
        filtered_df = filtered_df[filtered_df['Duration'] < 60]
    elif duration == "60-90 min":
        filtered_df = filtered_df[(filtered_df['Duration'] >= 60) & (filtered_df['Duration'] <= 90)]
    else:
        filtered_df = filtered_df[filtered_df['Duration'] > 90]

    filtered_df = filtered_df[filtered_df['Rating'] >= rating]

    filtered_df = filtered_df[filtered_df['Votes'] >= votes]

    if genre:
        filtered_df = filtered_df[filtered_df['Genre'].isin(genre)]

    filtered_df = filtered_df.sort_values(by='Rating', ascending=False)

    return filtered_df

if st.button("Apply Filters"):
    filtered_df = apply_filters(duration, rating, votes, genre)

    if filtered_df.empty:
        st.write("No movies match the selected filters.")
    else:
        st.write(f"Showing {filtered_df.shape[0]} movies that match your criteria:")
        st.dataframe(filtered_df)
