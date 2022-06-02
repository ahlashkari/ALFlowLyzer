#!/usr/bin/env python3

import statistics
from scipy import stats
from .feature import Feature
from . import utils


class Duration(Feature):
    name = "duration"
    def extract(self, flow: object) -> float:
        return format(utils.calculate_duration(flow.get_packets()), self.floating_point_unit)


class DeltaStart(Feature):
    name = "delta_start"
    def extract(self, flow: object) -> float:
        packets = flow.get_packets()
        start_handshake_time = []
        first_http_req_time = []
        for packet in packets:
            if (packet.get_dst_port() == 80) & (packet.get_syn_flag() == 1):
                start_handshake_time.append(packet.get_timestamp())
            if packet.get_req_status(): 
                first_http_req_time.append(packet.get_timestamp())
        if len(start_handshake_time) > 0 and len(first_http_req_time) > 0:
            return format(min(first_http_req_time) - min(start_handshake_time), self.floating_point_unit)
        return None


class PacketsDeltaTimeBase(Feature):
    def get_receiving_delta(self, flow: object) -> list:
        receiving_packets = utils.extract_receiving_packets(flow.get_packets(), flow.get_dst_ip())
        receiving_packets_timestamp = [float(packet.get_timestamp()) for packet in receiving_packets]
        receiving_packets_timestamp_sorted = sorted(receiving_packets_timestamp)
        receiving_packets_del_time = [pkt - pkt_prev for pkt_prev, pkt in
                           zip(receiving_packets_timestamp_sorted[:-1], receiving_packets_timestamp_sorted[1:])]
        return receiving_packets_del_time

    def get_sending_delta(self, flow: object) -> list:
        sending_packets = utils.extract_sending_packets(flow.get_packets(), flow.get_dst_ip())
        sending_packets_timestamp = [float(packet.get_timestamp()) for packet in sending_packets]
        sending_packets_timestamp_sorted = sorted(sending_packets_timestamp)
        sending_packets_del_time = [pkt - pkt_prev for pkt_prev, pkt in
                           zip(sending_packets_timestamp_sorted[:-1], sending_packets_timestamp_sorted[1:])]
        return sending_packets_del_time


class ReceivingPacketsDeltaTimeMin(PacketsDeltaTimeBase):
    name = "min_receiving_packets_delta_time"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().get_receiving_delta(flow)
        if len(receiving_packets_del_time) > 0:
            return format(min(receiving_packets_del_time), self.floating_point_unit)
        return 0


class ReceivingPacketsDeltaTimeMax(PacketsDeltaTimeBase):
    name = "max_receiving_packets_delta_time"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().get_receiving_delta(flow)
        if len(receiving_packets_del_time) > 0:
            return format(max(receiving_packets_del_time), self.floating_point_unit)
        return 0


class ReceivingPacketsDeltaTimeMean(PacketsDeltaTimeBase):
    name = "mean_receiving_packets_delta_time"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().get_receiving_delta(flow)
        if len(receiving_packets_del_time) > 0:
            return format(statistics.mean(receiving_packets_del_time), self.floating_point_unit)
        return 0


class ReceivingPacketsDeltaTimeMode(PacketsDeltaTimeBase):
    name = "mode_receiving_packets_delta_time"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().get_receiving_delta(flow)
        if len(receiving_packets_del_time) > 0:
            return format(float(stats.mode(receiving_packets_del_time)[0]), self.floating_point_unit)
        return 0


class ReceivingPacketsDeltaTimeVariance(PacketsDeltaTimeBase):
    name = "variance_receiving_packets_delta_time"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().get_receiving_delta(flow)
        if len(receiving_packets_del_time) > 0:
            return format(statistics.pvariance(receiving_packets_del_time), self.floating_point_unit)
        return 0


class ReceivingPacketsDeltaTimeStandardDeviation(PacketsDeltaTimeBase):
    name = "standard_deviation_receiving_packets_delta_time"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().get_receiving_delta(flow)
        if len(receiving_packets_del_time) > 0:
            return format(statistics.pstdev(receiving_packets_del_time), self.floating_point_unit)
        return 0


class ReceivingPacketsDeltaTimeMedian(PacketsDeltaTimeBase):
    name = "median_receiving_packets_delta_time"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().get_receiving_delta(flow)
        if len(receiving_packets_del_time) > 0:
            return format(statistics.median(receiving_packets_del_time), self.floating_point_unit)
        return 0


class ReceivingPacketsDeltaTimeSkewness(PacketsDeltaTimeBase):
    name = "skewness_sreceiving_packets_delta_time"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().get_receiving_delta(flow)
        if len(receiving_packets_del_time) > 0:
            return format(float(stats.skew(receiving_packets_del_time)), self.floating_point_unit)
        return 0


class ReceivingPacketsDeltaTimeCoefficientOfVariation(PacketsDeltaTimeBase):
    name = "coefficient_of_variation_receiving_packets_delta_time"
    def extract(self, flow: object) -> float:
        receiving_packets_del_time = super().get_receiving_delta(flow)
        if len(receiving_packets_del_time) > 0:
            return format(stats.variation(receiving_packets_del_time), self.floating_point_unit)
        return 0


class SendingPacketsDeltaTimeMin(PacketsDeltaTimeBase):
    name = "min_sending_packets_delta_time"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().get_sending_delta(flow)
        if len(sending_packets_del_time) > 0:
            return format(min(sending_packets_del_time), self.floating_point_unit)
        return 0


class SendingPacketsDeltaTimeMax(PacketsDeltaTimeBase):
    name = "max_sending_packets_delta_time"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().get_sending_delta(flow)
        if len(sending_packets_del_time) > 0:
            return format(max(sending_packets_del_time), self.floating_point_unit)
        return 0


class SendingPacketsDeltaTimeMean(PacketsDeltaTimeBase):
    name = "mean_sending_packets_delta_time"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().get_sending_delta(flow)
        if len(sending_packets_del_time) > 0:
            return format(statistics.mean(sending_packets_del_time), self.floating_point_unit)
        return 0


class SendingPacketsDeltaTimeMode(PacketsDeltaTimeBase):
    name = "mode_sending_packets_delta_time"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().get_sending_delta(flow)
        if len(sending_packets_del_time) > 0:
            return format(float(stats.mode(sending_packets_del_time)[0]), self.floating_point_unit)
        return 0


class SendingPacketsDeltaTimeVariance(PacketsDeltaTimeBase):
    name = "variance_sending_packets_delta_time"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().get_sending_delta(flow)
        if len(sending_packets_del_time) > 0:
            return format(statistics.pvariance(sending_packets_del_time), self.floating_point_unit)
        return 0


class SendingPacketsDeltaTimeStandardDeviation(PacketsDeltaTimeBase):
    name = "standard_deviation_sending_packets_delta_time"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().get_sending_delta(flow)
        if len(sending_packets_del_time) > 0:
            return format(statistics.pstdev(sending_packets_del_time), self.floating_point_unit)
        return 0


class SendingPacketsDeltaTimeMedian(PacketsDeltaTimeBase):
    name = "median_sending_packets_delta_time"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().get_sending_delta(flow)
        if len(sending_packets_del_time) > 0:
            return format(statistics.median(sending_packets_del_time), self.floating_point_unit)
        return 0


class SendingPacketsDeltaTimeSkewness(PacketsDeltaTimeBase):
    name = "skewness_sending_packets_delta_time"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().get_sending_delta(flow)
        if len(sending_packets_del_time) > 0:
            return format(float(stats.skew(sending_packets_del_time)), self.floating_point_unit)
        return 0


class SendingPacketsDeltaTimeCoefficientOfVariation(PacketsDeltaTimeBase):
    name = "coefficient_of_variation_sending_packets_delta_time"
    def extract(self, flow: object) -> float:
        sending_packets_del_time = super().get_sending_delta(flow)
        if len(sending_packets_del_time) > 0:
            return format(stats.variation(sending_packets_del_time), self.floating_point_unit)
        return 0
