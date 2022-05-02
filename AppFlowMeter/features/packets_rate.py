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
    
    
class SuccessfulPacketsRate(Feature):
    name = "success_packets_rate"
    def extract(self, flow: object) -> float:
        success_packets = utils.extract_successful_packets(flow.get_packets(), flow.get_dst_ip())
        if len(success_packets) <= 1:
            return 0
        return format(len(success_packets) / utils.calculate_duration(flow.get_packets()),
                     self.floating_point_unit)
