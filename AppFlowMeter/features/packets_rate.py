#!/usr/bin/env python3

from .feature import Feature
from . import utils


class PacketsRate(Feature):
    name = "packets_rate"
    def extract(self, flow: object) -> float:
        if len(flow.get_packets()) <= 1:
            return 0
        return len(flow.get_packets()) / utils.calculate_duration(flow.get_packets())


class IncomingPacketsRate(Feature):
    name = "incoming_packets_rate"
    def extract(self, flow: object) -> float:
        incoming_packets = utils.extract_incoming_packets(flow.get_packets(), flow.get_dst_ip())
        if len(incoming_packets) <= 1:
            return 0
        return len(incoming_packets) / utils.calculate_duration(incoming_packets)


class OutgoingPacketsRate(Feature):
    name = "outgoing_packets_rate"
    def extract(self, flow: object) -> float:
        outgoing_packets = utils.extract_outgoing_packets(flow.get_packets(), flow.get_dst_ip())
        if len(outgoing_packets) <= 1:
            return 0
        return len(outgoing_packets) / utils.calculate_duration(outgoing_packets)
