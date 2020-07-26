import glob
import os
import time, datetime 
import RPi.GPIO as GPIO
import telepot
from telepot.loop import MessageLoop
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import numpy as np
import cv2
from PIL import Image
from imutils.video import VideoStream
import argparse
import imutils
import requests

led1 = 26
led2 = 19
led3 = 13
led4 = 6
heating = 12
watering = 21

led1_sit = 0
led2_sit = 0
led3_sit = 0
led4_sit = 0
heating_temp = 16
deft = 0
heating_msg = 0
heating_mail = 0
got = 0
after = 0
after_val = 0
minute_af = 0
aon = 0
after_on = ''
aoff = 0 
after_off = ''
aoff_am = 0
aon_am = 0
after_off_am = ''
after_on_am = ''
after_temp = 0
temp_on = 0
after_temp_val = 0
old_message = ''

now = datetime.datetime.now()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


device_folder = '/sys/bus/w1/devices/28-031664445cff'
device_file = device_folder + '/w1_slave'

device_folder1 = '/sys/bus/w1/devices/28-041663868bff'
device_file1 = device_folder1 + '/w1_slave'

GPIO.setup(led1, GPIO.OUT)
GPIO.output(led1, 0)
GPIO.setup(led2, GPIO.OUT)
GPIO.output(led2, 0)
GPIO.setup(led3, GPIO.OUT)
GPIO.output(led3, 0)
GPIO.setup(led4, GPIO.OUT)
GPIO.output(led4, 0)
GPIO.setup(heating, GPIO.OUT)
GPIO.output(heating, 0)
GPIO.setup(watering, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def action(msg):
	global led1_sit
	global led2_sit
	global led3_sit
	global led4_sit
	global heating_temp
	global deft
	global heating_msg
	global heating_mail
	global got
	global after
	global after_val
	global minute_af
	global aon
	global after_on
	global aoff
	global after_off
	global aoff_am
	global aon_am
	global after_off_am
	global after_on_am
	global after_temp
	global after_temp_val
	global temp_on
	heating_msg = msg
	chat_id = msg['chat']['id']
	command = msg['text'].lower()
	print('Received: %s' % command)
	if 'on' in command and ('led' in command or 'all' in command) and 'after' not in command:
		message = "Turned on "
		hog = 0
		ner_check = command.split()
		for lus in ner_check:
			if lus[-1] == 's':
				hog = 1			
		if 'led1' in command:
			message = message + "led1 "
			GPIO.output(led1, 1)
			led1_sit = 1
		if 'led2' in command:
			message = message + "led2 "
			GPIO.output(led2, 1)
			led2_sit = 1
		if 'led3' in command:
			message = message + "led3 "
			GPIO.output(led3, 1)
			led3_sit = 1
		if 'led4' in command:
			message = message + "led4 "
			GPIO.output(led4, 1)
			led4_sit = 1
		if 'all' in command or (hog == 1 and 'led' in command):
			message = message + "all "
			GPIO.output(led1, 1)
			GPIO.output(led2, 1)
			GPIO.output(led3, 1)
			GPIO.output(led4, 1)
			led1_sit = 1
			led2_sit = 1
			led3_sit = 1
			led4_sit = 1
		message = message + "light(s)"
		telegram_bot.sendMessage (chat_id, message)

	elif 'on' in command and ('led' in command or 'all' in command) and 'after' in command:
		x = datetime.datetime.now()
		after = 1
		aon = 1
		com_spil = command.split()
		for word in com_spil:
			if word.isdigit():
				after_val = word
		minute_af = x.strftime("%M")
		if 'led1' in command:
			after_on = 'led1'
		if 'led2' in command:
			after_on = 'led2'
		if 'led3' in command:
			after_on = 'led3'
		if 'led4' in command:
			after_on = 'led4'
		if 'all' in command :
			after_on = 'all'

	elif ('միաց' in command or 'մյաց' in command) and 'հետո' not in command:
		message = "Միացվեց "
		hog = 0
		ner_check = command.split()
		for lus in ner_check:
			if lus[-1] == 'ը' and lus[-2] == 'ր' and lus[-3] == 'ե':
				hog = 1		
		if 'լույս1' in command or ('լույս' in command and 'առաջ' in command):
			message = message + "լույս1-ը "
			GPIO.output(led1, 1)
			led1_sit = 1
		if 'լույս2' in command or ('լույս' in command and 'երկր' in command):
			message = message + "լույս2-ը "
			GPIO.output(led2, 1)
			led2_sit = 1
		if 'լույս3' in command or ('լույս' in command and 'երրո' in command):
			message = message + "լույս3-ը "
			GPIO.output(led3, 1)
			led3_sit = 1
		if 'led4' in command or ('լույս' in command and 'չորո' in command):
			message = message + "led4 "
			GPIO.output(led4, 1)
			led4_sit = 1
		if 'բոլոր' in command or 'սաղ' in command or (hog == 1 and 'լույս' in command):
			message = "Միացվեցին "
			message = message + "բոլոր լույսերը"
			GPIO.output(led1, 1)
			GPIO.output(led2, 1)
			GPIO.output(led3, 1)
			GPIO.output(led4, 1)
			led1_sit = 1
			led2_sit = 1
			led3_sit = 1
			led4_sit = 1
		telegram_bot.sendMessage (chat_id, message)
	
	elif ('միաց' in command or 'մյաց' in command) and 'հետո' in command:
		x = datetime.datetime.now()
		after = 1
		aon_am = 1
		com_spil = command.split()
		for word in com_spil:
			if word.isdigit():
				after_val = word
		minute_af = x.strftime("%M")
		if 'լույս1' in command or ('լույս' in command and 'առաջ' in command):
			after_on_am = 'n1'
		if 'լույս2' in command or ('լույս' in command and 'երկր' in command):
			after_on_am = 'n2'
		if 'լույս3' in command or ('լույս' in command and 'երրո' in command):
			after_on_am = 'n3'
		if 'led4' in command or ('լույս' in command and 'չորո' in command):
			after_on_am = 'n4'
		if 'բոլոր' in command or 'սաղ' in command:
			after_on_am = 'all'
	
	if 'off' in command and ('led' in command or 'all' in command) and 'after' not in command:
		message = "Turned off "
		hog = 0
		ner_check = command.split()
		for lus in ner_check:
			if lus[-1] == 's':
				hog = 1			
		if 'led1' in command:
			message = message + "led1 "
			GPIO.output(led1, 0)
			led1_sit = 0
		if 'led2' in command:
			message = message + "led2 "
			GPIO.output(led2, 0)
			led2_sit = 0
		if 'led3' in command:
			message = message + "led3 "
			GPIO.output(led3, 0)
			led3_sit = 0
		if 'led4' in command:
			message = message + "led4 "
			GPIO.output(led4, 0)
			led4_sit = 0
		if 'all' in command or (hog == 1 and 'led' in command):
			message = message + "all "
			GPIO.output(led1, 0)
			GPIO.output(led2, 0)
			GPIO.output(led3, 0)
			GPIO.output(led4, 0)
			led1_sit = 0
			led2_sit = 0
			led3_sit = 0
			led4_sit = 0
		message = message + "light(s)"
		telegram_bot.sendMessage (chat_id, message)
		
	elif 'off' in command and ('led' in command or 'all' in command) and 'after' in command:
		x = datetime.datetime.now()
		after = 1
		aoff = 1
		com_spil = command.split()
		for word in com_spil:
			if word.isdigit():
				after_val = word
		minute_af = x.strftime("%M")
		if 'led1' in command:
			after_off = 'led1'
		if 'led2' in command:
			after_off = 'led2'
		if 'led3' in command:
			after_off = 'led3'
		if 'led4' in command:
			after_off = 'led4'
		if 'all' in command :
			after_off = 'all'		

	elif 'անջ' in command and 'հետո' not in command:
		message = "Անջատվեց "
		hog = 0
		ner_check = command.split()
		for lus in ner_check:
			if lus[-1] == 'ը' and lus[-2] == 'ր' and lus[-3] == 'ե':
				hog = 1
		if 'լույս1' in command or ('լույս' in command and 'առաջ' in command):
			message = message + "լույս1-ը "
			GPIO.output(led1, 0)
			led1_sit = 0
		if 'լույս2' in command or ('լույս' in command and 'երկր' in command):
			message = message + "լույս2-ը "
			GPIO.output(led2, 0)
			led2_sit = 0
		if 'լույս3' in command or ('լույս' in command and 'երրո' in command):
			message = message + "լույս3-ը "
			GPIO.output(led3, 0)
			led3_sit = 0
		if 'led4' in command or ('լույս' in command and 'չորո' in command):
			message = message + "led4 "
			GPIO.output(led4, 0)
			led4_sit = 0
		if 'բոլոր' in command or 'սաղ' in command or (hog == 1 and 'լույս' in command):
			message = "Անջատվեցին "
			message = message + "բոլոր լույսերը"
			GPIO.output(led1, 0)
			GPIO.output(led2, 0)
			GPIO.output(led3, 0)
			GPIO.output(led4, 0)
			led1_sit = 0
			led2_sit = 0
			led3_sit = 0
			led4_sit = 0
		telegram_bot.sendMessage (chat_id, message)

	elif 'անջ' in command and 'հետո' in command:
		x = datetime.datetime.now()
		after = 1
		aoff_am = 1
		com_spil = command.split()
		for word in com_spil:
			if word.isdigit():
				after_val = word
		minute_af = x.strftime("%M")
		if 'լույս1' in command or ('լույս' in command and 'առաջ' in command):
			after_off_am = 'n1'
		if 'լույս2' in command or ('լույս' in command and 'երկր' in command):
			after_off_am = 'n2'
		if 'լույս3' in command or ('լույս' in command and 'երրո' in command):
			after_off_am = 'n3'
		if 'led4' in command or ('լույս' in command and 'չորո' in command):
			after_off_am = 'n4'
		if 'բոլոր' in command or 'սաղ' in command:
			after_off_am = 'all'

	if 'temperature1' in command or 't1' in command:
		message = "Temperature is "
		def read_temp_raw():
			f = open(device_file, 'r')
			lines = f.readlines()
			f.close()
			return lines

		def read_temp():
			lines = read_temp_raw()
			while lines[0].strip()[-3:] != 'YES':
				time.sleep(0.2)
				lines = read_temp_raw()
			equals_pos = lines[1].find('t=')

			if equals_pos != -1:
				temp_string = lines[1][equals_pos+2:]
				temp_c = float(temp_string) / 1000.0
				return temp_c
		te = read_temp()
		message = message + str(te) + ' °C'
		telegram_bot.sendMessage (chat_id, message)

	elif 'ջերմ1' in command or 'ջ1' in command:
		message = "Ջերմաստիճանն է "
		def read_temp_raw():
			f = open(device_file, 'r')
			lines = f.readlines()
			f.close()
			return lines

		def read_temp():
			lines = read_temp_raw()
			while lines[0].strip()[-3:] != 'YES':
				time.sleep(0.2)
				lines = read_temp_raw()
			equals_pos = lines[1].find('t=')

			if equals_pos != -1:
				temp_string = lines[1][equals_pos+2:]
				temp_c = float(temp_string) / 1000.0
				return temp_c
		te = read_temp()
		message = message + str(te) + ' °C'
		telegram_bot.sendMessage (chat_id, message)	
	
	if 'temperature2' in command or 't2' in command:
		message = "Temperature is "
		def read_temp_raw():
			f = open(device_file1, 'r')
			lines = f.readlines()
			f.close()
			return lines

		def read_temp():
			lines = read_temp_raw()
			while lines[0].strip()[-3:] != 'YES':
				time.sleep(0.2)
				lines = read_temp_raw()
			equals_pos = lines[1].find('t=')

			if equals_pos != -1:
				temp_string = lines[1][equals_pos+2:]
				temp_c = float(temp_string) / 1000.0
				return temp_c
		te = read_temp()
		message = message + str(te) + ' °C'
		telegram_bot.sendMessage (chat_id, message)

	elif 'ջերմ2' in command or 'ջ2' in command:
		message = "Ջերմաստիճանն է "
		def read_temp_raw():
			f = open(device_file1, 'r')
			lines = f.readlines()
			f.close()
			return lines

		def read_temp():
			lines = read_temp_raw()
			while lines[0].strip()[-3:] != 'YES':
				time.sleep(0.2)
				lines = read_temp_raw()
			equals_pos = lines[1].find('t=')

			if equals_pos != -1:
				temp_string = lines[1][equals_pos+2:]
				temp_c = float(temp_string) / 1000.0
				return temp_c
		te = read_temp()
		message = message + str(te) + ' °C'
		telegram_bot.sendMessage (chat_id, message)
	if 'email' in command:
		def read_temp_raw():
			f = open(device_file, 'r')
			lines = f.readlines()
			f.close()
			return lines

		def read_temp():
			lines = read_temp_raw()
			while lines[0].strip()[-3:] != 'YES':
				time.sleep(0.2)
				lines = read_temp_raw()
			equals_pos = lines[1].find('t=')
			if equals_pos != -1:
				temp_string = lines[1][equals_pos+2:]
				temp_c = float(temp_string) / 1000.0
				return temp_c

		def read_temp_raw1():
			f = open(device_file1, 'r')
			lines = f.readlines()
			f.close()
			return lines

		def read_temp1():
			lines = read_temp_raw1()
			while lines[0].strip()[-3:] != 'YES':
				time.sleep(0.2)
				lines = read_temp_raw()
			equals_pos = lines[1].find('t=')

			if equals_pos != -1:
				temp_string = lines[1][equals_pos+2:]
				temp_c = float(temp_string) / 1000.0
				return temp_c
		te = str(read_temp())
		te2 = str(read_temp1())
		email = 'sahaksbot@gmail.com'
		password = 'newdvbt2'
		subject = 'Situation'
		send_email = command.split()
		if led1_sit == 0:
			led1_sit_str = 'Disconnected'
		else:
			led1_sit_str = 'Connected'
			
		if led2_sit == 0:
			led2_sit_str = 'Disconnected'
		else:
			led2_sit_str = 'Connected'
		if led3_sit == 0:
			led3_sit_str = 'Disconnected'
		else:
			led3_sit_str = 'Connected'
		if led4_sit == 0:
			led4_sit_str = 'Disconnected'
		else:
			led4_sit_str = 'Connected'
		if heating_mail == 0:
			heating_mail_str = 'Disconnected'
		else:
			heating_mail_str = 'Connected'
		for nar in send_email:
			if '@' in nar:
				send_to_email = nar 
		message = 'Led1: ' + str(led1_sit_str) + "\n" + 'Led2: ' + str(led2_sit_str) + "\n" + 'Led3: ' + str(led3_sit_str) + "\n" + 'Led4: ' + str(led4_sit_str) + "\n" + 'T1: ' + te + ' °C' + "\n" + 'T2: ' + te2 + ' °C' + "\n" + 'Heating ' + heating_mail_str + "\n" + 'Heating Temperature: ' + str(heating_temp) + ' °C' 
		msg = MIMEMultipart()
		msg['From'] = email
		msg['To'] = send_to_email
		msg['Subject'] = subject
		msg.attach(MIMEText(message, 'plain'))
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(email, password)
		text = msg.as_string()
		server.sendmail(email, send_to_email, text)
		server.quit()
		message = 'The mail was sent to ' + send_to_email
		telegram_bot.sendMessage (chat_id, message)

	elif 'իմեյլ' in command or 'մեյլ' in command or 'նամակ' in command:
		def read_temp_raw():
			f = open(device_file, 'r')
			lines = f.readlines()
			f.close()
			return lines

		def read_temp():
			lines = read_temp_raw()
			while lines[0].strip()[-3:] != 'YES':
				time.sleep(0.2)
				lines = read_temp_raw()
			equals_pos = lines[1].find('t=')
			if equals_pos != -1:
				temp_string = lines[1][equals_pos+2:]
				temp_c = float(temp_string) / 1000.0
				return temp_c

		def read_temp_raw1():
			f = open(device_file1, 'r')
			lines = f.readlines()
			f.close()
			return lines

		def read_temp1():
			lines = read_temp_raw1()
			while lines[0].strip()[-3:] != 'YES':
				time.sleep(0.2)
				lines = read_temp_raw()
			equals_pos = lines[1].find('t=')

			if equals_pos != -1:
				temp_string = lines[1][equals_pos+2:]
				temp_c = float(temp_string) / 1000.0
				return temp_c
		te = str(read_temp())
		te2 = str(read_temp1())
		email = 'sahaksbot@gmail.com'
		password = 'newdvbt2'
		subject = 'Իրավիճակ'
		send_email = command.split()
		if led1_sit == 0:
			led1_sit_str = 'Անջատված'
		else:
			led1_sit_str = 'Միացած'
			
		if led2_sit == 0:
			led2_sit_str = 'Անջատված'
		else:
			led2_sit_str = 'Միացած'
		if led3_sit == 0:
			led3_sit_str = 'Անջատված'
		else:
			led3_sit_str = 'Միացած'
		if led4_sit == 0:
			led4_sit_str = 'Անջատված'
		else:
			led4_sit_str = 'Միացած'		
		if heating_mail == 0:
			heating_mail_str = 'Անջատված'
		else:
			heating_mail_str = 'Միացած'
		for nar in send_email:
			if '@' in nar:
				send_to_email = nar 
		message = 'Լույս1: ' + str(led1_sit_str) +  "\n" + 'Լույս2: ' + str(led2_sit_str) + "\n" + 'Լույս3: ' + str(led3_sit_str) + "\n" + 'Լույս4: ' + str(led4_sit_str) + "\n" + 'Ջ1: ' + te + ' °C' + "\n"  + 'Ջ2: ' + te2 + ' °C' + "\n" + 'Ջեռուցում ' + heating_mail_str + "\n" + 'Ջեռուցման Ջերմաստիճան ' + str(heating_temp) + ' °C'
		msg = MIMEMultipart()
		msg['From'] = email
		msg['To'] = send_to_email
		msg['Subject'] = subject
		msg.attach(MIMEText(message, 'plain'))
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(email, password)
		text = msg.as_string()
		server.sendmail(email, send_to_email, text)
		server.quit()
		message = 'Նամակը ուղղարկվեց ' + send_to_email + ' ' + 'փոստին' 
		telegram_bot.sendMessage (chat_id, message)
	
	if (('set' in command and 'temperature' in command) or ('change' in command and 'temperature' in command)) and 'after' not in command:
		new_comm = command.split()
		for nor in new_comm:
			if nor.isdigit():
				heating_temp = int(nor)
		deft = heating_temp
		message = 'Heating temperature changed to ' + str(heating_temp) + ' °C'  
		telegram_bot.sendMessage (chat_id, message)
	elif (('set' in command and 'temperature' in command) or ('change' in command and 'temperature' in command)) and 'after' in command:
		temp_on = 1
		com_spil = command.split()
		after_val = com_spil[-1]
		after_temp_val = com_spil[-3]
		message = 'Hetaing temperature will changed after ' + after_val + ' minutes to ' + after_temp_val + ' °C' 
		telegram_bot.sendMessage (chat_id, message)
		after = 1
		x = datetime.datetime.now()
		minute_af = x.strftime("%M")
		heating_temp = after_temp_val
	elif ('դարձ' in command and 'ջերմ' in command) or ('փոխ' in command and 'ջերմ' in command):
		new_comm = command.split()
		for nor in new_comm:
			if nor.isdigit():
				heating_temp = int(nor)
		deft = heating_temp
		message = 'Տաքացման ջերմաստիճանը փոխվեց ' + str(heating_temp) + ' °C'
		telegram_bot.sendMessage (chat_id, message)
	if 'temperature' in command and 'heating' in command and 'set' not in command and 'change' not in command:
		message = 'Heating temperature is ' + str(heating_temp) + ' °C'
		telegram_bot.sendMessage (chat_id, message)
	elif 'ջերմաստ' in command and 'ջեռուց' in command and 'դարձ' not in command and 'փոխ' not in command:
		message = 'Տաքացման ջերմաստիճանն է՝ ' + str(heating_temp) + ' °C'
		telegram_bot.sendMessage (chat_id, message)
	
	if 'situat' in command or 'informat' in command:
		def read_temp_raw():
			f = open(device_file, 'r')
			lines = f.readlines()
			f.close()
			return lines

		def read_temp():
			lines = read_temp_raw()
			while lines[0].strip()[-3:] != 'YES':
				time.sleep(0.2)
				lines = read_temp_raw()
			equals_pos = lines[1].find('t=')
			if equals_pos != -1:
				temp_string = lines[1][equals_pos+2:]
				temp_c = float(temp_string) / 1000.0
				return temp_c

		def read_temp_raw1():
			f = open(device_file1, 'r')
			lines = f.readlines()
			f.close()
			return lines

		def read_temp1():
			lines = read_temp_raw1()
			while lines[0].strip()[-3:] != 'YES':
				time.sleep(0.2)
				lines = read_temp_raw()
			equals_pos = lines[1].find('t=')

			if equals_pos != -1:
				temp_string = lines[1][equals_pos+2:]
				temp_c = float(temp_string) / 1000.0
				return temp_c
		te = str(read_temp())
		te2 = str(read_temp1())		
		if led1_sit == 0:
			led1_sit_str = 'Disconnected'
		else:
			led1_sit_str = 'Connected'
		if led2_sit == 0:
			led2_sit_str = 'Disconnected'
		else:
			led2_sit_str = 'Connected'
		if led3_sit == 0:
			led3_sit_str = 'Disconnected'
		else:
			led3_sit_str = 'Connected'
		if led4_sit == 0:
			led4_sit_str = 'Disconnected'
		else:
			led4_sit_str = 'Connected'
		if heating_mail == 0:
			heating_mail_str = 'Disconnected'
		else:
			heating_mail_str = 'Connected'
		
		message = 'Led1: ' + str(led1_sit_str) + "\n" + 'Led2: ' + str(led2_sit_str) + "\n" + 'Led3: ' + str(led3_sit_str) + "\n" + 'Led4: ' + str(led4_sit_str) + "\n" + 'T1: ' + te + ' °C' + "\n" + 'T2: ' + te2 + ' °C' + "\n" + 'Heating ' + heating_mail_str + "\n" + 'Heating Temperature: ' + str(heating_temp) + ' °C' + '😉😉'
		telegram_bot.sendMessage (chat_id, message)
	
	elif 'իրավիճ' in command or 'ինֆորմ' in command:
		def read_temp_raw():
			f = open(device_file, 'r')
			lines = f.readlines()
			f.close()
			return lines

		def read_temp():
			lines = read_temp_raw()
			while lines[0].strip()[-3:] != 'YES':
				time.sleep(0.2)
				lines = read_temp_raw()
			equals_pos = lines[1].find('t=')
			if equals_pos != -1:
				temp_string = lines[1][equals_pos+2:]
				temp_c = float(temp_string) / 1000.0
				return temp_c

		def read_temp_raw1():
			f = open(device_file1, 'r')
			lines = f.readlines()
			f.close()
			return lines

		def read_temp1():
			lines = read_temp_raw1()
			while lines[0].strip()[-3:] != 'YES':
				time.sleep(0.2)
				lines = read_temp_raw()
			equals_pos = lines[1].find('t=')

			if equals_pos != -1:
				temp_string = lines[1][equals_pos+2:]
				temp_c = float(temp_string) / 1000.0
				return temp_c
		te = str(read_temp())
		te2 = str(read_temp1())		
		if led1_sit == 0:
			led1_sit_str = 'Անջատված'
		else:
			led1_sit_str = 'Միացած'
			
		if led2_sit == 0:
			led2_sit_str = 'Անջատված'
		else:
			led2_sit_str = 'Միացած'
		if led3_sit == 0:
			led3_sit_str = 'Անջատված'
		else:
			led3_sit_str = 'Միացած'
		if led4_sit == 0:
			led4_sit_str = 'Անջատված'
		else:
			led4_sit_str = 'Միացած'		
		if heating_mail == 0:
			heating_mail_str = 'Անջատված'
		else:
			heating_mail_str = 'Միացած'
		message = 'Լույս1: ' + str(led1_sit_str) +  "\n" + 'Լույս2: ' + str(led2_sit_str) + "\n" + 'Լույս3: ' + str(led3_sit_str) + "\n" + 'Լույս4: ' + str(led4_sit_str) + "\n" + 'Ջ1: ' + te + ' °C' + "\n"  + 'Ջ2: ' + te2 + ' °C' + "\n" + 'Ջեռուցում ' + heating_mail_str + "\n" + 'Ջեռուցման Ջերմաստիճան ' + str(heating_temp) + ' °C' + '😉😉' 
		telegram_bot.sendMessage (chat_id, message)
	if 'time' in command:
		x = datetime.datetime.now()
		hour = int(x.strftime("%H"))
		minute = str(x.strftime("%M"))
		seconde = str(x.strftime("%S"))
		am_pm = str(x.strftime("%p"))
		timezone = str(x.strftime("%Z"))
		message = str(hour + 4) + ':' + minute + ':' + seconde + ' ' + am_pm + '  ' + timezone
		telegram_bot.sendMessage (chat_id, message)

	if 'weather' in command:
		api_address='http://api.openweathermap.org/data/2.5/weather?appid=aab1f1cefc805b071ad76647225515c7&q='
		city_split = command.split(' ')
		city = city_split[-1]
		url = api_address + city
		json_data = requests.get(url).json()
		weather_description = 'Description: ' +  json_data['weather'][0]['description']
		weather_temp = 'Temperature: ' + str(int(int(json_data['main']['temp']) - 273.15)) + ' °C' 
		weather_country = 'Country: ' +  json_data['sys']['country']
		weather_wind = 'Wind Speed: ' + str(json_data['wind']['speed'])
		weather_visibility = 'Visibility: ' + str(json_data['visibility'])
		weather_humidity = 'Humidity: ' + str(json_data['main']['humidity'])
		weather_station = weather_description + "\n"  + str(weather_temp) + "\n"  + weather_country + "\n"  + weather_wind +  "\n" +  weather_visibility + "\n" +  weather_humidity
		print('Wet')
		telegram_bot.sendMessage (chat_id, weather_station)
	
	if 'secur' in command and 'on' in command:
		if got == 0:
			def motion():
				global got
				out = 0
				ap = argparse.ArgumentParser()
				ap.add_argument("-v", "--video", help="path to the video file")
				ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
				args = vars(ap.parse_args())
				if args.get("video", None) is None:
					vs = VideoStream(src=0).start()
					time.sleep(2.0)
				else:
					vs = cv2.VideoCapture(args["video"])
				firstFrame = None
				while got == 0:
					frame = vs.read()
					frame = frame if args.get("video", None) is None else frame[1]
					text = "Unoccupied"
					if frame is None:
						break
					frame = imutils.resize(frame, width=500)
					gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
					gray = cv2.GaussianBlur(gray, (21, 21), 0)
					if firstFrame is None:
						firstFrame = gray
						continue
					frameDelta = cv2.absdiff(firstFrame, gray)
					thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
					thresh = cv2.dilate(thresh, None, iterations=2)
					cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
						cv2.CHAIN_APPROX_SIMPLE)
					cnts = imutils.grab_contours(cnts)
					for c in cnts:
						if cv2.contourArea(c) < args["min_area"]:
							continue
						(x, y, w, h) = cv2.boundingRect(c)
						cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
						text = "Occupied"
						if got == 0:
							got = 1
						message = 'Detected motion!!'
						telegram_bot.sendMessage (chat_id, message)
						out = 1
						got = 1
					cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
					cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
						(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

					key = cv2.waitKey(1) & 0xFF

					if key == ord("q"):
						break
				vs.stop() if args.get("video", None) is None else vs.release()
				cv2.destroyAllWindows()

	
			def cut():
				face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_defult.xml")

				#img = cv2.imread("im.jpg")
				cap = cv2.VideoCapture(0)
				ret, img = cap.read()
				gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				n = 0
				faces = face_cascade.detectMultiScale(gray, 1.3, 5)
				cv2.imwrite("face/ress" + ".jpg", img)
				mydir = 'face'
				filelist = [ f for f in os.listdir(mydir) if f.endswith(".jpg") ]

				for f in filelist:
					os.remove(os.path.join(mydir, f))

				for (x, y, w, h) in faces:
						cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
						imgCrop = img[y:y+h,x:x+w]
						n += 1
						width = imgCrop.size
						height = imgCrop.size
						res = cv2.resize(imgCrop, dsize=(280, 280), interpolation=cv2.INTER_CUBIC)
						cv2.imwrite("face/res" + str(n) + ".jpg", res)
				cv2.imwrite('face/img.jpg', img)
			if got == 0:
				jp = 1
				motion()
				cut()
				got = 1
				foto = open('face/img.jpg')
				mydir1 = 'face'
				filelist1 = [ f1 for f1 in os.listdir(mydir1) if f1.endswith(".jpg") ]
				if len(filelist1) > 1:
					for f1 in range(len(filelist1) - 1):
						telegram_bot.sendPhoto(chat_id, photo=open('face/res' + str(jp) + '.jpg', 'rb'))
						jp += 1
				telegram_bot.sendPhoto(chat_id, photo=open('face/img.jpg', 'rb'))
				
		got = 0

def check_for_after():
	global after
	global after_val
	global minute_af
	global aon
	global after_on
	global aoff
	global after_off
	global aoff_am
	global aon_am
	global after_off_am
	global after_on_am
	global temp_on
	global after_temp
	global after_temp_val
	global heating_mail
	global deft
	x = datetime.datetime.now()
	if after == 1:
		if int(x.strftime("%M")) - int(after_val) == int(minute_af):
			if aon == 1:
				if after_on == 'led1':
					telegram_bot.sendMessage (718887974, 'Turned on led1 light(s)')
					GPIO.output(led1, 1)
					after = 0
					aon = 0
				if after_on == 'led2':
					telegram_bot.sendMessage (718887974, 'Turned on led2 light(s)')
					GPIO.output(led2, 1)
					after = 0
					aon = 0
				if after_on == 'led3':
					telegram_bot.sendMessage (718887974, 'Turned on led3 light(s)')
					GPIO.output(led3, 1)
					after = 0
					aon = 0
				if after_on == 'led4':
					telegram_bot.sendMessage (718887974, 'Turned on led4 light(s)')
					GPIO.output(led4, 1)
					after = 0
					aon = 0
				if after_on == 'all':
					telegram_bot.sendMessage (718887974, 'Turned on all light(s)')
					GPIO.output(led1, 1)
					GPIO.output(led2, 1)
					GPIO.output(led3, 1)
					GPIO.output(led4, 1)
					after = 0
					aon = 0
			if aoff == 1:
				if after_off == 'led1':
					telegram_bot.sendMessage (718887974, 'Turned off led1 light(s)')
					GPIO.output(led1, 0)
					after = 0
					aoff = 0
				if after_off == 'led2':
					telegram_bot.sendMessage (718887974, 'Turned off led2 light(s)')
					GPIO.output(led2, 0)
					after = 0
					aoff = 0
				if after_off == 'led3':
					telegram_bot.sendMessage (718887974, 'Turned off led3 light(s)')
					GPIO.output(led3, 0)
					after = 0
					aoff = 0
				if after_off == 'led4':
					telegram_bot.sendMessage (718887974, 'Turned off led4 light(s)')
					GPIO.output(led4, 0)
					after = 0
					aoff = 0
				if after_off == 'all':
					telegram_bot.sendMessage (718887974, 'Turned off all light(s)')
					GPIO.output(led1, 0)
					GPIO.output(led2, 0)
					GPIO.output(led3, 0)
					GPIO.output(led4, 0)
					after = 0
					aoff = 0
			if aon_am == 1:
				if after_on_am == 'n1':
					telegram_bot.sendMessage (718887974, 'Միացվեց լույս1-ը')
					GPIO.output(led1, 1)
					after = 0
					aon_am = 0
				if after_on_am == 'n2':
					telegram_bot.sendMessage (718887974, 'Միացվեց լույս2-ը')
					GPIO.output(led2, 1)
					after = 0
					aon_am = 0
				if after_on_am == 'n3':
					telegram_bot.sendMessage (718887974, 'Միացվեց լույս3-ը')
					GPIO.output(led3, 1)
					after = 0
					after = 0
					aon_am = 0
				if after_on_am == 'n4':
					telegram_bot.sendMessage (718887974, 'Միացվեց լույս4-ը')
					GPIO.output(led4, 1)
					after = 0
					aon_am = 0
				if after_on_am == 'all':
					telegram_bot.sendMessage (718887974, 'Միացվեցին բոլոր լույսերը')
					GPIO.output(led1, 1)
					GPIO.output(led2, 1)
					GPIO.output(led3, 1)
					GPIO.output(led4, 1)
					after = 0
					aon_am = 0	
			if aoff_am == 1:
				if after_off_am == 'n1':
					telegram_bot.sendMessage (718887974, 'Անջատվեց լույս1-ը')
					GPIO.output(led1, 0)
					after = 0
					aoff_am = 0
				if after_off_am == 'n2':
					telegram_bot.sendMessage (718887974, 'Անջատվեց լույս2-ը')
					GPIO.output(led2, 0)
					after = 0
					aoff_am = 0
				if after_off_am == 'n3':
					telegram_bot.sendMessage (718887974, 'Անջատվեց լույս3-ը')
					GPIO.output(led3, 0)
					after = 0
					aoff_am = 0
				if after_on_am == 'n4':
					telegram_bot.sendMessage (718887974, 'Անջատվեց լույս3-ը')
					GPIO.output(led4, 0)
					after = 0
					aoff_am = 0
				if after_off_am == 'all':
					telegram_bot.sendMessage (718887974, 'Անջատվեցին բոլոր լույսերը')
					GPIO.output(led1, 0)
					GPIO.output(led2, 0)
					GPIO.output(led3, 0)
					GPIO.output(led4, 0)
					after = 0
			
				aoff_am = 0	
			if temp_on == 1:
				deft = after_temp_val
				after = 0
				temp_on = 0
def check_fro_heating():
	global heating_mail
	global deft
	global old_message
	def read_temp_raw():
		f = open(device_file, 'r')
		lines = f.readlines()
		f.close()
		return lines

	def read_temp():
		lines = read_temp_raw()
		while lines[0].strip()[-3:] != 'YES':
			time.sleep(0.2)
			lines = read_temp_raw()
		equals_pos = lines[1].find('t=')
		if equals_pos != -1:
			temp_string = lines[1][equals_pos+2:]
			temp_c = float(temp_string) / 1000.0
			return temp_c
	t1_for_heating = read_temp()
	if 	int(deft) > t1_for_heating:
		message = 'Heating turnt on'
		GPIO.output(heating, 1)
		heating_mail = 1
		if old_message != message:
			telegram_bot.sendMessage (718887974, message)
	elif int(deft) < t1_for_heating:
		message = 'Heating turnt off'
		heating_mail = 0
		GPIO.output(heating, 0)
		if old_message != message:
			telegram_bot.sendMessage (718887974, message)	
	old_message = message

telegram_bot = telepot.Bot('731307227:AAE9hLj9G5pjzuEGTNvEH0UJ2ToWQ-u9Sow')
print (telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print('Up and Running....')

while 1:
	check_for_after()
	check_fro_heating()
	time.sleep(10)

