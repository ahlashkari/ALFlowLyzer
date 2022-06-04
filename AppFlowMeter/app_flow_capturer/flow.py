#!/usr/bin/env python3

from datetime import datetime

class Flow(object):
    def __init__(self, src_ip: str, dst_ip: str, src_port: str, dst_port: str, timestamp: str,
            protocol: str):
        self.__src_ip = src_ip
        self.__dst_ip = dst_ip
        self.__src_port = src_port
        self.__dst_port = dst_port
        self._timestamp = timestamp
        self.__protocol = protocol
        self.__packets = []
        self.__number_of_fin_flags = 0
        self.__has_rst_flag = False
        self._last_packet_timestamp = timestamp

    def __str__(self):
        return str(datetime.fromtimestamp(self._timestamp)) + '_' + self.__src_ip + '_' + \
                str(self.__src_port) + '_' + self.__dst_ip + '_' + str(self.__dst_port) + \
                '_' + self.__protocol

    # TODO: check line lengths
    def __eq__(self, other):
        if isinstance(other, Flow):
            if self.equality_check(other.get_src_ip(), other.get_dst_ip(), other.get_src_port(),
                    other.get_dst_port(), other.get_timestamp(), other.get_protocol()):
                return True
        return False

    def equality_check(self, src_ip: str, dst_ip: str, src_port: str, dst_port: str,
            timestamp: str, protocol: str) -> bool:
        if (self.__src_ip == src_ip or self.__dst_ip == src_ip) and \
           (self.__src_ip == dst_ip or self.__dst_ip == dst_ip) and \
           (self.__src_port == src_port or self.__dst_port == src_port) and \
           (self.__src_port == dst_port or self.__dst_port == dst_port) and \
           (self.__protocol == protocol) and \
           (datetime.fromtimestamp(self._timestamp) <= datetime.fromtimestamp(timestamp)):
           return True
        return False

    def add_packet(self, packet) -> None:
        self.__packets.append(packet)
        self._last_packet_timestamp = packet.get_timestamp()
        # TODO: check for forward and backward FIN
        if 'F' in packet.get_tcp_flags():
            self.__number_of_fin_flags += 1
        if 'R' in packet.get_tcp_flags():
            self.__has_rst_flag = True

    def get_src_ip(self) -> str:
        return self.__src_ip

    def get_dst_ip(self) -> str:
        return self.__dst_ip

    def get_src_port(self) -> str:
        return self.__src_port

    def get_dst_port(self) -> str:
        return self.__dst_port

    def get_timestamp(self) -> str:
        return self._timestamp

    def get_protocol(self) -> str:
        return self.__protocol

    def get_packets(self) -> list:
        return self.__packets

    def has_two_fin_flags(self) -> bool:
        if self.__number_of_fin_flags >= 2:
            return True
        return False

    def has_rst_flag(self) -> bool:
        return self.__has_rst_flag

    def get_last_packet_timestamp(self) -> str:
        return self._last_packet_timestamp

    # TODO: change configuration class to be singleton
    # TODO: check the function name
    def is_ended(self, packet: object, max_flow_duration: int, activity_timeout: int) -> bool:
        flow_duration = packet.get_timestamp() - self._timestamp
        active_time = packet.get_timestamp() - self._last_packet_timestamp
        if flow_duration > max_flow_duration or active_time > activity_timeout or \
                self.has_two_fin_flags() or self.has_rst_flag():
            return True
        return False


class DNSFlow(Flow):
    def __init__(self, src_ip: str, dst_ip: str, src_port: str, dst_port: str, timestamp: str,
            protocol: str, transaction_id: int):
        super().__init__(src_ip, dst_ip, src_port, dst_port, timestamp, protocol)
        self.__transaction_id = transaction_id

    def __str__(self):
        return super().__str__() + '_' + str(self.__transaction_id)

    def __eq__(self, other):
        if isinstance(other, DNSFlow):
            if super().__eq__(other):
                if other.get_transaction_id() == self.__transaction_id:
                    return True
        return False

    def get_transaction_id(self) -> int:
        return self.__transaction_id

    def is_ended(self, packet: object, max_flow_duration: int, activity_timeout: int) -> bool:
        # TODO: check dns timeout=30 sec
        flow_duration = packet.get_timestamp() - self._timestamp
        active_time = packet.get_timestamp() - self._last_packet_timestamp
        if flow_duration > max_flow_duration or active_time > activity_timeout:
            return True
        return False