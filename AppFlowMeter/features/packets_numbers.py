#!/usr/bin/env python3

from .feature import Feature

class PacketsNumbers(Feature):
    name = "packets_numbers"
    def extract(self, flow: object) -> dict:
        return len(flow.get_packets())
