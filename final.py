import numpy as np
import csv
import streamlit as st
import pydeck as pdk
import pandas as pd
import mapbox as mb
import matplotlib.pyplot as plt

# heading with pink background and white text using HTML
st.markdown(
    """<p style="text-align:center; background-color: #FC89D8; color: white;">
    Name: Angie Leigh <br>
    CS230: Section SN5 <br>
    Data: McDonald's <br>
    URL: Link to your web application online (see extra credit) <br>
    Description: This program allows the user to analyze McDonald's locations by location, feature, and/or store type using maps, bar graphs, and pie charts.  </p>
    """,
    unsafe_allow_html=True,
)

# fun rainbow title using HTML
Title_html = """
    <style>
        .title h1{
          user-select: none;
          text-align: center;
          font-size: 43px;
          color: white;
          background: repeating-linear-gradient(-45deg, red 0%, yellow 7.14%, rgb(0,255,0) 14.28%, rgb(0,255,255) 21.4%, cyan 28.56%, blue 35.7%, magenta 42.84%, red 50%);
          background-size: 600vw 600vw;
          -webkit-text-fill-color: transparent;
          -webkit-background-clip: text;
          animation: slide 10s linear infinite forwards;
        }
        @keyframes slide {
          0%{
            background-position-x: 0%;
          }
          100%{
            background-position-x: 600vw;
          }
        }
    </style> 
    
    <div class="title">
        <h1>McDonald's Locations</h1>
    </div>
    """
st.markdown(Title_html, unsafe_allow_html=True)


# read in data from file into data frame and return df
def read_data(file):
    df = pd.read_csv(file)
    return df


# show table of passed in df
def show_data(df):
    st.write(df)


# 4 options for filtering the passed in df which are mutually inclusive
def widgets(df):
    st.sidebar.write("Filter Options")
    # filter by city, allow lowercase input
    city = st.sidebar.text_input("Enter your city: ").upper()
    # make list of all cities in df then check if input is valid
    cities = df['city'].tolist()
    if city in cities:
        st.sidebar.write("That city is valid.")
        # update df
        is_city = df['city'] == city
        df = df[is_city]
    else:
        st.sidebar.write("That city is not valid!")

    # filter by state, allow lowercase input
    state = st.sidebar.text_input("Enter your state: ").upper()
    # make list of all states in df then check if input is valid
    states = df['state'].tolist()
    if state in states:
        st.sidebar.write("That state is valid.")
        # update df
        is_state = df['state'] == state
        df = df[is_state]
    else:
        st.sidebar.write("That state is not valid!")

    # filter by feature
    st.sidebar.write("Features:")
    playplace = st.sidebar.checkbox("Play Place", False)
    drivethru = st.sidebar.checkbox("Drive Thru", False)
    archcard = st.sidebar.checkbox("Arch Card", False)
    freewifi = st.sidebar.checkbox("Free Wi-Fi", False)

    # update df
    if playplace:
        is_play = df['playplace'] == 'Y'
        df = df[is_play]
    if drivethru:
        is_drive = df['driveThru'] == 'Y'
        df = df[is_drive]
    if archcard:
        is_arch = df['archCard'] == 'Y'
        df = df[is_arch]
    if freewifi:
        is_free = df['freeWifi'] == 'Y'
        df = df[is_free]

    # count number of stores with each feature
    playCount = len(df[df['playplace'] == 'Y'])
    driveCount = len(df[df['driveThru'] == 'Y'])
    archCount = len(df[df['archCard'] == 'Y'])
    wifiCount = len(df[df['freeWifi'] == 'Y'])

    # create lists to be graphed
    x = ['playPlace', 'driveThru', 'archCard', 'freeWifi']
    y = [playCount, driveCount, archCount, wifiCount]

    # count number of stores of each type
    freeCount = len(df[df['storeType'] == 'FREESTANDING'])
    sharedCount = len(df[df['storeType'] == 'SHARED BLDNG'])
    gasCount = len(df[df['storeType'] == 'GAS STATION'])
    hospitalCount = len(df[df['storeType'] == 'HOSPITAL'])
    walCount = len(df[df['storeType'] == 'WAL*MART'])
    busCount = len(df[df['storeType'] == 'BUS/TRAIN'])
    mallCount = len(df[df['storeType'] == 'MALL'])
    tollCount = len(df[df['storeType'] == 'TOLLWAY'])
    storeCount = len(df[df['storeType'] == 'STOREFRONT'])
    airCount = len(df[df['storeType'] == 'AIRPORT'])

    # create lists to be graphed
    x2 = ['FREESTANDING', 'SHARED BLDNG', 'GAS STATION', 'HOSPITAL', 'WAL*MART', 'BUS/TRAIN', 'MALL', 'TOLLWAY',
          'STOREFRONT', 'AIRPORT']
    y2 = [freeCount, sharedCount, gasCount, hospitalCount, walCount, busCount, mallCount, tollCount, storeCount,
          airCount]

    # graph options
    st.sidebar.write("Chart Options")
    charts = ['Features Pie Chart', 'Features Bar Graph', 'Store Type Pie Chart', 'Store Type Bar Graph']
    chart = st.sidebar.radio("Select a graph: ", charts)

    # call functions (must be done here, not earlier, so that it is updated with user selections)
    show_data(df)
    map_data(df)

    # graph data if it can be graphed based on user selection
    if len(df) > 0:
        if chart == 'Features Pie Chart':
            pie_plot(x, y, "What features do McDonald's have?")
        elif chart == 'Store Type Pie Chart':
            pie_plot(x2, y2, "What kinds of stores are these?")
        elif chart == 'Features Bar Graph':
            bar_plot(x, y, "What features do McDonald's have?", "Features")
        elif chart == 'Store Type Bar Graph':
            bar_plot(x2, y2, "What kinds of stores are these?", "Kind")


# map data from passed in df
def map_data(df):
    # fun rainbow title using HTML
    Title_html = """
    <style>
        .title h1{
          user-select: none;
          text-align: center;
          font-size: 43px;
          color: white;
          background: repeating-linear-gradient(-45deg, red 0%, yellow 7.14%, rgb(0,255,0) 14.28%, rgb(0,255,255) 21.4%, cyan 28.56%, blue 35.7%, magenta 42.84%, red 50%);
          background-size: 600vw 600vw;
          -webkit-text-fill-color: transparent;
          -webkit-background-clip: text;
          animation: slide 10s linear infinite forwards;
        }
        @keyframes slide {
          0%{
            background-position-x: 0%;
          }
          100%{
            background-position-x: 600vw;
          }
        }
    </style> 
    
    <div class="title">
        <h1>Map</h1>
    </div>
    """
    st.markdown(Title_html, unsafe_allow_html=True)

    # map coordinates
    df = pd.DataFrame({'lat': df['Y'], 'lon': df['X']})
    st.map(df)

    # fun rainbow title using HTML
    Title_html = """
    <style>
        .title h1{
          user-select: none;
          text-align: center;
          font-size: 43px;
          color: white;
          background: repeating-linear-gradient(-45deg, red 0%, yellow 7.14%, rgb(0,255,0) 14.28%, rgb(0,255,255) 21.4%, cyan 28.56%, blue 35.7%, magenta 42.84%, red 50%);
          background-size: 600vw 600vw;
          -webkit-text-fill-color: transparent;
          -webkit-background-clip: text;
          animation: slide 10s linear infinite forwards;
        }
        @keyframes slide {
          0%{
            background-position-x: 0%;
          }
          100%{
            background-position-x: 600vw;
          }
        }
    </style> 
    
    <div class="title">
        <h1>Map with Tooltips</h1>
    </div>
    """
    st.markdown(Title_html, unsafe_allow_html=True)

    # create parts for map with tool tips
    view_state = pdk.ViewState(
        latitude=df["lat"].mean(),
        longitude=df["lon"].mean(),
        zoom=15,
        pitch=0)
    layer1 = pdk.Layer('ScatterplotLayer',
                       df,
                       get_position='[lon, lat]',
                       get_radius=150,
                       get_color=[255, 77, 198],
                       pickable=True
                       )
    tool_tip = {"html": "Address:<br/> <b>{address}</b> ",
                "style": {"backgroundColor": "pink",
                          "color": "white"}
                }
    MAPKEY = "pk.eyJ1IjoiYW5naWVsZWlnaCIsImEiOiJja2lqb2loeWEwMXhqMnZqejlzMmgwczRsIn0.Fqspp_wwMHKa1YH2fx6wvA"
    map1 = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        mapbox_key=MAPKEY,
        layers=[layer1],
        tooltip=tool_tip
    )

    # map df with tool tips if it can be graphed
    if len(df) > 0:
        st.pydeck_chart(map1)
    else:
        st.write("No data!")


# create bar plot from passed in data
def bar_plot(x, y, title, xlabel):
    # fun rainbow title using HTML
    Title_html = """
    <style>
        .title h1{
          user-select: none;
          text-align: center;
          font-size: 43px;
          color: white;
          background: repeating-linear-gradient(-45deg, red 0%, yellow 7.14%, rgb(0,255,0) 14.28%, rgb(0,255,255) 21.4%, cyan 28.56%, blue 35.7%, magenta 42.84%, red 50%);
          background-size: 600vw 600vw;
          -webkit-text-fill-color: transparent;
          -webkit-background-clip: text;
          animation: slide 10s linear infinite forwards;
        }
        @keyframes slide {
          0%{
            background-position-x: 0%;
          }
          100%{
            background-position-x: 600vw;
          }
        }
    </style> 
    
    <div class="title">
        <h1>Bar Graph</h1>
    </div>
    """
    st.markdown(Title_html, unsafe_allow_html=True)

    # plot with specifications
    plt.bar(x, y, align='center', color='mediumspringgreen', edgecolor='white', linewidth=3)
    plt.xticks(rotation=45)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Count")
    st.pyplot(plt)
    return plt


# create pie chart from passed in data
def pie_plot(x, y, title):
    # fun rainbow title using HTML
    Title_html = """
    <style>
        .title h1{
          user-select: none;
          text-align: center;
          font-size: 43px;
          color: white;
          background: repeating-linear-gradient(-45deg, red 0%, yellow 7.14%, rgb(0,255,0) 14.28%, rgb(0,255,255) 21.4%, cyan 28.56%, blue 35.7%, magenta 42.84%, red 50%);
          background-size: 600vw 600vw;
          -webkit-text-fill-color: transparent;
          -webkit-background-clip: text;
          animation: slide 10s linear infinite forwards;
        }
        @keyframes slide {
          0%{
            background-position-x: 0%;
          }
          100%{
            background-position-x: 600vw;
          }
        }
    </style> 
    
    <div class="title">
        <h1>Pie Chart</h1>
    </div>
    """
    st.markdown(Title_html, unsafe_allow_html=True)

    # plot with specifications
    plt.pie(y, labels=x)
    plt.legend()
    plt.title(title)
    st.pyplot(plt)


# main program
def main():
    # get df
    df = read_data("mcdonalds_clean.csv")
    # call widgets, pass in df
    widgets(df)
    # 2 blank lines
    st.write("\n")
    st.write("\n")
    # picture and text linking to McDonald's website
    st.markdown("## Feeling hungry?")
    st.markdown(
        """<a style='display: block; font-size: 20px; color: #FFC300; text-align: center;' href="https://www.mcdonalds.com/us/en-us.html"> <img src="https://logos-world.net/wp-content/uploads/2020/04/McDonalds-Logo-700x394.png">Click for McDonald's Website</a>
        """,
        unsafe_allow_html=True,
    )


# run
main()
