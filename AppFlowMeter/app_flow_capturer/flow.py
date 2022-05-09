#!/usr/bin/env python3

from datetime import datetime

class Flow(object):
    def __init__(self, src_ip: str, dst_ip: str, src_port: str, dst_port: str, timestamp: str,
            protocol: str):
        self.__src_ip = src_ip
        self.__dst_ip = dst_ip
        self.__src_port = src_port
        self.__dst_port = dst_port
        self.__timestamp = timestamp
        self.__protocol = protocol
        self.__packets = []
        self.__number_of_fin_flags = 0
        self.__has_rst_flag = False
        self.__last_packet_timestamp = timestamp

    def __str__(self):
        return str(datetime.fromtimestamp(self.__timestamp)) + '--' + self.__src_ip + '--' + \
                str(self.__src_port) + '--' + self.__dst_ip + '--' + str(self.__dst_port)

    def add_packet(self, packet) -> None:
        self.__packets.append(packet)
        self.__last_packet_timestamp = packet.get_timestamp()
        # TODO: check for forward and backward FIN
        if 'F' in packet.get_tcp_flags():
            self.__number_of_fin_flags += 1
        if 'R' in packet.get_tcp_flags():
            self.__has_rst_flag = True

    def get_src_ip(self) -> str:
        return self.__src_ip

    def get_dst_ip(self) -> str:
        return self.__dst_ip

    def get_src_port(self) -> str:
        return self.__src_port

    def get_dst_port(self) -> str:
        return self.__dst_port

    def get_timestamp(self) -> str:
        return self.__timestamp

    def get_protocol(self) -> str:
        return self.__protocol

    def get_packets(self) -> list:
        return self.__packets

    def has_two_fin_flags(self) -> bool:
        if self.__number_of_fin_flags >= 2:
            return True
        return False

    def has_rst_flag(self) -> bool:
        return self.__has_rst_flag

    def get_last_packet_timestamp(self):
        return self.__last_packet_timestamp