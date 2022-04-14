#!/usr/bin/env python3

from .feature import Feature

class PacketsNumbers(Feature):
    def extract(self, flows: list) -> dict:
        data = { "src_ip": [], "dst_ip": [], "src_port": [], "dst_port": [], "packets_numbers": []}
        for flow in flows:
            data["src_ip"].append(flow.get_src_ip())
            data["dst_ip"].append(flow.get_dst_ip())
            data["src_port"].append(flow.get_src_port())
            data["dst_port"].append(flow.get_dst_port())
            data["packets_numbers"].append(len(flow.get_packets()))
        return data
