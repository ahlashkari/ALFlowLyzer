#!/usr/bin/env python3

from scapy.all import *


def calculate_incoming_packets_number(packets: list, dst_ip: str) -> int:
    counter = 0
    for packet in packets:
        if packet[IP].dst == dst_ip:
            counter += 1
    return counter


def calculate_outgoing_packets_number(packets: list, dst_ip: str) -> int:
    counter = 0
    for packet in packets:
        if packet[IP].src == dst_ip:
            counter += 1
    return counter

