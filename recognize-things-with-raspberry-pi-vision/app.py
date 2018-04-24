import RPi.GPIO as GPIO
import picamera
import Adafruit_CharLCD as LCD
import os.path
import time
import requests
import dropbox
import json

# Subscription Key for Vision API
subscription_key = 'YOUR_SUBSCRIPTION_KEY'
url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/analyze"

# Access token for Dropbox API
access_token = 'YOUR_ACCESS_TOKEN'

# Raspberry Pi board
GPIO.setmode(GPIO.BCM)

# Pin config for button
btn = 16
GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Pin config for LCD
lcd_rs = 4
lcd_en = 17
lcd_d4 = 25
lcd_d5 = 24
lcd_d6 = 23
lcd_d7 = 18

# LCD column and row size 
lcd_columns = 20
lcd_rows    = 4

# Initilaise Dropbox
dbx = dropbox.Dropbox(access_token)
# Initialise the LCD using the pins above by calling the construct method of Adafruit LCD library
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
# Initialise the camera
cam = picamera.PiCamera()

# Drive the LCD and display characters
def display_message(line1 = '', line2 = '', line3 = '', line4 = ''):
    lcd.clear() # Clear the display
    lcd.home() # Bring cursor to row 1 and column 1
    if(line1 != '' and line2 == '' and line3 == '' and line4 == ''):
        lcd.message(line1)
    else:
        lcd.message(line1 + '\n' + line2 + '\n' + line3 + '\n' + line4) # multiline message

# Upload image.jpg from working directory to dropbox
def upload_image():
    local_file = os.path.join(os.path.dirname(__file__), 'image.jpg')
    remote_file = '/image.jpg'
    f = open(local_file, 'rb')
    dbx.files_upload(f.read(), remote_file, mode=dropbox.files.WriteMode.overwrite)

# Get the sharable url from dropbox for previously uploaded image
def get_image_url():
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    data = {
        "path": "/image.jpg"
    }
    r = requests.post('https://api.dropboxapi.com/2/sharing/create_shared_link', headers=headers, data=json.dumps(data))
    image_url = r.json()['url']
    image_url = image_url.replace('www', 'dl') # do this step to convert the URL so it can be downloaded
    return image_url

# Make API call and display best guessed caption and tags on LCD
def predict_contents(image_url):
    headers  = {'Ocp-Apim-Subscription-Key': subscription_key }
    params   = {'visualFeatures': 'Description'}
    data     = {'url': image_url}
    response = requests.post(url, headers=headers, params=params, json=data)
    response.raise_for_status()
    image_desc = response.json()['description']['captions'][0]['text']
    image_tags = response.json()['description']['tags']
    display_message(image_desc)
    time.sleep(5)
    display_message('{}, {},'.format(image_tags[0], image_tags[1]), '{}, {},'.format(image_tags[2], image_tags[3]), '{}, {},'.format(image_tags[4], image_tags[5]), '{}, {}'.format(image_tags[6], image_tags[7]),)
    time.sleep(10)

# Starting function
def main():
    display_message('Press the button to', 'capture and analyze', 'the image')
    while True:
        if GPIO.input(btn) == False:
            display_message('Capturing..')
            cam.capture('image.jpg') # Take a picture and save it to working directory
            display_message('Uploading..')
            upload_image() # Save to dropbox
            display_message('Generating Image', 'link..')
            image_url = get_image_url() # Store the URL link for image in a variable
            display_message('Predicting..')
            predict_contents(image_url) # Pass the URL link and make an API call
            main()
        
try:
    main()
finally:
    display_message('Program Stopped.')
