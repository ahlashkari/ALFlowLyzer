#!/usr/bin/env python3


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

    def add_packet(self, packet) -> None:
        self.__packets.append(packet)

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
