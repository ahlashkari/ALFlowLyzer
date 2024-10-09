#!/usr/bin/env python3

import dpkt
import socket
import datetime
from .protocols import Protocols
from scapy.all import DNS, DNSQR, DNSRR, Ether


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
        self.__timestamp = float(ts)
        self.__human_readable_timestamp = datetime.datetime.fromtimestamp(float(ts), datetime.UTC)
        self.__tcp_flags = net_layer.flags if self.__network_protocol == 'TCP' else 0
        self.__seq_number = net_layer.seq if self.__network_protocol == 'TCP' else -1
        self.__ack_number = net_layer.ack if self.__network_protocol == 'TCP' else -1
        self.__len = len(packet)
        self.__application_protocol = 'Others'
        self.__extract_application_layer_protocol()
        self.__transaction_id = -1
        self.__dns_ttl_values = []
        self.__dns_rr_types = []
        self.__dns_rr_rclasses = []
        self.__dns_rr_qtypes = []
        self.__dns_rr_qclasses = []
        self.__domain_names = []
        self.__extract_dns_data(net_layer, packet)

    def __len__(self):
        return self.__len

    def __lt__(self, o: object):
        return (self.__timestamp <= o.get_timestamp())

    def contains_non_hex_values(self, byte_string):
        for byte in byte_string:
            if not (0x00 <= byte <= 0x7F and (0x20 <= byte <= 0x7E)):
                return True
        try:
            byte_string.decode('ascii')
            return False
        except UnicodeDecodeError:
            return True

    def __extract_dns_data_using_scapy(self, parsed_packet):
        dns_data = parsed_packet[DNS]
        self.__transaction_id = dns_data.id

        if dns_data.qdcount > 0 and isinstance(dns_data.qd, DNSQR):
            self.__domain_names.append(dns_data.qd.qname.decode())

        self.__dns_ancount = dns_data.ancount
        if dns_data.ancount > 0 and isinstance(dns_data.an, DNSRR):
            for i in range(dns_data.ancount):
                if hasattr(dns_data.an[i], 'rrname'):
                    self.__domain_names.append(dns_data.an[i].rrname.decode())
                if hasattr(dns_data.an[i], 'ttl'):
                    self.__dns_ttl_values.append(dns_data.an[i].ttl)
                if hasattr(dns_data.an[i], 'type'):
                    self.__dns_rr_types.append(dns_data.an[i].type)
                if hasattr(dns_data.an[i], 'rclass'):
                    self.__dns_rr_rclasses.append(dns_data.an[i].rclass)

        self.__dns_nscount = dns_data.nscount

        self.__dns_arcount = dns_data.arcount
        if dns_data.arcount > 0 and isinstance(dns_data.ar, DNSRR):
            for i in range(dns_data.arcount):
                if hasattr(dns_data.ar[i], 'type'):
                    self.__dns_rr_qtypes.append(dns_data.ar[i].type)
                if hasattr(dns_data.ar[i], 'rclass'):
                    self.__dns_rr_qclasses.append(dns_data.ar[i].rclass)


    def __extract_dns_data(self, net_layer, packet):
        if self.__application_protocol != 'DNS':
            return
        try:
            if self.contains_non_hex_values(net_layer.data):
                # print()
                # print(f">> The DNS payload contains non bytes data. It is probably a malformed packet.")
                parsed_packet = Ether(packet)
                if DNS in parsed_packet:
                    # print(">> Some data are extractable using `Scapy` library. We will use them for this packet.")
                    self.__extract_dns_data_using_scapy(parsed_packet)

                else:
                    # print(">> We continue the analysis and use the UDP layer data for analysis.")
                    self.__transaction_id = -2
                    self.__domain_names.append("malformed-packet")
                    self.__dns_ancount = -2
                    self.__dns_nscount = -2
                    self.__dns_arcount = -2

                # print()
                return
            dns_data = dpkt.dns.DNS(net_layer.data)
            self.__transaction_id = dns_data.id
            if len(dns_data.qd) > 0:
                self.__domain_names.append(dns_data.qd[0].name)

            self.__dns_ancount = len(dns_data.an)
            if len(dns_data.an) > 0:
                for data in dns_data.an:
                    self.__domain_names.append(dns_data.qd[0].name)
                    self.__dns_ttl_values.append(data.ttl)
                    self.__dns_rr_types.append(data.type)
                    self.__dns_rr_rclasses.append(data.cls)

            self.__dns_nscount = len(dns_data.ns)
            self.__dns_arcount = len(dns_data.ar)
            if len(dns_data.ar) > 0:
                for data in dns_data.ar:
                    self.__dns_rr_qtypes.append(data.type)
                    self.__dns_rr_qclasses.append(data.cls)

        except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError, Exception) as e:
            print()
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

    def get_domain_names(self) -> str:
        return self.__domain_names

    def get_dns_ttl_values(self) -> int:
        return self.__dns_ttl_values
    
    def get_dns_rr_types(self) -> str:
        return self.__dns_rr_types
    
    def get_dns_auth_rr(self) -> int:
        return self.__dns_nscount
    
    def get_dns_add_rr(self) -> int:
        return self.__dns_arcount
    
    def get_dns_ans_rr(self) -> int:
        return self.__dns_ancount
    
    def get_dns_qtypes(self) -> int:
        return self.__dns_rr_qtypes
    
    def get_dns_qclasses(self) -> int:
        return self.__dns_rr_qclasses
    
    def get_dns_rclasses(self) -> int:
        return self.__dns_rr_rclasses
