#!/usr/bin/env python3

from datetime import datetime
from multipledispatch import dispatch
from scapy.all import *
from .flow import Flow
from .packet import Packet

class AppFlowCapturer(object):
    def __init__(self):
        self.__finished_flows = []
        self.__ongoing_flows = []
        # TODO: read these from config file
        self.max_flow_duration = 120000
        self.activity_timeout = 5000

    @dispatch()
    def capture(self) -> list:
        pass

    @dispatch(str)
    def capture(self, pcap_file: str) -> list:
        sniff(offline=pcap_file, filter="ip", prn=self.packet_processing, store=0)
        return self.__finished_flows + self.__ongoing_flows

    def packet_processing(self, pkt):
        packet = Packet(pkt)
        self.__add_packet_to_flow(packet)

    def __add_packet_to_flow(self, packet: object) -> None:
        src_ip = packet.get_src_ip()
        dst_ip = packet.get_dst_ip()
        src_port = packet.get_src_port()
        dst_port = packet.get_dst_port()
        flow = self.__search_for_flow(src_ip, dst_ip, src_port, dst_port, packet.get_timestamp(),
                packet.get_application_protocol())
        if flow == None:
            self.__create_new_flow(src_ip, dst_ip, src_port, dst_port, packet)
        else:
            if self.__flow_is_ended(flow, packet):
                self.__ongoing_flows.remove(flow)
                self.__finished_flows.append(flow)
                self.__create_new_flow(src_ip, dst_ip, src_port, dst_port, packet)
            else:
                flow.add_packet(packet)

    def __flow_is_ended(self, flow: object, packet: object) -> bool:
        flow_duration = packet.get_timestamp() - flow.get_timestamp()
        active_time = packet.get_timestamp() - flow.get_last_packet_timestamp()
        if flow_duration > self.max_flow_duration or active_time > self.activity_timeout or \
                flow.has_two_fin_flags() or flow.has_rst_flag():

            return True
        return False

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
            packet: object) -> None:
        new_flow = Flow(src_ip, dst_ip, src_port, dst_port, packet.get_timestamp(),
                packet.get_application_protocol())
        new_flow.add_packet(packet)
        self.__ongoing_flows.append(new_flow)
