#!/usr/bin/env python

import scapy.all as scapy
import optparse

from scapy.arch.linux import PACKET_ADD_MEMBERSHIP

def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-t", "--target", dest="iprange", help="Sets the range of addresses to scan")

    (options, arguments) = parser.parse_args()

    if not options.iprange:
        parser.error("[-] Please specify an address range to scan")

    return options

def scan(ip):
    #Creates and ARP packet with a destination ip (pdst), op is set to 1 when ommited meaning that it is and arp request
    arp_request = scapy.ARP(pdst=ip)
    #Creates a broadcast frame
    broadcast_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #Appends the broadcast frame to the arp request
    packet = broadcast_frame/arp_request
    #Sends the packet and receives a list of the captured answers
    answered_list = scapy.srp(packet, timeout=1, verbose=False)[0]
    connected_clients = []
    for element in answered_list:
        client_info = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        connected_clients.append(client_info)

    return connected_clients
        

def print_clients(client_list):
    print("IP\t\t\tMAC ADDRESS\n--------------------------------------------")
    for client in client_list:
        print(client["ip"]+"\t\t"+client["mac"])



options = get_arguments()
clients = scan(options.iprange)
print_clients(clients)