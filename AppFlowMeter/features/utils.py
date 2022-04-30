#!/usr/bin/env python3

from scapy.all import *


def calculate_duration(packets: list) -> float:
    packets_time = [packet.time for packet in packets]
    return max(packets_time) - min(packets_time)


def extract_receiving_packets(packets: list, dst_ip: str) -> list:
    receiving_packets = []
    for packet in packets:
        if packet[IP].dst == dst_ip:
            receiving_packets.append(packet)
    return receiving_packets


def extract_sending_packets(packets: list, dst_ip: str) -> list:
    sending_packets = []
    for packet in packets:
        if packet[IP].src == dst_ip:
            sending_packets.append(packet)
    return sending_packets

