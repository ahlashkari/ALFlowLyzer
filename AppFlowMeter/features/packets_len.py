#!/usr/bin/env python3

import statistics
from scipy import stats
from .feature import Feature


class PacketsLen(Feature):
    def __init__(self):
        self.data = { "src_ip": [], "dst_ip": [], "src_port": [], "dst_port": []}

    def extract(self, flows: list) -> dict:
        pass


class PacketsLenMin(PacketsLen):
    def extract(self, flows: list) -> dict:
        self.data["min_packets_length"] = []
        for flow in flows:
            self.data["src_ip"].append(flow.get_src_ip())
            self.data["dst_ip"].append(flow.get_dst_ip())
            self.data["src_port"].append(flow.get_src_port())
            self.data["dst_port"].append(flow.get_dst_port())
            packets_len = [len(packet) for packet in flow.get_packets()]
            self.data["min_packets_length"].append(min(packets_len))
        return self.data


class PacketsLenMax(PacketsLen):
    def extract(self, flows: list) -> dict:
        self.data["max_packets_length"] = []
        for flow in flows:
            self.data["src_ip"].append(flow.get_src_ip())
            self.data["dst_ip"].append(flow.get_dst_ip())
            self.data["src_port"].append(flow.get_src_port())
            self.data["dst_port"].append(flow.get_dst_port())
            packets_len = [len(packet) for packet in flow.get_packets()]
            self.data["max_packets_length"].append(max(packets_len))
        return self.data


class PacketsLenMean(PacketsLen):
    def extract(self, flows: list) -> dict:
        self.data["mean_packets_length"] = []
        for flow in flows:
            self.data["src_ip"].append(flow.get_src_ip())
            self.data["dst_ip"].append(flow.get_dst_ip())
            self.data["src_port"].append(flow.get_src_port())
            self.data["dst_port"].append(flow.get_dst_port())
            packets_len = [len(packet) for packet in flow.get_packets()]
            self.data["mean_packets_length"].append(statistics.mean(packets_len))
        return self.data


class PacketsLenMode(PacketsLen):
    def extract(self, flows: list) -> dict:
        self.data["mode_packets_length"] = []
        for flow in flows:
            self.data["src_ip"].append(flow.get_src_ip())
            self.data["dst_ip"].append(flow.get_dst_ip())
            self.data["src_port"].append(flow.get_src_port())
            self.data["dst_port"].append(flow.get_dst_port())
            packets_len = [len(packet) for packet in flow.get_packets()]
            self.data["mode_packets_length"].append(statistics.mode(packets_len))
        return self.data


class PacketsLenVariance(PacketsLen):
    def extract(self, flows: list) -> dict:
        self.data["variance_packets_length"] = []
        for flow in flows:
            self.data["src_ip"].append(flow.get_src_ip())
            self.data["dst_ip"].append(flow.get_dst_ip())
            self.data["src_port"].append(flow.get_src_port())
            self.data["dst_port"].append(flow.get_dst_port())
            packets_len = [len(packet) for packet in flow.get_packets()]
            self.data["variance_packets_length"].append(statistics.pvariance(packets_len))
        return self.data


class PacketsLenStandardDeviation(PacketsLen):
    def extract(self, flows: list) -> dict:
        self.data["standard_deviation_packets_length"] = []
        for flow in flows:
            self.data["src_ip"].append(flow.get_src_ip())
            self.data["dst_ip"].append(flow.get_dst_ip())
            self.data["src_port"].append(flow.get_src_port())
            self.data["dst_port"].append(flow.get_dst_port())
            packets_len = [len(packet) for packet in flow.get_packets()]
            self.data["standard_deviation_packets_length"].append(statistics.pstdev(packets_len))
        return self.data


class PacketsLenMedian(PacketsLen):
    def extract(self, flows: list) -> dict:
        self.data["median_packets_length"] = []
        for flow in flows:
            self.data["src_ip"].append(flow.get_src_ip())
            self.data["dst_ip"].append(flow.get_dst_ip())
            self.data["src_port"].append(flow.get_src_port())
            self.data["dst_port"].append(flow.get_dst_port())
            packets_len = [len(packet) for packet in flow.get_packets()]
            self.data["median_packets_length"].append(statistics.median(packets_len))
        return self.data


class PacketsLenSkewness(PacketsLen):
    def extract(self, flows: list) -> dict:
        self.data["skewness_packets_length"] = []
        for flow in flows:
            self.data["src_ip"].append(flow.get_src_ip())
            self.data["dst_ip"].append(flow.get_dst_ip())
            self.data["src_port"].append(flow.get_src_port())
            self.data["dst_port"].append(flow.get_dst_port())
            packets_len = [len(packet) for packet in flow.get_packets()]
            self.data["skewness_packets_length"].append(statistics.median(packets_len))
        return self.data


class PacketsLenCoefficientOfVariation(PacketsLen):
    def extract(self, flows: list) -> dict:
        self.data["median_packets_length"] = []
        for flow in flows:
            self.data["src_ip"].append(flow.get_src_ip())
            self.data["dst_ip"].append(flow.get_dst_ip())
            self.data["src_port"].append(flow.get_src_port())
            self.data["dst_port"].append(flow.get_dst_port())
            packets_len = [len(packet) for packet in flow.get_packets()]
            self.data["median_packets_length"].append(stats.skew(packets_len))
        return self.data
