#!/usr/bin/env python3

from .feature import Feature
from . import utils


class PacketsNumbers(Feature):
    name = "packets_numbers"
    def extract(self, flow: object) -> int:
        return len(flow.get_packets())


class IncomingPacketsNumbers(Feature):
    name = "incoming_packets_numbers"
    def extract(self, flow: object) -> int:
        return len(utils.extract_incoming_packets(flow.get_packets(), flow.get_dst_ip()))


class OutgoingPacketsNumbers(Feature):
    name = "outgoing_packets_numbers"
    def extract(self, flow: object) -> int:
        return len(utils.extract_outgoing_packets(flow.get_packets(), flow.get_dst_ip()))
