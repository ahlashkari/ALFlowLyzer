#!/usr/bin/env python3

from scapy.all import *


def calculate_duration(packets: list):
    packets_time = [packet.time for packet in packets]
    return max(packets_time) - min(packets_time)


def extract_incoming_packets(packets: list, dst_ip: str) -> list:
    incoming_packets = []
    for packet in packets:
        if packet[IP].dst == dst_ip:
            incoming_packets.append(packet)
    return incoming_packets


def extract_outgoing_packets(packets: list, dst_ip: str) -> list:
    outgoing_packets = []
    for packet in packets:
        if packet[IP].src == dst_ip:
            outgoing_packets.append(packet)
    return outgoing_packets

