# -----------------------------------------------------------------------------     
# Purpose:  CS 122 Mini Project 3
#           Create dashboard displaying current weather, 5 day forecast, and
#           5 day/3 hour forecast for user inputted city 
#
#           Using "Current Weather API" (http://openweathermap.org/current)
#           and "5 days/3hour Forecast API" (http://openweathermap.org/forecast5)
#
# Author:   Michelle Lai
# Date:     March 16, 2018
# -----------------------------------------------------------------------------


from flask import Flask, render_template, redirect, request
import pandas as pd
import weather_functions

app = Flask(__name__)

@app.route('/')  # when route ends with /
def main():
    """
    Redirect the default route (/) to /index
    :return: redirection to the correct route, /index
    """
    return redirect('/index')  # redirect /index
 
@app.route('/index')
def index():
    """
    Render the correct html template, index.html for the /index route
    Html template shows a form for user input
    :return: template, index.html, rendered for the user
    """
    return render_template('index.html')  # index.html has the form

@app.route('/weather', methods = ['POST', 'GET'])
def info():
    """
    Render the correct html template, weather.html for the /weather route
    Get the city name input from the form and generate the required data to display,
    for current forecast and five day forecast
    :return: template, weather.html, rendered for the user, with the display info
    """
    form_info = request.form  # get the form
    city = form_info['City']  # get the user inputted city name from the form
    current_forecast = weather_functions.weather_forecast(city)  # get the current forecast from the API
    five_day_forecast = weather_functions.weather_5_forecast(city)    
    info = weather_functions.create_info(current_forecast, five_day_forecast)
    info['City'] = city

    return render_template('weather.html', info = info) 

@app.errorhandler(404)
def page_not_found(e):
    """
    Handle the 404 error by rendering the correct html template, 404.html
    Error is for an incorrect route being submitted
    :return: template, 404.html, rendered for the error display to the user
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """
    Handle the 500 error by rendering the correct html template, 500.html
    Error is for internal server problems
    :return: template, 500.html, rendered for the error display to the user
    """
    return render_template('500.html')
	
if __name__ == '__main__':
    app.debug = True	
    app.run(port=33507)