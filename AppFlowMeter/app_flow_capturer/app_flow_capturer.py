#!/usr/bin/env python3

from scapy.all import *
from scapy.layers.http import HTTPRequest #TODO: check for HTTPResponse
from multipledispatch import dispatch
from .flow import Flow

class AppFlowCapturer(object):
    def __init__(self):
        self.__flows = []

    @dispatch()
    def capture(self) -> list:
        pass

    @dispatch(str)
    def capture(self, pcap_file: str) -> list:
        packets = rdpcap(pcap_file)
        for packet in packets:
            if packet.haslayer(HTTPRequest) and packet.haslayer(TCP):
                self.__add_packet_to_flow(packet)
        return self.__flows

    def __add_packet_to_flow(self, packet):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
        flow = self.__search_for_flow(src_ip, dst_ip, src_port, dst_port)
        if flow == None:
            self.__create_new_flow(src_ip, dst_ip, src_port, dst_port, packet)
        else:
            flow.add_packet(packet)

#    TODO: Improve it
    def __search_for_flow(self, src_ip: str, dst_ip: str, src_port: str, dst_port: str) -> object:
        for flow in self.__flows:
            if (flow.get_src_ip() == src_ip or flow.get_src_ip() == dst_ip) and \
               (flow.get_dst_ip() == src_ip or flow.get_dst_ip() == dst_ip) and \
               (flow.get_src_port() == src_port or flow.get_src_port() == dst_port) and \
               (flow.get_dst_port() == src_port or flow.get_dst_port() == dst_port):
                   return flow

        return None

    def __create_new_flow(self, src_ip: str, dst_ip: str, src_port: str, dst_port: str, packet) -> None:
        new_flow = Flow(src_ip, dst_ip, src_port, dst_port)
        new_flow.add_packet(packet)
        self.__flows.append(new_flow)

