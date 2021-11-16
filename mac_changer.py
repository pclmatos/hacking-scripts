#!/usr/bin/env python

#Module to call system commands
import subprocess

#Module to use arguments when running the program
import optparse

#Module to use regex
import re

def get_arguments():
    parser = optparse.OptionParser()

    #Adds options to use and a description to help menu
    parser.add_option("-i", "--iface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="mac", help="New value for the MAC address")

    #parse_args() return 2 sets of strings which is (options, arguments)
    (options, args) = parser.parse_args()

    if not options.interface and not options.mac:
        #All arguments missing error handler
        parser.error("[-] Please specify an interface and a MAC address. Use --help for more info")
    elif not options.interface:
        #Missing interface error handler
        parser.error("[-] Please specify an interface. Use --help for more info")
    elif not options.mac:
        parser.error("[-] Please specify a MAC address. Use --help for more info")

    return options    

def get_current_mac(interface):
    ifconfig_res = subprocess.check_output(["ifconfig", interface])
    #searches for a pattern in a string
    check_mac = re.search(r"(\w\w:)+\w\w", str(ifconfig_res))
    if check_mac:
        return check_mac.group(0)
    else:
        print("[-] Cannot read MAC address")
        exit(-1)
        

def change_mac(iface , mac):
    print("[+] Changing MAC address for " + iface + " to " + mac)

    subprocess.call(["ifconfig", iface ,"down"])
    subprocess.call(["ifconfig", iface ,"hw","ether", mac])
    subprocess.call(["ifconfig", iface ,"up"])


options = get_arguments()

current_mac = get_current_mac(options.interface)

if current_mac == options.mac:
    print("[-] Desired MAC address matches current MAC")
else:
    change_mac(options.interface, options.mac)
    current_mac = get_current_mac(options.interface)
    if current_mac == options.mac:
        print("[+] Successfully changed MAC")
    else:
        print("[-] Error changing MAC address")