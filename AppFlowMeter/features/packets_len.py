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
