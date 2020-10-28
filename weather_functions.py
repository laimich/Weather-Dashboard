# -----------------------------------------------------------------------------     
# Purpose:  CS 122 Mini Project 3
#           Gather weather information for user inputted city to display
#           current weather's temperature and 5 day graphs
#
#           Using "Current Weather API" (http://openweathermap.org/current)
#           and "5 days/3hour Forecast API" (http://openweathermap.org/forecast5)
#           Icon images for current weather from (http://openweathermap.org/weather-conditions)           
#
# Author:   Michelle Lai
# Date:     March 16, 2018
# -----------------------------------------------------------------------------

import requests
import pandas as pd
import json
from pandas.io.json import json_normalize 
import re
import matplotlib.pyplot as plt
import seaborn as sns


def weather_forecast(city):
    """
    Get json data for the city using "Current Weather API"
    (http://openweathermap.org/current)
    :param
    city (string) name of the city to search
    :return: json for the data of the city's current weather 
    """
    params = { 'q'        : city, 
               'APPID': 'enter your api id here', 
             }
    # get data from the user inputted city, using "Current Weather API"
    res = requests.get('http://api.openweathermap.org/data/2.5/weather', params=params)
    return res.json()


def weather_5_forecast(city):
    """
    Get json data for the city using "5 days/3 hour Forecast API" 
    (http://openweathermap.org/forecast5)
    :param
    city (string) name of the city to search
    :return: json for the data of the city's 5 day/3 hour weather forecast
    """
    params = { 'q'        : city, 
               'APPID': 'enter your api id here', 
             }
    # get data from the user inputted city, using "5 days/3hour Forecast"
    res = requests.get('http://api.openweathermap.org/data/2.5/forecast', params=params)
    return res.json()

def create_info(current, five_day):
    """
    Create dictionary for the information needed to be displayed
    Information includes current weather's temperature and image name
    Saves 5 day forecast information through another method
    :param
    current (json) data for the city's current weather
    five_day (json) data for the city's five day forecast
    :return: dictionary with current weather's temperature and image name
    """
    # get the temperature from the current forecast
    current_temp_K = current['main']['temp'] 
    # convert temperature to C from K
    current_temp_C = current_temp_K - 273.15
    current_temp_C = int(round(current_temp_C))
    # get the current weather's id, for displaying the correct icon
    current_id = current['weather'][0]['id']
    # using the weather's id, get the name of the matching image
    current_image = get_match_image(current_id)

    # get the data needed from five day, date/time and temperature
    # plots data into graph, which is saved as "graph_five_day"
    save_five_day_graph(five_day)

    # return a list with the current's data, temperature and image name
    # five day's data is already saved as a graph image
    return {"Temp": current_temp_C, "Image": current_image}

def get_match_image(weather_id):
    """
    Get the matching image name for the assigned weather forecast id
    Images and id matching categories from (http://openweathermap.org/weather-conditions)
    :param
    weather_id (int) id assigned to represent the type of weather
    :return: string that represents the name for the id's matching image
    """
    if weather_id == 800:
        # set image as "clear sky"
        image_name = "01d"
    elif weather_id == 801:
        # set image as "few clouds"
        image_name = "02d"
    elif weather_id == 802:
        # set image as "scattered clouds"
        image_name = "03d"
    elif weather_id in [803,804]:
        # set image as "broken clouds"
        image_name = "04d"
    elif weather_id in [300,301,302,310,311,312,313,314,321,520,521,522,531]:
        # set image as "shower rain"
        image_name = "09d"
    elif weather_id in [500,501,502,503,504]:
        # set image as "rain"
        image_name = "10d"
    elif weather_id in [200,201,202,210,211,212,221,230,231,232]:
        # set image as "thunderstorm"
        image_name = "11d"
    elif weather_id in [511,600,601,602,611,612,615,616,620,621,622]:
        # set image as "snow"
        image_name = "13d"
    elif weather_id in [701,711,721,731,741,751,761,762,771,781]:
        # set image as "mist"
        image_name = "50d"

    return image_name

def save_five_day_graph(forecast_5):
    """
    For the five day forecast, create the plot and save the graphs as images
    One graph is for the 5 day temperatures, another graph is for the 5 day/3 hour temperatures
    Images saved as "graph_five_day.png" and "graph_five_day_hour.png" respectively
    :param
    forecast_5 (json) data for the five day forecast
    """
    # get the needed data, date/time and temp, but temp in list
    df = json_normalize(forecast_5, 'list') # 0 = 38 rows, thus 39 rows, starts tomorrow @ 3AM to last day at 9PM
    # extract temp then put into new column
    df['Temperature'] = df[['main']].apply(temperature,axis=1)
    # extract only needed info from dt_txt (month, day, hour, minute), put into new columns
    df['Datetime'] = df[['dt_txt']].apply(date_time,axis=1)
    df['Date'] = df[['dt_txt']].apply(date,axis=1)
    df['Time'] = df[['dt_txt']].apply(time,axis=1)

    # save the new df as just columns needed for 5 day, date/time and temp
    df_keep = df[['Date', 'Time', 'Datetime', 'Temperature']]
    # group by date, get the avg temp per day (for all the times of that day)
    group = df_keep.groupby('Date').mean().reset_index()

    # for creating and styling the graph
    sns.set(font_scale=1.5)
    fig, ax = plt.subplots()
    # set size of plot (width, height)
    fig.set_size_inches(12, 6)
    # set x labels to be rotated
    plt.xticks(rotation=45)
    # create the 5 day graph
    sns.factorplot('Date', 'Temperature', data=group, ax=ax)
    # save plot as image in the static sub directory
    fig.savefig('static/graph_five_day.png', bbox_inches='tight')
    # create the second graph
    sns.set(font_scale=1.5)
    fig, ax = plt.subplots()
    # set size of plot (width, height)
    fig.set_size_inches(20, 10)
    # set x labels to be rotated
    plt.xticks(rotation=45)
    # create the 5 day/3 hour graph
    sns.factorplot('Datetime', 'Temperature', data=df_keep, ax=ax)
    # save plot as image in the static sub directory
    fig.savefig('static/graph_five_day_hour.png', bbox_inches='tight')

def temperature(main):
    """
    Extract the temperature column and convert it from Kelvin (K) to Celcius (C)
    :param
    main (Series) series containing a dictionary with the temperature data 
    :return: temperature converted to Celcius (C)
    """
    return main[0]['temp'] - 273.15

def date_time(dt_txt):
    """
    Extract the month, day, hour, and minute from the data containing the full date
    :param
    dt_txt (String) data representing the date and time
    :return: date (MM/DD) and time (HH:MM) in one string
    """
    # split by -, space, or :
    contents = re.split("[- :]", dt_txt[0])
    # only keep the month, day, hour and minute
    datetime = contents[1] + "/" + contents[2] + " at " + contents[3] + ":" + contents[4]  
    return datetime

def date(dt_txt):
    """
    Extract the month and day from the data containing the full date
    :param
    dt_txt (String) data representing the date and time
    :return: date (MM/DD) in one string
    """
    contents = re.split("[- :]", dt_txt[0])
    # only get the month and day
    date = contents[1] + "/" + contents[2]  
    return date

def time(dt_txt):
    """
    Extract hour and minute from the data containing the full date
    :param
    dt_txt (String) data representing the date and time
    :return: time (HH:MM) in one string
    """
    contents = re.split("[- :]", dt_txt[0])
    # only get the hour and minute
    time = contents[3] + ":" + contents[4]  
    return time
