#!/usr/bin/env python3

from .feature import Feature
from . import utils


class PacketsNumbers(Feature):
    name = "packets_numbers"
    def extract(self, flow: object) -> int:
        return len(flow.get_packets())


class ReceivingPacketsNumbers(Feature):
    name = "receiving_packets_numbers"
    def extract(self, flow: object) -> int:
        return len(utils.extract_receiving_packets(flow.get_packets(), flow.get_dst_ip()))


class SendingPacketsNumbers(Feature):
    name = "sending_packets_numbers"
    def extract(self, flow: object) -> int:
        return len(utils.extract_sending_packets(flow.get_packets(), flow.get_dst_ip()))
