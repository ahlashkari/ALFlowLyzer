#!/usr/bin/env python3

def calculate_duration(packets: list) -> float:
    packets_time = [packet.get_timestamp() for packet in packets]
    return max(packets_time) - min(packets_time)


def extract_receiving_packets(packets: list, dst_ip: str) -> list:
    receiving_packets = []
    for packet in packets:
        if packet.get_dst_ip() == dst_ip:
            receiving_packets.append(packet)
    return receiving_packets


def extract_sending_packets(packets: list, dst_ip: str) -> list:
    sending_packets = []
    for packet in packets:
        if packet.get_src_ip() == dst_ip:
            sending_packets.append(packet)
    return sending_packets