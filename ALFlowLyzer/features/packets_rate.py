#!/usr/bin/env python3

from .feature import Feature
from . import utils


class PacketsRate(Feature):
    name = "packets_rate"
    def extract(self, flow: object) -> float:
        if len(flow.get_packets()) <= 1:
            return 0
        return format(len(flow.get_packets()) / utils.calculate_duration(flow.get_packets()),
                     self.floating_point_unit)


class ReceivingPacketsRate(Feature):
    name = "receiving_packets_rate"
    def extract(self, flow: object) -> float:
        receiving_packets = utils.extract_receiving_packets(flow.get_packets(), flow.get_dst_ip())
        if len(receiving_packets) <= 1:
            return 0
        return format(len(receiving_packets) / utils.calculate_duration(receiving_packets),
                     self.floating_point_unit)


class SendingPacketsRate(Feature):
    name = "sending_packets_rate"
    def extract(self, flow: object) -> float:
        sending_packets = utils.extract_sending_packets(flow.get_packets(), flow.get_dst_ip())
        if len(sending_packets) <= 1:
            return 0
        return format(len(sending_packets) / utils.calculate_duration(sending_packets),
                     self.floating_point_unit)


class PacketsLenRate(Feature):
    name = "packets_len_rate"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        packets_timestamp = [float(packet.get_timestamp()) for packet in flow.get_packets()]

        if len(packets_len) > 1:
            return format(sum(packets_len) / utils.calculate_duration(flow.get_packets()),
                         self.floating_point_unit)
        else:
            return 0


class SendingPacketsLenRate(Feature):
    name = "sending_packets_len_rate"
    def extract(self, flow: object) -> float:
        sending_packets = utils.extract_sending_packets(flow.get_packets(), flow.get_dst_ip())
        sending_packets_len = [len(packet) for packet in sending_packets]
        sending_packets_timestamp = [float(packet.get_timestamp()) for packet in sending_packets]

        if len(sending_packets_len) > 1:
            return format(sum(sending_packets_len) / utils.calculate_duration(sending_packets),
                         self.floating_point_unit)
        else:
            return 0


class ReceivingPacketsLenRate(Feature):
    name = "receiving_packets_len_rate"
    def extract(self, flow: object) -> float:
        receiving_packets = utils.extract_receiving_packets(flow.get_packets(), flow.get_dst_ip())
        receiving_packets_len = [len(packet) for packet in receiving_packets]
        receiving_packets_timestamp = [float(packet.get_timestamp()) for packet in receiving_packets]

        if len(receiving_packets_len) > 1:
            return format(sum(receiving_packets_len) / utils.calculate_duration(receiving_packets),
                         self.floating_point_unit)
        else:
            return 0
