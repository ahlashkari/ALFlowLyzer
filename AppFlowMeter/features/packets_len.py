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
        return stats.skew(packets_len)


class PacketsLenCoefficientOfVariation(Feature):
    name = "packets_length_coefficient_of_variation"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return stats.variation(packets_len)
    

class PacketsDeltaLenBase(Feature):
    def delta(self, flow: object) -> list:
        packets_len = [len(packet) for packet in flow.get_packets()]
        packets_del_len = [pkt - pkt_prev for pkt_prev, pkt in 
                           zip(packets_len[:-1], packets_len[1:])]
        return packets_del_len
    

class PacketsDeltaLenMin(PacketsDeltaLenBase):
    name = "packets_delta_length_min"
    def extract(self, flow: object) -> int:
        packets_del_len = super().delta(flow)
        return min(packets_del_len) if len(packets_del_len) > 0 else 0
    
    
class PacketsDeltaLenMax(PacketsDeltaLenBase):
    name = "packets_delta_length_max"
    def extract(self, flow: object) -> int:
        packets_del_len = super().delta(flow)
        return max(packets_del_len) if len(packets_del_len) > 0 else 0


class PacketsDeltaLenMean(PacketsDeltaLenBase):
    name = "packets_delta_length_mean"
    def extract(self, flow: object) -> float:
        packets_del_len = super().delta(flow)
        return statistics.mean(packets_del_len) if len(packets_del_len) > 0 else 0


class PacketsDeltaLenMode(PacketsDeltaLenBase):
    name = "packets_delta_length_mode"
    def extract(self, flow: object) -> int:
        packets_del_len = super().delta(flow)
        return statistics.mode(packets_del_len) if len(packets_del_len) > 0 else 0


class PacketsDeltaLenVariance(PacketsDeltaLenBase):
    name = "packets_delta_length_variance"
    def extract(self, flow: object) -> float:
        packets_del_len = super().delta(flow)
        return statistics.pvariance(packets_del_len) if len(packets_del_len) > 0 else 0


class PacketsDeltaLenStandardDeviation(PacketsDeltaLenBase):
    name = "packets_delta_length_standard_deviation"
    def extract(self, flow: object) -> float:
        packets_del_len = super().delta(flow)
        return statistics.pstdev(packets_del_len) if len(packets_del_len) > 0 else 0


class PacketsDeltaLenMedian(PacketsDeltaLenBase):
    name = "packets_delta_length_median"
    def extract(self, flow: object) -> float:
        packets_del_len = super().delta(flow)
        return statistics.median(packets_del_len) if len(packets_del_len) > 0 else 0


class PacketsDeltaLenSkewness(PacketsDeltaLenBase):
    name = "packets_delta_length_skewness"
    def extract(self, flow: object) -> float:
        packets_del_len = super().delta(flow)
        return stats.skew(packets_del_len) if len(packets_del_len) > 0 else 0


class PacketsDeltaLenCoefficientOfVariation(PacketsDeltaLenBase):
    name = "packets_delta_length_coefficient_of_variation"
    def extract(self, flow: object) -> float:
        packets_del_len = super().delta(flow)
        return stats.variation(packets_del_len) if len(packets_del_len) > 0 else 0
