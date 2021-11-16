#!/usr/bin/env python

import scapy.all as scapy


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast_frame/arp_request
    answered_list = scapy.srp(packet, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def sniff(interface):
	scapy.sniff(iface=interface, store=False, prn=proccess_sniffed_packet)

def proccess_sniffed_packet(packet):
	if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
		try:
			real_mac = get_mac(packet[scapy.ARP].psrc)
			response_mac = packet[scapy.ARP].hwsrc

			if real_mac != response_mac:
				print("[+] You're under attack")
		except IndexError:
			pass

try:
	sniff("eth0")
except KeyboardInterrupt:
	print("[+] Stopping ARP Spoofing detection")