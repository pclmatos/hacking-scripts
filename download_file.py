#!/usr/bin/env python

import requests, optparse, subprocess, os

def get_arguments():

    parser = optparse.OptionParser()

    parser.add_option("-u", "--url", dest="url", help="URL of the file to download")
    parser.add_option("-p", "--path", dest="path",help="The PATH of the downloaded file")

    options,arguments = parser.parse_args()

    if not options.url and not options.path:
        parser.error("[-] Please provide an url and a PATH. Use -h for more information")
    elif not options.path:
        parser.error("[-] Please provide a PATH to store the file. Use -h for more information")
    elif not options.url:
        parser.error("[-] Please provide an url. Use -h for more information") 

    return options

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    #wb mode for writing a binary file
    with open(file_name, "wb") as file:
        print("[+] Writing to disk")
        file.write(get_response.content)
       
    return file_name


def check_download(file_name):
    list_output = subprocess.check_output(["ls"])
    if file_name in list_output:
        print("[+] Download completed")

options = get_arguments()
os.chdir(options.path)
print("[+] Downloading file from " + options.url + " into " + options.path)
file_name = download(options.url)
check_download(file_name)