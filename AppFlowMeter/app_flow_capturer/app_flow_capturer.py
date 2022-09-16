#!/usr/bin/env python3

import dpkt
import os
from multiprocessing import Lock
from AppFlowMeter.app_flow_capturer.flow import DNSFlow
from .packet import Packet
from .flow_factory import FlowFactory

class AppFlowCapturer(object):
    def __init__(self, max_flow_duration: int, activity_timeout: int):
        self.__finished_flows = []
        self.__ongoing_flows = []
        self.max_flow_duration = max_flow_duration
        self.activity_timeout = activity_timeout
        self.flow_factory = FlowFactory()
        self.thread_number = -1

    def capture(self, thread_number: int, pcap_file: str, flows: list, flows_lock: Lock,
            thread_pid: list) -> list:
        thread_pid.set(os.getpid())
        self.thread_number = thread_number
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
                print('\nError Parsing DNS, Might be a truncated packet...')
                print('Exception: {!r}'.format(e))
                continue

            app_flow_packet = Packet(buf, ts)
            self.__add_packet_to_flow(app_flow_packet, flows, flows_lock)
            if i % 10000 == 0:
                print(">> ", self.thread_number, " >>", i, "number of packets has been processed from", pcap_file)

        with flows_lock:
            print(50*"#")
            flows.extend(self.__finished_flows)
            flows.extend(self.__ongoing_flows)
            print(50*"#")
        return self.__finished_flows + self.__ongoing_flows

    def __add_packet_to_flow(self, packet: Packet, flows: list, flows_lock: Lock) -> None:
        src_ip = packet.get_src_ip()
        dst_ip = packet.get_dst_ip()
        src_port = packet.get_src_port()
        dst_port = packet.get_dst_port()
        transaction_id = packet.get_transaction_id()
        flow = self.__search_for_flow(src_ip, dst_ip, src_port, dst_port, packet.get_timestamp(),
                packet.get_application_protocol(), transaction_id)
        if flow == None:
            self.__ongoing_flows.append(self.flow_factory.create(packet))
            return

        if flow.is_ended(packet, self.max_flow_duration, self.activity_timeout):
            self.__ongoing_flows.remove(flow)
            self.__finished_flows.append(flow)
            self.__ongoing_flows.append(self.flow_factory.create(packet))

            # TODO: read from file
            if len(self.__ongoing_flows) >= 8000:
                # TODO: read from file
                dns_activity_timeout = 30
                for oflow in self.__ongoing_flows:
                    timeout = self.activity_timeout
                    if isinstance(oflow, DNSFlow):
                        timeout = dns_activity_timeout
                    active_time = packet.get_timestamp() - oflow.get_last_packet_timestamp()
                    if active_time >= timeout:
                        self.__ongoing_flows.remove(oflow)
                        self.__finished_flows.append(oflow)
            if len(self.__finished_flows) >= 5000:
                with flows_lock:
                    print(50*"@")
                    flows.extend(self.__finished_flows.copy())
                    self.__finished_flows.clear()
                    print(50*"@")
            return

        flow.add_packet(packet)


    def __search_for_flow(self, src_ip: str, dst_ip: str, src_port: str, dst_port: str,
            timestamp: str, protocol: str, transaction_id: int) -> object:
        for flow in self.__ongoing_flows:
            if flow.equality_check(src_ip, dst_ip, src_port, dst_port, timestamp, protocol,
                    transaction_id):
                return flow
        return None
