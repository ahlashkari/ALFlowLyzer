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


def extract_successful_packets(packets: list, dst_ip: str) -> list:
    successful_packets = []
    for packet in packets:
        if packet.get_status_code() == 200:
            successful_packets.append(packet)
    return successful_packets


def extract_request_response_packets(packets: list) -> list:
    request_response_packets = []
    for packet in packets:
        if packet.get_req_status() or packet.get_response_status():
            request_response_packets.append(packet)
    return request_response_packets


def extract_delta_delay(packets: list) -> list:
    delta_delay = []
    req_pkt_end_time = []
    resp_pkt_time = []
    for (pkt_idx, packet) in enumerate(packets):
        if packet.get_req_status():
            req_pkt_end_time.append(packets[pkt_idx+1].get_timestamp())
        if packet.get_response_status():
            resp_pkt_time.append(packet.get_timestamp())
    
    if len(req_pkt_end_time) == len(resp_pkt_time):
        for i in range(len(req_pkt_end_time)):
            delta_delay.append(float(resp_pkt_time[i] - req_pkt_end_time[i]))
    return delta_delay
