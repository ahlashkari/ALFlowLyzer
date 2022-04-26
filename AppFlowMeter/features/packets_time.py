#!/usr/bin/env python3

import statistics
from scipy import stats
from .feature import Feature
from . import utils


class ConnectionTime(Feature):
    name = "connection_time"
    def extract(self, flow: object) -> float:
        return utils.calculate_duration(flow.get_packets())


class PacketsDeltaTimeBase(Feature):
    def ReceivingDelta(self, flow: object) -> list:
        receiving_packets = utils.extract_incoming_packets(flow.get_packets(), flow.get_dst_ip())
        receiving_packets_timestamp = [float(packet.time) for packet in receiving_packets]
        receiving_packets_timestamp_sorted = sorted(receiving_packets_timestamp)
        receiving_packets_del_time = [pkt - pkt_prev for pkt_prev, pkt in
                           zip(receiving_packets_timestamp_sorted[:-1], receiving_packets_timestamp_sorted[1:])]
        return receiving_packets_del_time

    def SendingDelta(self, flow: object) -> list:
        sending_packets = utils.extract_outgoing_packets(flow.get_packets(), flow.get_dst_ip())
        sending_packets_timestamp = [float(packet.time) for packet in sending_packets]
        sending_packets_timestamp_sorted = sorted(sending_packets_timestamp)
        sending_packets_del_time = [pkt - pkt_prev for pkt_prev, pkt in
                           zip(sending_packets_timestamp_sorted[:-1], sending_packets_timestamp_sorted[1:])]
        return sending_packets_del_time


class ReceivingPacketsDeltaTimeMin(PacketsDeltaTimeBase):
    name = "receiving_packets_delta_time_min"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().ReceivingDelta(flow)
        return min(receiving_packets_del_time) if len(receiving_packets_del_time) > 0 else 0


class ReceivingPacketsDeltaTimeMax(PacketsDeltaTimeBase):
    name = "receiving_packets_delta_time_max"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().ReceivingDelta(flow)
        return max(receiving_packets_del_time) if len(receiving_packets_del_time) > 0 else 0


class ReceivingPacketsDeltaTimeMean(PacketsDeltaTimeBase):
    name = "receiving_packets_delta_time_mean"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().ReceivingDelta(flow)
        return statistics.mean(receiving_packets_del_time) if len(receiving_packets_del_time) > 0 else 0


class ReceivingPacketsDeltaTimeMode(PacketsDeltaTimeBase):
    name = "receiving_packets_delta_time_mode"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().ReceivingDelta(flow)
        return float(stats.mode(receiving_packets_del_time)[0]) if len(receiving_packets_del_time) > 0 else 0


class ReceivingPacketsDeltaTimeVariance(PacketsDeltaTimeBase):
    name = "receiving_packets_delta_time_variance"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().ReceivingDelta(flow)
        return statistics.pvariance(receiving_packets_del_time) if len(receiving_packets_del_time) > 0 else 0


class ReceivingPacketsDeltaTimeStandardDeviation(PacketsDeltaTimeBase):
    name = "receiving_packets_delta_time_standard_deviation"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().ReceivingDelta(flow)
        return statistics.pstdev(receiving_packets_del_time) if len(receiving_packets_del_time) > 0 else 0


class ReceivingPacketsDeltaTimeMedian(PacketsDeltaTimeBase):
    name = "receiving_packets_delta_time_median"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().ReceivingDelta(flow)
        return statistics.median(receiving_packets_del_time) if len(receiving_packets_del_time) > 0 else 0


class ReceivingPacketsDeltaTimeSkewness(PacketsDeltaTimeBase):
    name = "receiving_packets_delta_time_skewness"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().ReceivingDelta(flow)
        return stats.skew(receiving_packets_del_time) if len(receiving_packets_del_time) > 0 else 0


class ReceivingPacketsDeltaTimeCoefficientOfVariation(PacketsDeltaTimeBase):
    name = "receiving_packets_delta_time_coefficient_of_variation"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().ReceivingDelta(flow)
        return stats.variation(receiving_packets_del_time) if len(receiving_packets_del_time) > 0 else 0


class SendingPacketsDeltaTimeMin(PacketsDeltaTimeBase):
    name = "sending_packets_delta_time_min"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().SendingDelta(flow)
        return min(sending_packets_del_time) if len(sending_packets_del_time) > 0 else 0


class SendingPacketsDeltaTimeMax(PacketsDeltaTimeBase):
    name = "sending_packets_delta_time_max"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().SendingDelta(flow)
        return max(sending_packets_del_time) if len(sending_packets_del_time) > 0 else 0


class SendingPacketsDeltaTimeMean(PacketsDeltaTimeBase):
    name = "sending_packets_delta_time_mean"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().SendingDelta(flow)
        return statistics.mean(sending_packets_del_time) if len(sending_packets_del_time) > 0 else 0


class SendingPacketsDeltaTimeMode(PacketsDeltaTimeBase):
    name = "sending_packets_delta_time_mode"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().SendingDelta(flow)
        return float(stats.mode(sending_packets_del_time)[0]) if len(sending_packets_del_time) > 0 else 0


class SendingPacketsDeltaTimeVariance(PacketsDeltaTimeBase):
    name = "sending_packets_delta_time_variance"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().SendingDelta(flow)
        return statistics.pvariance(sending_packets_del_time) if len(sending_packets_del_time) > 0 else 0


class SendingPacketsDeltaTimeStandardDeviation(PacketsDeltaTimeBase):
    name = "sending_packets_delta_time_standard_deviation"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().SendingDelta(flow)
        return statistics.pstdev(sending_packets_del_time) if len(sending_packets_del_time) > 0 else 0


class SendingPacketsDeltaTimeMedian(PacketsDeltaTimeBase):
    name = "sending_packets_delta_time_median"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().SendingDelta(flow)
        return statistics.median(sending_packets_del_time) if len(sending_packets_del_time) > 0 else 0


class SendingPacketsDeltaTimeSkewness(PacketsDeltaTimeBase):
    name = "sending_packets_delta_time_skewness"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().SendingDelta(flow)
        return stats.skew(sending_packets_del_time) if len(sending_packets_del_time) > 0 else 0


class SendingPacketsDeltaTimeCoefficientOfVariation(PacketsDeltaTimeBase):
    name = "sending_packets_delta_time_coefficient_of_variation"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().SendingDelta(flow)
        return stats.variation(sending_packets_del_time) if len(sending_packets_del_time) > 0 else 0
