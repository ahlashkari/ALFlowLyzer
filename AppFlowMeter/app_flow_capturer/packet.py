#!/usr/bin/env python3

from datetime import datetime
from scapy.all import *
from scapy.layers.http import HTTP, HTTPResponse
from scapy.layers.dns import DNS, DNSRR
from .protocols import Protocols

class Packet(object):
    def __init__(self, packet: object):
        self.__network_protocol = None
        self.__application_protocol = 'Others'
        self.__extract_network_layer_protocol(packet)
        self.__is_http_response = True if HTTPResponse in packet else False
        self.__status_code = int(packet[HTTPResponse].Status_Code) if self.__is_http_response else -1
        self.__src_ip = packet[IP].src
        self.__dst_ip = packet[IP].dst
        self.__src_port = packet[self.__network_protocol].sport
        self.__dst_port = packet[self.__network_protocol].dport
        self.__timestamp = packet.time
        self.__dns_ttl_value = packet[DNSRR].ttl if packet.haslayer(DNSRR) else 0
        self.__tcp_flags = packet[self.__network_protocol].flags if self.__network_protocol == TCP else []
        self.__len = len(packet)
        self.__has_rst_flag = False
        self.__seq_number = packet[self.__network_protocol].seq if self.__network_protocol == TCP else -1
        self.__ack_number = packet[self.__network_protocol].ack if self.__network_protocol == TCP else -1
        self.__extract_application_layer_protocol(packet)
        self.__transaction_id = -1
        self.__domain_name = "!!!"
        if DNS in packet:
            self.__transaction_id = packet[DNS].id
            if packet[DNS].qd is not None and not isinstance(packet[DNS].qd, bytes):
                self.__domain_name = packet[DNS].qd.qname.decode('UTF-8')
            elif packet[DNS].an is not None and not isinstance(packet[DNS].qd, bytes):
                self.__domain_name = packet[DNS].an.rrname.decode('UTF-8')
            else:
                self.__domain_name = "no domain name!"

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
        # decide based on other things than main port numbers
        if DNS in packet:
            self.__application_protocol = "DNS"
        else:
            self.__application_protocol = "Others"

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

    def get_network_protocol(self) -> str:
        return "TCP" if self.__network_protocol == TCP else "UDP"

    def get_seq_number(self) -> int:
        return self.__seq_number

    def get_ack_number(self) -> int:
        return self.__ack_number

    def get_ack_flag(self) -> bool:
        return 'A' in self.__tcp_flags

    def get_syn_flag(self) -> bool:
        return 'S' in self.__tcp_flags

    def get_transaction_id(self) -> int:
        return self.__transaction_id

    def get_domain_name(self) -> str:
        return self.__domain_name

    def get_dns_ttl_value(self) -> int:
        return self.__dns_ttl_value
