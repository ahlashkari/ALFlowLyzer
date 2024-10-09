#!/usr/bin/env python3

import dpkt
from ALFlowLyzer.application_flow_capturer.flow import DNSFlow
from .packet import Packet
from .flow_factory import FlowFactory

class AppFlowCapturer(object):
    def __init__(self, max_flow_duration: int, activity_timeout: int, dns_activity_timeout: int,
                check_flows_ending_min_flows: int, capturer_updating_flows_min_value: int,
                read_packets_count_value_log_info: int):
        self.__finished_flows = []
        self.__ongoing_flows = []
        self.__max_flow_duration = max_flow_duration
        self.__activity_timeout = activity_timeout
        self.__dns_activity_timeout = dns_activity_timeout
        self.__check_flows_ending_min_flows = check_flows_ending_min_flows
        self.__capturer_updating_flows_min_value = capturer_updating_flows_min_value
        self.__read_packets_count_value_log_info = read_packets_count_value_log_info
        self.__flow_factory = FlowFactory()
        self.__number_of_flows = 0

    def capture(self, pcap_file: str, flows: list, flows_lock, thread_finished) -> list:
        f = open(pcap_file, 'rb')
        pcap = dpkt.pcap.Reader(f)
        i = 0
        for ts, buf in pcap:
            i +=1
            try:
                eth = dpkt.ethernet.Ethernet(buf)
                if not isinstance(eth.data, dpkt.ip.IP):
                    continue
                ip = eth.data
                if not isinstance(ip.data, dpkt.udp.UDP) and \
                        not isinstance(ip.data, dpkt.tcp.TCP):
                    continue

            except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError, Exception) as e:
                print(f"Error encountered during the pcap file reading process: {e}")
                continue

            app_flow_packet = Packet(buf, ts)
            self.__add_packet_to_flow(app_flow_packet, flows, flows_lock)
            if i % self.__read_packets_count_value_log_info == 0:
                print(">>", i, "number of packets has been processed...")

        with flows_lock:
            flows.extend(self.__finished_flows)
            flows.extend(self.__ongoing_flows)
            self.__number_of_flows += len(self.__finished_flows)
            self.__number_of_flows += len(self.__ongoing_flows)


        print(">> end of reading from", pcap_file)
        thread_finished.set(True)
        print(f">> {self.__number_of_flows} number of flows created in total.")
        return self.__finished_flows + self.__ongoing_flows

    def __add_packet_to_flow(self, packet: Packet, flows: list, flows_lock) -> None:
        src_ip = packet.get_src_ip()
        dst_ip = packet.get_dst_ip()
        src_port = packet.get_src_port()
        dst_port = packet.get_dst_port()
        transaction_id = packet.get_transaction_id()
        flow = self.__search_for_flow(src_ip, dst_ip, src_port, dst_port, packet.get_timestamp(),
                packet.get_application_protocol(), transaction_id)
        if flow == None:
            self.__ongoing_flows.append(self.__flow_factory.create(
                    packet, self.__activity_timeout, self.__dns_activity_timeout))
            return

        if flow.is_ended(packet, self.__max_flow_duration):
            self.__ongoing_flows.remove(flow)
            self.__finished_flows.append(flow)
            self.__ongoing_flows.append(self.__flow_factory.create(
                    packet, self.__activity_timeout, self.__dns_activity_timeout))

            if len(self.__ongoing_flows) >= self.__check_flows_ending_min_flows:
                for oflow in self.__ongoing_flows:
                    if oflow.actvity_timeout(packet):
                        self.__ongoing_flows.remove(oflow)
                        self.__finished_flows.append(oflow)
            if len(self.__finished_flows) >= self.__capturer_updating_flows_min_value:
                with flows_lock:
                    flows.extend(self.__finished_flows)
                    self.__number_of_flows += len(self.__finished_flows)
                    self.__finished_flows.clear()
            return
        flow.add_packet(packet)

    def __search_for_flow(self, src_ip: str, dst_ip: str, src_port: str, dst_port: str,
            timestamp: str, protocol: str, transaction_id: int) -> object:
        for flow in self.__ongoing_flows:
            if flow.equality_check(src_ip, dst_ip, src_port, dst_port, timestamp, protocol,
                    transaction_id):
                return flow
        return None
