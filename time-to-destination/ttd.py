#!/usr/bin/python3
import time
import Adafruit_CharLCD as LCD
import requests

# API key for accessing Google Distance Matric API
api_key =  'YOUR_API_KEY'
base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

# Addesses to find the estimated travel times
origin = 'Papakura,Auckland,New+Zealand'
destination = 'Penrose,Auckland,New+Zealand'

# Raspberry Pi pin config
lcd_rs = 4
lcd_en = 17
lcd_d4 = 25
lcd_d5 = 24
lcd_d6 = 23
lcd_d7 = 18

# LCD column and row size 
lcd_columns = 20
lcd_rows    = 4

# Initialize the LCD using the pins above
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

# Function to get traffic and historic data based commute time
def get_data():
    try:
        # Make request to get best guess duration between specified two points
        r1 = requests.get(base_url+'origins={}&destinations={}&departure_time={}&traffic_model={}&key={}'.format(origin, destination, time_in_seconds_UTC(), 'best_guess', api_key))
        r1= r1.json()['rows'][0]['elements'][0] # Convert the response to JSON
        best_guess_duration = r1['duration_in_traffic']['text']

        # Make request to get worst case duration between specified two points
        r2 = requests.get(base_url+'origins={}&destinations={}&departure_time={}&traffic_model={}&key={}'.format(origin, destination, time_in_seconds_UTC(), 'pessimistic', api_key))
        r2 = r2.json()['rows'][0]['elements'][0] # Convert the response to JSON
        pessimistic_duration = r2['duration_in_traffic']['text']

        display('Estimated Drive Time', 'BG: ' + best_guess_duration, 'PSMT: ' + pessimistic_duration, human_readable_time()) # Pass the results to display function
    except requests.exceptions.RequestException as e:
        # Print time when exception happened and exception meyyssage
        print(time.strftime("%d-%m-%Y %H:%M:%S", time.localtime()))
        print(e)
        display('Error, check console', 'Trying again...') # Update LCD with error message

def time_in_seconds_UTC():
    return int(round(time.time()))

def human_readable_time():
    return time.strftime("%d %b %Y %I:%M %P", time.localtime())
    
def display(line1 = '', line2 = '', line3 = '', line4 = ''):
    lcd.clear() # Clear the display
    lcd.home() # Bring cursor to row 1 and column 1
    lcd.message(line1 + '\n' + line2 + '\n' + line3 + '\n' + line4) # Print message

def main():
    display('Loading...')
    get_data() # Gets and displays data on LCD
    time.sleep(60) # Wait for 1 minute

# Keep the program running and update LCD every 1 minute
while True:
    try:
        main()
    finally:
        display('Stopped')
