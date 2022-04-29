#!/usr/bin/env python3

from datetime import datetime
from scapy.all import *
from scapy.layers.http import HTTP
from multipledispatch import dispatch
from .flow import Flow

class AppFlowCapturer(object):
    def __init__(self):
        self.__finished_flows = []
        self.__ongoing_flows = []
        # TODO: read these from config file
        self.ideal_time = 100000
        self.threshold = 100000

    @dispatch()
    def capture(self) -> list:
        pass

    @dispatch(str)
    def capture(self, pcap_file: str) -> list:
        packets = rdpcap(pcap_file)
        for packet in packets:
            if packet.haslayer(HTTP):
                self.__add_packet_to_flow(packet, 'HTTP')
        return self.__finished_flows + self.__ongoing_flows

    def __add_packet_to_flow(self, packet: object, protocol: str) -> None:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
        flow = self.__search_for_flow(src_ip, dst_ip, src_port, dst_port, packet.time, protocol)
        if flow == None:
            self.__create_new_flow(src_ip, dst_ip, src_port, dst_port, protocol, packet)
        else:
            if self.__flow_is_ended(flow, packet):
                self.__ongoing_flows.remove(flow)
                self.__finished_flows.append(flow)
                self.__create_new_flow(src_ip, dst_ip, src_port, dst_port, protocol, packet)
            else:
                flow.add_packet(packet)

    def __flow_is_ended(self, flow: object, packet: object) -> bool:
        duration = packet.time - flow.get_timestamp()
        if duration > self.ideal_time or duration > self.threshold or flow.has_two_fin_flags() or \
                flow.has_rst_flag():
            return True
        return False


#    TODO: Improve it
    def __search_for_flow(self, src_ip: str, dst_ip: str, src_port: str, dst_port: str,
            timestamp: str, protocol: str) -> object:
        for flow in self.__ongoing_flows:
            if (flow.get_src_ip() == src_ip or flow.get_src_ip() == dst_ip) and \
               (flow.get_dst_ip() == src_ip or flow.get_dst_ip() == dst_ip) and \
               (flow.get_src_port() == src_port or flow.get_src_port() == dst_port) and \
               (flow.get_dst_port() == src_port or flow.get_dst_port() == dst_port) and \
               (flow.get_protocol() == protocol) and \
               (datetime.fromtimestamp(timestamp) >= datetime.fromtimestamp(flow.get_timestamp())):
                   return flow

        return None

    def __create_new_flow(self, src_ip: str, dst_ip: str, src_port: str, dst_port: str,
            protocol: str, packet: object) -> None:
        new_flow = Flow(src_ip, dst_ip, src_port, dst_port, packet.time, protocol)
        new_flow.add_packet(packet)
        self.__ongoing_flows.append(new_flow)
