#!/usr/bin/env python3

import statistics
from scipy import stats
from .feature import Feature
from . import utils


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
    def ReceivingDelta(self, flow: object) -> list:
        receiving_packets = utils.extract_incoming_packets(flow.get_packets(), flow.get_dst_ip())
        receiving_packets_timestamp = [packet.time for packet in receiving_packets]
        receiving_packets_sorted = [packet for _, packet in sorted(zip(receiving_packets_timestamp, 
                                                                       receiving_packets))]
        receiving_packets_len = [len(packet) for packet in receiving_packets_sorted]
        receiving_packets_del_len = [pkt - pkt_prev for pkt_prev, pkt in 
                           zip(receiving_packets_len[:-1], receiving_packets_len[1:])]
        return receiving_packets_del_len
    
    def SendingDelta(self, flow: object) -> list:
        sending_packets = utils.extract_outgoing_packets(flow.get_packets(), flow.get_dst_ip())
        sending_packets_timestamp = [packet.time for packet in sending_packets]
        sending_packets_sorted = [packet for _, packet in sorted(zip(sending_packets_timestamp, 
                                                                       sending_packets))]
        sending_packets_len = [len(packet) for packet in sending_packets_sorted]
        sending_packets_del_len = [pkt - pkt_prev for pkt_prev, pkt in 
                           zip(sending_packets_len[:-1], sending_packets_len[1:])]
        return sending_packets_del_len
    

class ReceivingPacketsDeltaLenMin(PacketsDeltaLenBase):
    name = "receiving_packets_delta_length_min"
    def extract(self, flow: object) -> int:
        receiving_packets_del_len = super().ReceivingDelta(flow)
        return min(receiving_packets_del_len) if len(receiving_packets_del_len) > 0 else 0
    
    
class ReceivingPacketsDeltaLenMax(PacketsDeltaLenBase):
    name = "receiving_packets_delta_length_max"
    def extract(self, flow: object) -> int:
        receiving_packets_del_len = super().ReceivingDelta(flow)
        return max(receiving_packets_del_len) if len(receiving_packets_del_len) > 0 else 0


class ReceivingPacketsDeltaLenMean(PacketsDeltaLenBase):
    name = "receiving_packets_delta_length_mean"
    def extract(self, flow: object) -> float:
        receiving_packets_del_len = super().ReceivingDelta(flow)
        return statistics.mean(receiving_packets_del_len) if len(receiving_packets_del_len) > 0 else 0


class ReceivingPacketsDeltaLenMode(PacketsDeltaLenBase):
    name = "receiving_packets_delta_length_mode"
    def extract(self, flow: object) -> int:
        receiving_packets_del_len = super().ReceivingDelta(flow)
        return statistics.mode(receiving_packets_del_len) if len(receiving_packets_del_len) > 0 else 0


class ReceivingPacketsDeltaLenVariance(PacketsDeltaLenBase):
    name = "receiving_packets_delta_length_variance"
    def extract(self, flow: object) -> float:
        receiving_packets_del_len = super().ReceivingDelta(flow)
        return statistics.pvariance(receiving_packets_del_len) if len(receiving_packets_del_len) > 0 else 0


class ReceivingPacketsDeltaLenStandardDeviation(PacketsDeltaLenBase):
    name = "receiving_packets_delta_length_standard_deviation"
    def extract(self, flow: object) -> float:
        receiving_packets_del_len = super().ReceivingDelta(flow)
        return statistics.pstdev(receiving_packets_del_len) if len(receiving_packets_del_len) > 0 else 0


class ReceivingPacketsDeltaLenMedian(PacketsDeltaLenBase):
    name = "receiving_packets_delta_length_median"
    def extract(self, flow: object) -> float:
        receiving_packets_del_len = super().ReceivingDelta(flow)
        return statistics.median(receiving_packets_del_len) if len(receiving_packets_del_len) > 0 else 0


class ReceivingPacketsDeltaLenSkewness(PacketsDeltaLenBase):
    name = "receiving_packets_delta_length_skewness"
    def extract(self, flow: object) -> float:
        receiving_packets_del_len = super().ReceivingDelta(flow)
        return stats.skew(receiving_packets_del_len) if len(receiving_packets_del_len) > 0 else 0


class ReceivingPacketsDeltaLenCoefficientOfVariation(PacketsDeltaLenBase):
    name = "receiving_packets_delta_length_coefficient_of_variation"
    def extract(self, flow: object) -> float:
        receiving_packets_del_len = super().ReceivingDelta(flow)
        return stats.variation(receiving_packets_del_len) if len(receiving_packets_del_len) > 0 else 0
    

class SendingPacketsDeltaLenMin(PacketsDeltaLenBase):
    name = "sending_packets_delta_length_min"
    def extract(self, flow: object) -> int:
        sending_packets_del_len = super().SendingDelta(flow)
        return min(sending_packets_del_len) if len(sending_packets_del_len) > 0 else 0
    
    
class SendingPacketsDeltaLenMax(PacketsDeltaLenBase):
    name = "sending_packets_delta_length_max"
    def extract(self, flow: object) -> int:
        sending_packets_del_len = super().SendingDelta(flow)
        return max(sending_packets_del_len) if len(sending_packets_del_len) > 0 else 0


class SendingPacketsDeltaLenMean(PacketsDeltaLenBase):
    name = "sending_packets_delta_length_mean"
    def extract(self, flow: object) -> float:
        sending_packets_del_len = super().SendingDelta(flow)
        return statistics.mean(sending_packets_del_len) if len(sending_packets_del_len) > 0 else 0


class SendingPacketsDeltaLenMode(PacketsDeltaLenBase):
    name = "sending_packets_delta_length_mode"
    def extract(self, flow: object) -> int:
        sending_packets_del_len = super().SendingDelta(flow)
        return statistics.mode(sending_packets_del_len) if len(sending_packets_del_len) > 0 else 0


class SendingPacketsDeltaLenVariance(PacketsDeltaLenBase):
    name = "sending_packets_delta_length_variance"
    def extract(self, flow: object) -> float:
        sending_packets_del_len = super().SendingDelta(flow)
        return statistics.pvariance(sending_packets_del_len) if len(sending_packets_del_len) > 0 else 0


class SendingPacketsDeltaLenStandardDeviation(PacketsDeltaLenBase):
    name = "sending_packets_delta_length_standard_deviation"
    def extract(self, flow: object) -> float:
        sending_packets_del_len = super().SendingDelta(flow)
        return statistics.pstdev(sending_packets_del_len) if len(sending_packets_del_len) > 0 else 0


class SendingPacketsDeltaLenMedian(PacketsDeltaLenBase):
    name = "sending_packets_delta_length_median"
    def extract(self, flow: object) -> float:
        sending_packets_del_len = super().SendingDelta(flow)
        return statistics.median(sending_packets_del_len) if len(sending_packets_del_len) > 0 else 0


class SendingPacketsDeltaLenSkewness(PacketsDeltaLenBase):
    name = "sending_packets_delta_length_skewness"
    def extract(self, flow: object) -> float:
        sending_packets_del_len = super().SendingDelta(flow)
        return stats.skew(sending_packets_del_len) if len(sending_packets_del_len) > 0 else 0


class SendingPacketsDeltaLenCoefficientOfVariation(PacketsDeltaLenBase):
    name = "sending_packets_delta_length_coefficient_of_variation"
    def extract(self, flow: object) -> float:
        sending_packets_del_len = super().SendingDelta(flow)
        return stats.variation(sending_packets_del_len) if len(sending_packets_del_len) > 0 else 0