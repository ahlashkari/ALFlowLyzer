#!/usr/bin/env python3

from ..application_flow_capturer import Flow

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

def get_dns_ttl_valus(flow: Flow):
    ttl_values = []
    for packet in flow.get_packets():
        ttl_values.extend([dns_ttl for dns_ttl in packet.get_dns_ttl_values()])
    return ttl_values

def get_dns_rr_types(flow: Flow):
    rr_types = []
    for packet in flow.get_packets():
        rr_types.extend([dns_rr_type for dns_rr_type in packet.get_dns_rr_types()])
    return rr_types