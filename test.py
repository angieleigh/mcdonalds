import numpy as np
import csv
import streamlit as st
import pydeck as pdk
import pandas as pd
# import mapbox as mb
import matplotlib.pyplot as plt

# """
# Name: Angie Leigh \n
# CS230: Section SN5 \n
# Data: McDonald's \n
# URL: Link to your web application online (see extra credit)
#
# Description: This program ... (a few sentences about your program and the queries and charts)
# """

st.markdown(
    """<p style="text-align:center; background-color: #FC89D8; color: white;">
    Name: Angie Leigh <br>
    CS230: Section SN5 <br>
    Data: McDonald's <br>
    URL: Link to your web application online (see extra credit) <br>
    Description: This program ... (a few sentences about your program and the queries and charts)  </p>
    """,
    unsafe_allow_html=True,
)

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


def read_data(file):
    df = pd.read_csv(file)
    return df


def show_data(df):
    st.write(df)


def widgets(df):
    st.sidebar.write("Filter Options")
    city = st.sidebar.text_input("Enter your city: ").upper()
    cities = df['city'].tolist()
    if city in cities:
        st.sidebar.write("That city is valid.")
        is_city = df['city'] == city
        df = df[is_city]
    else:
        st.sidebar.write("That city is not valid!")

    state = st.sidebar.text_input("Enter your state: ").upper()
    states = df['state'].tolist()
    if state in states:
        st.sidebar.write("That state is valid.")
        is_state = df['state'] == state
        df = df[is_state]
    else:
        st.sidebar.write("That state is not valid!")

    st.sidebar.write("Features:")
    playplace = st.sidebar.checkbox("Play Place", False)
    drivethru = st.sidebar.checkbox("Drive Thru", False)
    archcard = st.sidebar.checkbox("Arch Card", False)
    freewifi = st.sidebar.checkbox("Free Wi-Fi", False)

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

    playCount = len(df[df['playplace'] == 'Y'])
    driveCount = len(df[df['driveThru'] == 'Y'])
    archCount = len(df[df['archCard'] == 'Y'])
    wifiCount = len(df[df['freeWifi'] == 'Y'])

    x = ['playPlace', 'driveThru', 'archCard', 'freeWifi']
    y = [playCount, driveCount, archCount, wifiCount]

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

    x2 = ['FREESTANDING', 'SHARED BLDNG', 'GAS STATION', 'HOSPITAL', 'WAL*MART', 'BUS/TRAIN', 'MALL', 'TOLLWAY', 'STOREFRONT', 'AIRPORT']
    y2 = [freeCount, sharedCount, gasCount, hospitalCount, walCount, busCount, mallCount, tollCount, storeCount, airCount]

    show_data(df)
    map_data(df)
    # pie_plot(x, y, "What features do McDonald's have?")
    pie_plot(x2, y2, "What kinds of stores are these?")
    # bar_plot(x, y, "What features do McDonald's have?", "Features")
    # bar_plot(x2, y2, "What kinds of stores are these?", "Kind")


def map_data(df):
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

    df = pd.DataFrame({'lat': df['Y'], 'lon': df['X']})
    st.map(df)

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

    if len(df) > 0:
        st.pydeck_chart(map1)
    else:
        st.write("No data!")


def bar_plot(x, y, title, xlabel):
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

    plt.bar(x, y, align='center', color='mediumspringgreen', edgecolor='white', linewidth=3)
    plt.xticks(rotation=45)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Count")
    st.pyplot(plt)
    return plt


def pie_plot(x, y, title):
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

    plt.pie(y, labels=x)
    plt.legend()
    plt.title(title)
    st.pyplot(plt)


def main():
    df = read_data("mcdonalds_clean.csv")
    widgets(df)

    st.write("\n")
    st.write("\n")
    st.markdown("## Feeling hungry?")
    st.markdown(
        """<a style='display: block; font-size: 20px; color: #FFC300; text-align: center;' href="https://www.mcdonalds.com/us/en-us.html"> <img src="https://logos-world.net/wp-content/uploads/2020/04/McDonalds-Logo-700x394.png">Click for McDonald's Website</a>
        """,
        unsafe_allow_html=True,
    )


main()
