#!/usr/bin/env python3

import statistics
from scipy import stats
from .feature import Feature


class PacketsLenMin(Feature):
    name = "packets_length_min"
    def extract(self, flow: object) -> int:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return min(packets_len)


class PacketsLenMax(Feature):
    name = "packets_length_max"
    def extract(self, flow: object) -> int:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return max(packets_len)


class PacketsLenMean(Feature):
    name = "packets_length_mean"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return statistics.mean(packets_len)


class PacketsLenMode(Feature):
    name = "packets_length_mode"
    def extract(self, flow: object) -> int:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return statistics.mode(packets_len)


class PacketsLenVariance(Feature):
    name = "packets_length_variance"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return statistics.pvariance(packets_len)


class PacketsLenStandardDeviation(Feature):
    name = "packets_length_standard_deviation"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return statistics.pstdev(packets_len)


class PacketsLenMedian(Feature):
    name = "packets_length_median"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return statistics.median(packets_len)


class PacketsLenSkewness(Feature):
    name = "packets_length_skewness"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return statistics.median(packets_len)

class PacketsLenCoefficientOfVariation(Feature):
    name = "packets_length_coefficient_of_variation"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return stats.skew(packets_len)
    
#Del L feature class
class PacketsDelLenMin(Feature):
    name = "packets_del_length_min"
    def extract(self, flow: object) -> int:
        packets_len = [len(packet) for packet in flow.get_packets()]
        packets_del_len = [pkt - pkt_prev for pkt_prev, pkt in 
                           zip(packets_len[:-1], packets_len[1:])]
        print(packets_len)
        print(packets_del_len)
        return min(packets_del_len) if len(packets_del_len)>0 else 0
    
class PacketsDelLenMax(Feature):
    name = "packets_del_length_max"
    def extract(self, flow: object) -> int:
        packets_len = [len(packet) for packet in flow.get_packets()]
        packets_del_len = [pkt - pkt_prev for pkt_prev, pkt in 
                           zip(packets_len[:-1], packets_len[1:])]
        return max(packets_del_len) if len(packets_del_len)>0 else 0

class PacketsDelLenMean(Feature):
    name = "packets_del_length_mean"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        packets_del_len = [pkt - pkt_prev for pkt_prev, pkt in 
                           zip(packets_len[:-1], packets_len[1:])]
        return statistics.mean(packets_del_len) if len(packets_del_len)>0 else 0

class PacketsDelLenMode(Feature):
    name = "packets_del_length_mode"
    def extract(self, flow: object) -> int:
        packets_len = [len(packet) for packet in flow.get_packets()]
        packets_del_len = [pkt - pkt_prev for pkt_prev, pkt in 
                           zip(packets_len[:-1], packets_len[1:])]
        return statistics.mode(packets_del_len) if len(packets_del_len)>0 else 0


class PacketsDelLenVariance(Feature):
    name = "packets_del_length_variance"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        packets_del_len = [pkt - pkt_prev for pkt_prev, pkt in 
                           zip(packets_len[:-1], packets_len[1:])]
        return statistics.pvariance(packets_del_len) if len(packets_del_len)>0 else 0


class PacketsDelLenStandardDeviation(Feature):
    name = "packets_del_length_standard_deviation"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        packets_del_len = [pkt - pkt_prev for pkt_prev, pkt in 
                           zip(packets_len[:-1], packets_len[1:])]
        return statistics.pstdev(packets_del_len) if len(packets_del_len)>0 else 0


class PacketsDelLenMedian(Feature):
    name = "packets_del_length_median"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        packets_del_len = [pkt - pkt_prev for pkt_prev, pkt in 
                           zip(packets_len[:-1], packets_len[1:])]
        return statistics.median(packets_del_len) if len(packets_del_len)>0 else 0


class PacketsDelLenSkewness(Feature):
    name = "packets_del_length_skewness"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        packets_del_len = [pkt - pkt_prev for pkt_prev, pkt in 
                           zip(packets_len[:-1], packets_len[1:])]
        return statistics.median(packets_del_len) if len(packets_del_len)>0 else 0

class PacketsDelLenCoefficientOfVariation(Feature):
    name = "packets_del_length_coefficient_of_variation"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        packets_del_len = [pkt - pkt_prev for pkt_prev, pkt in 
                           zip(packets_len[:-1], packets_len[1:])]
        return stats.skew(packets_del_len) if len(packets_del_len)>0 else 0
