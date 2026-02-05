import streamlit as st
import pandas as pd  # Helps you analyze big data
import numpy as py  # Use of functions such as maximum()
import matplotlib.pyplot as plt  # Allows you to make charts
import pydeck as pdk  # Allows you to make maps


# Read data
def read_data():
    df = pd.read_csv('../../BigBelly/big-belly-alerts-2014_7000_sample.csv')  # Import .csv file as our data frame
    return df


# Filter data by fullness colors
def filter_data_by_color(df, color):
    return df[df['fullness'] == color.upper()]


# Create a list of descriptions to use for a multiselect function on a streamlit sidebar
def all_desc():
    df = read_data()  # Get our data frame
    lst = []
    for ind, row in df.iterrows():  # Iterate through each row
        if row['description'] not in lst:  # If description not in list
            lst.append(row['description'])  # We append the description

    return lst


# Count frequency of address descriptions
def count_desc(descriptions, df):
    lst = [df.loc[df['description'].isin([description])].shape[0] for description in descriptions]  # Call all the
    # descriptions and check if it is in the one specific description. Shape gets the size of each data frame list.
    # List iteration.
    return lst


# Create pie chart
def pie_chart(counts, sel_descriptions):
    plt.figure()

    if counts:
        maximum = counts.index(py.max(counts))  # Find the max using numpy package
        explodes = [0.25 if i == maximum else 0 for i in range(len(counts))]  # How far from the center the piece of
        # the pie explodes
    else:
        explodes = []  # Handle the case when counts is empty

    plt.pie(counts, labels=sel_descriptions, explode=explodes, autopct='%.2f')  # Creates pie chart
    plt.title(f"% Visits by Address: {', '.join(sel_descriptions)}")  # Pie chart title
    return plt


# "cool" Split location column into latitude and longitude. This was one of the hardest parts about this project
def split_loc(lat_long):
    loc = lat_long.split(', ')  # Split location at the comma
    lat = float(loc[0].lstrip('"('))  # Takes the first number in the series aka lat and removes the unnecessary
    # punctuation
    long = float(loc[1].rstrip(')"'))  # Takes the second number in the series aka long and removes the unnecessary
    # punctuation
    return lat, long


# Create a map
def generate_map(df):
    map_df = df.filter(['description', 'location'])  # Create new data frame that only looks at description and location
    map_df['lat'], map_df['long'] = zip(*map_df['location'].apply(split_loc))  # "zip" which unpacks the resulting tuple of latitudes and longitudes into separate columns.

    # Watched the video on the CIS sandbox website to create this
    view_state = pdk.ViewState(
        latitude=map_df["lat"].mean(),
        longitude=map_df["long"].mean(),
        zoom=10,
        pitch=0)

    layer = pdk.Layer('ScatterplotLayer',
                      data=map_df,
                      get_position='[long, lat]',
                      get_radius=70,
                      get_color=[0, 0, 255],
                      pickable=True)

    tool_tip = {"html": "Big Belly Alerts:<br/> <b>{description}</b> ",
                "style": {"backgroundColor": "steelblue",
                          "color": "white"}}

    style = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', initial_view_state=view_state, layers=[layer],
                     tooltip=tool_tip)

    st.pydeck_chart(style)


# Create bar chart
def bar_chart1(counts, sel_descriptions):
    plt.figure(figsize=(10, 6))  # Figure size
    plt.bar(sel_descriptions, counts, color='teal')  # Creates bar chart
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
    plt.xlabel('Description')  # X axis
    plt.ylabel('Count')  # Y axis
    plt.title(f"Counts by Description for {', '.join(sel_descriptions)}")  # Bar chart title
    return plt


# A dictionary mapping fullness colors to actual colors
fullness_colors = {
        'GREEN': 'green',
        'YELLOW': 'yellow',
        'RED': 'red'
    }


# Create another bar chart
def bar_chart2(counts):
    plt.figure(figsize=(10, 6))  # Figure size
    colors = [fullness_colors[color] for color in counts.index]  # Map fullness colors to actual colors
    plt.bar(counts.index, counts, color=colors)  # Creates bar chart
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
    plt.xlabel('Fullness')  # X axis
    plt.ylabel('Count')  # Y axis
    plt.title("Counts by Fullness")  # Bar chart title
    return plt


def main():
    df = read_data()

    st.title("Big Belly Alerts & Locations")  # Title
    st.write("Welcome to this 2014 Big Belly Alert data. Open the sidebar to begin!")  # Subtitle

    st.sidebar.write("Please choose certain options to display their data.")  # Sidebar
    descriptions = st.sidebar.multiselect("Select a description: ", all_desc())  # Multiselect

    selected_color = st.sidebar.radio("Select a color as an attribute of fullness:", ['Green', 'Yellow', 'Red'])  #
    # Radio button for selecting a color

    data = filter_data_by_color(df, selected_color)  # Filter data based on color
    series = count_desc(descriptions, data)

    st.write("View a map of Big Belly Alert locations!")
    generate_map(df)

    st.write("View a pie chart. Make sure to select one or more descriptions!")
    st.pyplot(pie_chart(series, descriptions))

    st.write("View a bar chart. Make sure to select one or more descriptions!")
    st.pyplot(bar_chart1(series, descriptions))

    st.write("View a bar chart. Make sure to select one or more descriptions!")
    fullness_counts = df['fullness'].value_counts()  # Obtain the counts of each 'fullness' color
    plt_chart = bar_chart2(fullness_counts)
    st.pyplot(plt_chart)


main()
