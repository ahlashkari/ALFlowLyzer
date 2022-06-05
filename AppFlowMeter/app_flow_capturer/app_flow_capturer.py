#!/usr/bin/env python3

from datetime import datetime
from multipledispatch import dispatch
from scapy.all import *
from .flow import Flow, DNSFlow
from .packet import Packet
from .protocols import Protocols

class AppFlowCapturer(object):
    def __init__(self, max_flow_duration: int, activity_timeout: int):
        self.__finished_flows = []
        self.__ongoing_flows = []
        self.max_flow_duration = max_flow_duration
        self.activity_timeout = activity_timeout

    @dispatch()
    def capture(self) -> list:
        pass

    @dispatch(str)
    def capture(self, pcap_file: str) -> list:
        sniff(offline=pcap_file, prn=self.packet_processing, store=0)
        return self.__finished_flows + self.__ongoing_flows

    def packet_processing(self, scapy_packet):
        if IP not in scapy_packet:
            return
        if TCP not in scapy_packet and UDP not in scapy_packet:
            return
        app_flow_packet = Packet(scapy_packet)
        self.__add_packet_to_flow(app_flow_packet)

    def __add_packet_to_flow(self, packet: object) -> None:
        src_ip = packet.get_src_ip()
        dst_ip = packet.get_dst_ip()
        src_port = packet.get_src_port()
        dst_port = packet.get_dst_port()
        transaction_id = packet.get_transaction_id()
        flow = self.__search_for_flow(src_ip, dst_ip, src_port, dst_port, packet.get_timestamp(),
                packet.get_application_protocol(), transaction_id)
        if flow == None:
            self.__create_new_flow(src_ip, dst_ip, src_port, dst_port, packet)
        else:
            if flow.is_ended(packet, self.max_flow_duration, self.activity_timeout):
                self.__ongoing_flows.remove(flow)
                self.__finished_flows.append(flow)
                self.__create_new_flow(src_ip, dst_ip, src_port, dst_port, packet)
            else:
                flow.add_packet(packet)

    def __search_for_flow(self, src_ip: str, dst_ip: str, src_port: str, dst_port: str,
            timestamp: str, protocol: str, transaction_id: int) -> object:
        for flow in self.__ongoing_flows:
            if flow.equality_check(src_ip, dst_ip, src_port, dst_port, timestamp, protocol, transaction_id):
                return flow
        return None

    # Factory design pattern
    def __create_new_flow(self, src_ip: str, dst_ip: str, src_port: str, dst_port: str,
            packet: object) -> None:
        if "DNS" == packet.get_application_protocol():
            new_flow = DNSFlow(src_ip, dst_ip, src_port, dst_port, packet.get_timestamp(),
                    packet.get_application_protocol(), packet.get_transaction_id())
        else:
            new_flow = Flow(src_ip, dst_ip, src_port, dst_port, packet.get_timestamp(),
                    packet.get_application_protocol())

        new_flow.add_packet(packet)
        self.__ongoing_flows.append(new_flow)
