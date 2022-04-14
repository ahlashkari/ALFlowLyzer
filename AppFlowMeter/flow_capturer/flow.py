#!/usr/bin/env python3


class Flow(object):
    def __init__(self, src_ip: str, dst_ip: str, src_port: str, dst_port: str):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.packets = []

    def add_packet(self, packet) -> None:
        self.packets.append(packet)

    def get_src_ip(self):
        return self.src_ip

    def get_dst_ip(self):
        return self.dst_ip

    def get_src_port(self):
        return self.src_port

    def get_dst_port(self):
        return self.dst_port

    def get_packets(self):
        return self.packets
