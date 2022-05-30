#!/usr/bin/env python3

from datetime import datetime
from scapy.all import *
from scapy.layers.http import HTTP, HTTPResponse, HTTPRequest
from scapy.layers.dns import DNS
from .protocols import Protocols

class Packet(object):
    def __init__(self, packet: object):
        self.__network_protocol = None
        self.__application_protocol = 'Others'
        self.__extract_network_layer_protocol(packet)
        self.__is_http_response = True if HTTPResponse in packet else False
        self.__is_http_request = True if HTTPRequest in packet else False
        self.__status_code = int(packet[HTTPResponse].Status_Code) if self.__is_http_response else -1
        self.__src_ip = packet[IP].src
        self.__dst_ip = packet[IP].dst
        self.__src_port = packet[self.__network_protocol].sport
        self.__dst_port = packet[self.__network_protocol].dport
        self.__timestamp = packet.time
        self.__tcp_flags = packet[self.__network_protocol].flags if self.__network_protocol == TCP else []
        self.__len = len(packet)
        self.__has_rst_flag = False
        self.__extract_application_layer_protocol(packet)

    def __len__(self):
        return self.__len

    def __lt__(self, o: object):
        return (self.__timestamp <= o.get_timestamp())

    def __extract_network_layer_protocol(self, packet: object) -> None:
        if packet.haslayer(TCP):
            self.__network_protocol = TCP

        elif packet.haslayer(UDP):
            self.__network_protocol = UDP

    def __extract_application_layer_protocol(self, packet: object) -> None:
        for protocol_name, protocol_port in Protocols.__members__.items():
            if self.__dst_port == protocol_port.value or self.__src_port == protocol_port.value:
                self.__application_protocol = protocol_name
                return

    def get_tcp_flags(self):
        return self.__tcp_flags

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

    def get_status_code(self) -> int:
        return self.__status_code

    def get_application_protocol(self) -> str:
        return self.__application_protocol

    def get_req_status(self) -> bool:
        return self.__is_http_request

    def get_syn_flag(self) -> int:
        if self.__network_protocol == TCP:
            syn_flag = self.__tcp_flags.S
            return int(syn_flag)
        return 0
