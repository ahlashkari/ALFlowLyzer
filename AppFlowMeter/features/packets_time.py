#!/usr/bin/env python3

import statistics
from scipy import stats
from .feature import Feature


class ConnectionTime(Feature):
    def extract(self, flows: list) -> dict:
        self.data = { "src_ip": [], "dst_ip": [], "src_port": [], "dst_port": []}
        self.data["connection_time"] = []
        for flow in flows:
            self.data["src_ip"].append(flow.get_src_ip())
            self.data["dst_ip"].append(flow.get_dst_ip())
            self.data["src_port"].append(flow.get_src_port())
            self.data["dst_port"].append(flow.get_dst_port())
            packets_time = [packet.time for packet in flow.get_packets()]
            timestamps = [packet.time for packet in flow.get_packets()]
            self.data["connection_time"].append(max(packets_time) - min(packets_time))
        return self.data
