#!/usr/bin/env python3

import dpkt
from datetime import datetime
# from scapy.all import *
# from scapy.layers.http import HTTP, HTTPResponse
# from scapy.layers.dns import *
from .protocols import Protocols
import socket


class Packet(object):
    def __init__(self, packet: object, ts):
        eth = dpkt.ethernet.Ethernet(packet)
        ip = eth.data
        self.__src_ip = socket.inet_ntoa(ip.src)
        self.__dst_ip = socket.inet_ntoa(ip.dst)
        net_layer = ip.data
        self.__src_port = net_layer.sport
        self.__dst_port = net_layer.dport
        self.__network_protocol = 'TCP'
        if isinstance(ip.data, dpkt.udp.UDP):
            self.__network_protocol = 'UDP'
        self.__timestamp = ts
        self.__human_readable_timestamp = datetime.utcfromtimestamp(ts)
        self.__tcp_flags = net_layer.flags if self.__network_protocol == 'TCP' else 0
        self.__seq_number = net_layer.seq if self.__network_protocol == 'TCP' else -1
        self.__ack_number = net_layer.ack if self.__network_protocol == 'TCP' else -1
        self.__len = len(packet)
        self.__application_protocol = 'Others'
        self.__extract_application_layer_protocol()
        self.__transaction_id = -1
        self.__dns_ttl_value = 0
        self.__dns_rr_type = 0
        self.__dns_rr_rclass = 0
        self.__dns_rr_qtype = 0
        self.__dns_rr_qclass = 0
        self.__domain_name = "no domain name!"
        self.__extract_dns_data(net_layer)
        del eth
        del ip

    def __len__(self):
        return self.__len

    def __lt__(self, o: object):
        return (self.__timestamp <= o.get_timestamp())

    def __extract_dns_data(self, net_layer):
        if self.__application_protocol != 'DNS':
            return
        try:
            dns_data = dpkt.dns.DNS(net_layer.data)
            self.__transaction_id = dns_data.id
            if len(dns_data.qd) > 0:
                self.__domain_name = dns_data.qd[0].name

            self.__dns_ancount = len(dns_data.an)
            if len(dns_data.an) > 0:
                self.__dns_ttl_value = dns_data.an[0].ttl
                self.__dns_rr_type = dns_data.an[0].type
                self.__dns_rr_rclass = dns_data.an[0].cls

            self.__dns_nscount = len(dns_data.ns)
            self.__dns_arcount = len(dns_data.ar)
            if len(dns_data.ar) > 0:
                self.__dns_rr_qtype = dns_data.ar[0].type
                self.__dns_rr_qclass = dns_data.ar[0].cls
            del dns_data

        except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError, Exception) as e:
            print('\nError Parsing DNS, Might be a truncated packet...')
            print('Exception: {!r}'.format(e))
            return

    def __extract_application_layer_protocol(self) -> None:
        for protocol_name, protocol_port in Protocols.__members__.items():
            if self.__dst_port == protocol_port.value or self.__src_port == protocol_port.value:
                self.__application_protocol = protocol_name
                return
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

    def get_human_readable_timestamp(self) -> str:
        return self.__human_readable_timestamp

    def get_application_protocol(self) -> str:
        return self.__application_protocol

    def get_network_protocol(self) -> str:
        return self.__network_protocol

    def get_seq_number(self) -> int:
        return self.__seq_number

    def get_ack_number(self) -> int:
        return self.__ack_number

    def has_fin_flag(self) -> bool:
        return (self.__tcp_flags & dpkt.tcp.TH_FIN)

    def has_rst_flag(self) -> bool:
        return (self.__tcp_flags & dpkt.tcp.TH_RST)

    def has_ack_flag(self) -> bool:
        return (self.__tcp_flags & dpkt.tcp.TH_ACK)

    def has_syn_flag(self) -> bool:
        return (self.__tcp_flags & dpkt.tcp.TH_SYN)

    def get_transaction_id(self) -> int:
        return self.__transaction_id

    def get_domain_name(self) -> str:
        return self.__domain_name

    def get_dns_ttl_value(self) -> int:
        return self.__dns_ttl_value
    
    def get_dns_rr_type(self) -> str:
        return self.__dns_rr_type
    
    def get_dns_auth_rr(self) -> int:
        return self.__dns_nscount
    
    def get_dns_add_rr(self) -> int:
        return self.__dns_arcount
    
    def get_dns_ans_rr(self) -> int:
        return self.__dns_ancount
    
    def get_dns_qtype(self) -> int:
        return self.__dns_rr_qtype
    
    def get_dns_qclass(self) -> int:
        return self.__dns_rr_qclass
    
    def get_dns_rclass(self) -> int:
        return self.__dns_rr_rclass
