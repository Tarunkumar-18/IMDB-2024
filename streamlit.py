#cd "C:\Users\staru\Desktop\imdb project\stream_lit\env\Scripts".\Activate
#streamlit run "C:\Users\staru\Desktop\imdb project\stream_lit\env\Scripts\streamlit.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


st.title("IMDB 2024")
st.image("C:/Users/staru/Downloads/IMDB_Logo_2016.svg.png")  

df = pd.read_csv("c:/Users/staru/Desktop/imdb project/web_scrap/modified_file.csv")

st.sidebar.title("Navigation")
option = st.sidebar.radio(
    "Select a page:",
    [
        "Home",
        "Top 10 Movies by Rating and Voting Counts",
        "Genre Distribution",
        "Average Duration by Genre",
        "Voting Trends by Genre",
        "Rating Distribution",
        "Genre-Based Rating Leaders",
        "Most Popular Genres by Voting",
        "Duration Extremes",
        "Ratings by Genre",
        "Correlation Analysis"
    ]
)


def home_page():
    st.write("Welcome to the IMDB 2024 Dashboard!")
    st.write("You can navigate to different visualizations using the sidebar.")
    st.dataframe(df) 

def top_10_movies():
    unique_movies = df.drop_duplicates(subset='Title')
    top_movies = unique_movies[['Title', 'Rating', 'Votes']].sort_values(by=['Rating', 'Votes'], ascending=[False, False]).head(10)
    st.write("Top 10 Movies by Rating and Voting Counts:")
    st.dataframe(top_movies)


def genre_distribution():
    genre_counts = df['Genre'].value_counts()
    st.write("Genre Distribution (Bar Chart):")
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(x=genre_counts.index, y=genre_counts.values)
    plt.xticks(rotation=45)
    plt.xlabel('Genre')
    plt.ylabel('Count of Movies')
    st.pyplot(fig)

def avg_duration_by_genre():
    avg_duration = df.groupby('Genre')['Duration'].mean().sort_values(ascending=False)
    st.write("Average Duration by Genre (Horizontal Bar Chart):")
    fig = plt.figure(figsize=(10, 6))
    avg_duration.plot(kind='barh', color='skyblue')
    plt.xlabel('Average Duration (Minutes)')
    plt.ylabel('Genre')
    st.pyplot(fig)

def voting_trends_by_genre():
    avg_votes = df.groupby('Genre')['Votes'].mean()
    st.write("Voting Trends by Genre:")
    fig = plt.figure(figsize=(10, 6))
    avg_votes.plot(kind='bar', color='lightcoral')
    plt.xlabel('Genre')
    plt.ylabel('Average Voting Counts')
    st.pyplot(fig)

def rating_distribution():
    st.write("Rating Distribution (Histogram):")
    fig = plt.figure(figsize=(10, 6))
    sns.histplot(df['Rating'], kde=True, bins=20)
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    st.pyplot(fig)

def genre_rating_leaders():
    genre_rating = df.groupby('Genre').apply(lambda x: x.loc[x['Rating'].idxmax()])[['Title', 'Rating']]
    st.write("Top-Rated Movies by Genre:")
    st.dataframe(genre_rating)

def popular_genres_by_voting():
    genre_votes = df.groupby('Genre')['Votes'].sum()
    st.write("Most Popular Genres by Voting (Pie Chart):")
    fig = px.pie(genre_votes, names=genre_votes.index, values=genre_votes.values, title="Genres by Total Voting Counts")
    st.plotly_chart(fig)

def duration_extremes():
    filtered_df = df[df['Duration'] > 0]
    
    if filtered_df.empty:
        st.write("No movies with valid duration greater than 0 minutes.")
    else:
        shortest_movie = filtered_df.loc[filtered_df['Duration'].idxmin()]
        longest_movie = filtered_df.loc[filtered_df['Duration'].idxmax()]
        
        st.write("Shortest and Longest Movies:")
        st.write(f"Shortest Movie: {shortest_movie['Title']} ({shortest_movie['Duration']} minutes)")
        st.write(f"Longest Movie: {longest_movie['Title']} ({longest_movie['Duration']} minutes)")

def ratings_by_genre():
    genre_ratings = df.pivot_table(index='Genre', values='Rating', aggfunc='mean')
    st.write("Average Ratings by Genre:")
    fig = plt.figure(figsize=(10, 6))
    sns.heatmap(genre_ratings, annot=True, cmap="coolwarm", cbar=True)
    plt.ylabel('Genre')
    plt.title('Ratings by Genre')
    st.pyplot(fig)

def correlation_analysis():
    st.write("Correlation between Ratings and Voting Counts:")
    fig = plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Rating', y='Votes', hue='Genre', palette='Set1')
    plt.xlabel('Rating')
    plt.ylabel('Voting Counts')
    st.pyplot(fig)

if option == "Home":
    home_page()
elif option == "Top 10 Movies by Rating and Voting Counts":
    top_10_movies()
elif option == "Genre Distribution":
    genre_distribution()
elif option == "Average Duration by Genre":
    avg_duration_by_genre()
elif option == "Voting Trends by Genre":
    voting_trends_by_genre()
elif option == "Rating Distribution":
    rating_distribution()
elif option == "Genre-Based Rating Leaders":
    genre_rating_leaders()
elif option == "Most Popular Genres by Voting":
    popular_genres_by_voting()
elif option == "Duration Extremes":
    duration_extremes()
elif option == "Ratings by Genre":
    ratings_by_genre()
elif option == "Correlation Analysis":
    correlation_analysis()
