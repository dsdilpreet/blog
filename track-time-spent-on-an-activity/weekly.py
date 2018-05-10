import RPi.GPIO as GPIO
import time
import csv

# Raspberry Pi board
GPIO.setmode(GPIO.BCM)

# Pin config for Button
btn = 21
GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Pin config for LED
led = 20
GPIO.setup(led, GPIO.OUT)

# Pin config for Buzzer
buzzer = 16
GPIO.setup(buzzer, GPIO.OUT)

# Global variables
is_working = False
start_time_UTC = None
last_saved_week = None
last_saved_year = None
start_date_local = None
start_time_local = None

# Create a new CSV file with all the headings. A new CSV file is created for every week.
def createCSV(file_name):
	try:
		with open(file_name, 'w', newline='') as f:
			writer = csv.writer(f)	
			GPIO.output(buzzer, GPIO.LOW) # turn off buzzer to clear last exception if any
			writer.writerow(['Start Date', 'Start Time', 'Finish Date', 'Finish Time', 'Hours Worked (hh:mm)'])
	except Exception as e:
		print(e)
		GPIO.output(buzzer, GPIO.HIGH) # make constant sound with buzzer to indicate exception in program

# Append to an existing CSV file 
def updateCSV(file_name, start_date_local, start_time_local, finish_date_local, finish_time_local, hours_worked):
	try:
		with open(file_name, 'a', newline='') as f:
			writer = csv.writer(f)
			GPIO.output(buzzer, GPIO.LOW) # turn off buzzer to clear last exception if any
			writer.writerow([start_date_local, start_time_local, finish_date_local, finish_time_local, hours_worked])
	except Exception as e:
		print(e)
		GPIO.output(buzzer, GPIO.HIGH) # make constant sound with buzzer to indicate exception in program

# Returns human readable time difference in start and end time
def calculate_work_time(finish_time_UTC):
	work_time = finish_time_UTC - start_time_UTC
	work_time = time.strftime('%H:%M', time.gmtime(work_time))
	return work_time

# Only used when program starts for the first time. Gets the last saved week. Prevents overwritting of an existing timesheet.
def get_last_saved_time():
	global last_saved_week
	global last_saved_year
	try:
		with open('last-saved.csv', newline='') as f:
			reader = csv.reader(f)
			for row in reader:
				last_saved_week = row[0] # update global variables 
				last_saved_year = row[1]
	except Exception as e:
		print(e)

# Saves the last Week and Year for last saved record
def set_last_saved(current_week, current_year):
	with open('last-saved.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerow([current_week, current_year])

# This functions calls other functions to save records when push button is pressed.
def main():
	get_last_saved_time()
	global is_working
	global last_saved_week
	global last_saved_year
	global start_time_UTC
	global start_date_local
	global start_time_local

	while True:
		if GPIO.input(btn) == False: 
			if(is_working): # Executed when push button is pressed the 2nd time. Resets the is_working variable. Saves the record in timesheet file.
				is_working = False
				finish_time_UTC = time.time() # only used to calcuate the worked hours
				finish_date_local = time.strftime('%d %b %Y', time.localtime())
				finish_time_local = time.strftime('%I:%M %P', time.localtime())
				current_week = time.strftime('%U', time.localtime())
				current_year = time.strftime('%Y', time.localtime())
				if (last_saved_week == current_week and last_saved_year == current_year): #Update file if already exists
					file_name = last_saved_week + "-" + current_year + '.csv' 
					updateCSV(file_name, start_date_local, start_time_local, finish_date_local, finish_time_local, calculate_work_time(finish_time_UTC))
				else: # create new CSV file and then update it. New CSV timesheet file for new week.
					last_saved_week = current_week
					file_name = last_saved_week + "-" + current_year + '.csv'
					createCSV(file_name)
					updateCSV(file_name, start_date_local, start_time_local, finish_date_local, finish_time_local, calculate_work_time(finish_time_UTC))
					set_last_saved(current_week, current_year)
				GPIO.output(led, GPIO.LOW) # turn the LED off to indicate not working
				GPIO.output(buzzer, GPIO.HIGH) # beep the buzzer for 2 seconds to indicate that record has been saved.
				time.sleep(2)
				GPIO.output(buzzer, GPIO.LOW)
			else: # Executed when push button is pressed for 1st time. Saves the start time and turn the led on.
				is_working = True
				start_time_UTC = time.time()
				start_date_local = time.strftime('%d %b %Y', time.localtime())
				start_time_local = time.strftime('%I:%M %P', time.localtime())
				GPIO.output(led, GPIO.HIGH)
			time.sleep(0.5)

try:
	GPIO.output(buzzer, GPIO.LOW) # turn off buzzer to clear last exception if any
	main()
except Exception as e:
	print(str(e))
	GPIO.output(led, GPIO.LOW) # turn the led off
	GPIO.output(buzzer, GPIO.HIGH) # make constant sound with buzzer to indicate exception in program
finally:
	GPIO.output(led, GPIO.LOW)
	GPIO.output(buzzer, GPIO.LOW)
	GPIO.cleanup()
    
