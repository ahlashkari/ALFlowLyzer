#!/usr/bin/env python3

import statistics
from scipy import stats
from .feature import Feature
from . import utils


class TotalBytes(Feature):
    name = "total_bytes"
    def extract(self, flow: object) -> int:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return sum(packets_len)


class SendingBytes(Feature):
    name = "sending_bytes"
    def extract(self, flow: object) -> int:
        sending_packets = utils.extract_sending_packets(flow.get_packets(), flow.get_dst_ip())
        sending_packets_len = [len(packet) for packet in sending_packets]
        return sum(sending_packets_len)


class ReceivingBytes(Feature):
    name = "receiving_bytes"
    def extract(self, flow: object) -> int:
        receiving_packets = utils.extract_receiving_packets(flow.get_packets(), flow.get_dst_ip())
        receiving_packets_len = [len(packet) for packet in receiving_packets]
        return sum(receiving_packets_len)


class PacketsLenMin(Feature):
    name = "min_packets_len"
    def extract(self, flow: object) -> int:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return min(packets_len)


class PacketsLenMax(Feature):
    name = "max_packets_len"
    def extract(self, flow: object) -> int:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return max(packets_len)


class PacketsLenMean(Feature):
    name = "mean_packets_len"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return format(statistics.mean(packets_len), self.floating_point_unit)


class PacketsLenMode(Feature):
    name = "mode_packets_len"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return format(float(stats.mode(packets_len)[0]), self.floating_point_unit)


class PacketsLenVariance(Feature):
    name = "variance_packets_len"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return format(statistics.pvariance(packets_len), self.floating_point_unit)


class PacketsLenStandardDeviation(Feature):
    name = "standard_deviation_packets_len"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return format(statistics.pstdev(packets_len), self.floating_point_unit)


class PacketsLenMedian(Feature):
    name = "median_packets_len"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return format(statistics.median(packets_len), self.floating_point_unit)


class PacketsLenSkewness(Feature):
    name = "skewness_packets_len"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return format(stats.skew(packets_len), self.floating_point_unit)


class PacketsLenCoefficientOfVariation(Feature):
    name = "coefficient_of_variation_packets_len"
    def extract(self, flow: object) -> float:
        packets_len = [len(packet) for packet in flow.get_packets()]
        return format(stats.variation(packets_len), self.floating_point_unit)


class SendingPacketsLenMin(Feature):
    name = "min_sending_packets_len"
    def extract(self, flow: object) -> int:
        sending_packets_len = [len(packet) for packet in utils.extract_sending_packets(flow.get_packets(),
                flow.get_dst_ip())]
        return min(sending_packets_len) if len(sending_packets_len) > 0 else 0


class SendingPacketsLenMax(Feature):
    name = "max_sending_packets_len"
    def extract(self, flow: object) -> int:
        sending_packets_len = [len(packet) for packet in utils.extract_sending_packets(flow.get_packets(),
                flow.get_dst_ip())]
        return max(sending_packets_len) if len(sending_packets_len) > 0 else 0


class SendingPacketsLenMean(Feature):
    name = "mean_sending_packets_len"
    def extract(self, flow: object) -> float:
        sending_packets_len = [len(packet) for packet in utils.extract_sending_packets(flow.get_packets(),
                flow.get_dst_ip())]
        if len(sending_packets_len) > 0:
            return format(statistics.mean(sending_packets_len), self.floating_point_unit)
        return 0


class SendingPacketsLenMode(Feature):
    name = "mode_sending_packets_len"
    def extract(self, flow: object) -> float:
        sending_packets_len = [len(packet) for packet in utils.extract_sending_packets(flow.get_packets(),
                flow.get_dst_ip())]
        if len(sending_packets_len) > 0:
            return format(float(stats.mode(sending_packets_len)[0]), self.floating_point_unit)
        return 0


class SendingPacketsLenVariance(Feature):
    name = "variance_sending_packets_len"
    def extract(self, flow: object) -> float:
        sending_packets_len = [len(packet) for packet in utils.extract_sending_packets(flow.get_packets(),
                flow.get_dst_ip())]
        if len(sending_packets_len) > 0:
            return format(statistics.pvariance(sending_packets_len), self.floating_point_unit)
        return 0


class SendingPacketsLenStandardDeviation(Feature):
    name = "standard_deviation_sending_packets_len"
    def extract(self, flow: object) -> float:
        sending_packets_len = [len(packet) for packet in utils.extract_sending_packets(flow.get_packets(),
                flow.get_dst_ip())]
        if len(sending_packets_len) > 0:
            return format(statistics.pstdev(sending_packets_len), self.floating_point_unit)
        return 0


class SendingPacketsLenMedian(Feature):
    name = "median_sending_packets_len"
    def extract(self, flow: object) -> float:
        sending_packets_len = [len(packet) for packet in utils.extract_sending_packets(flow.get_packets(),
                flow.get_dst_ip())]
        if len(sending_packets_len) > 0:
            return format(statistics.median(sending_packets_len), self.floating_point_unit)
        return 0


class SendingPacketsLenSkewness(Feature):
    name = "skewness_sending_packets_len"
    def extract(self, flow: object) -> float:
        sending_packets_len = [len(packet) for packet in utils.extract_sending_packets(flow.get_packets(),
                flow.get_dst_ip())]
        if len(sending_packets_len) > 0:
            return format(stats.skew(sending_packets_len), self.floating_point_unit)
        return 0


class SendingPacketsLenCoefficientOfVariation(Feature):
    name = "coefficient_of_variation_sending_packets_len"
    def extract(self, flow: object) -> float:
        sending_packets_len = [len(packet) for packet in utils.extract_sending_packets(flow.get_packets(),
                flow.get_dst_ip())]
        if len(sending_packets_len) > 0:
            return format(stats.variation(sending_packets_len), self.floating_point_unit)
        return 0


class ReceivingPacketsLenMin(Feature):
    name = "min_receiving_packets_len"
    def extract(self, flow: object) -> int:
        receiving_packets_len = [len(packet) for packet in utils.extract_receiving_packets(flow.get_packets(),
                flow.get_dst_ip())]
        return min(receiving_packets_len) if len(receiving_packets_len) > 0 else 0


class ReceivingPacketsLenMax(Feature):
    name = "max_receiving_packets_len"
    def extract(self, flow: object) -> int:
        receiving_packets_len = [len(packet) for packet in utils.extract_receiving_packets(flow.get_packets(),
                flow.get_dst_ip())]
        return max(receiving_packets_len) if len(receiving_packets_len) > 0 else 0


class ReceivingPacketsLenMean(Feature):
    name = "mean_receiving_packets_len"
    def extract(self, flow: object) -> float:
        receiving_packets_len = [len(packet) for packet in utils.extract_receiving_packets(flow.get_packets(),
                flow.get_dst_ip())]
        if len(receiving_packets_len) > 0:
            return format(statistics.mean(receiving_packets_len), self.floating_point_unit)
        return 0


class ReceivingPacketsLenMode(Feature):
    name = "mode_receiving_packets_len"
    def extract(self, flow: object) -> float:
        receiving_packets_len = [len(packet) for packet in utils.extract_receiving_packets(flow.get_packets(),
                flow.get_dst_ip())]
        if len(receiving_packets_len) > 0:
            return format(float(stats.mode(receiving_packets_len)[0]), self.floating_point_unit)
        return 0


class ReceivingPacketsLenVariance(Feature):
    name = "variance_receiving_packets_len"
    def extract(self, flow: object) -> float:
        receiving_packets_len = [len(packet) for packet in utils.extract_receiving_packets(flow.get_packets(),
                flow.get_dst_ip())]
        if len(receiving_packets_len) > 0:
            return format(statistics.pvariance(receiving_packets_len), self.floating_point_unit)
        return 0


class ReceivingPacketsLenStandardDeviation(Feature):
    name = "standard_deviation_receiving_packets_len"
    def extract(self, flow: object) -> float:
        receiving_packets_len = [len(packet) for packet in utils.extract_receiving_packets(flow.get_packets(),
                flow.get_dst_ip())]
        if len(receiving_packets_len) > 0:
            return format(statistics.pstdev(receiving_packets_len), self.floating_point_unit)
        return 0


class ReceivingPacketsLenMedian(Feature):
    name = "median_receiving_packets_len"
    def extract(self, flow: object) -> float:
        receiving_packets_len = [len(packet) for packet in utils.extract_receiving_packets(flow.get_packets(),
                flow.get_dst_ip())]
        if len(receiving_packets_len) > 0:
            return format(statistics.median(receiving_packets_len), self.floating_point_unit)
        return 0


class ReceivingPacketsLenSkewness(Feature):
    name = "skewness_receiving_packets_len"
    def extract(self, flow: object) -> float:
        receiving_packets_len = [len(packet) for packet in utils.extract_receiving_packets(flow.get_packets(),
                flow.get_dst_ip())]
        if len(receiving_packets_len) > 0:
            return format(stats.skew(receiving_packets_len), self.floating_point_unit)
        return 0


class ReceivingPacketsLenCoefficientOfVariation(Feature):
    name = "coefficient_of_variation_receiving_packets_len"
    def extract(self, flow: object) -> float:
        receiving_packets_len = [len(packet) for packet in utils.extract_receiving_packets(flow.get_packets(),
                flow.get_dst_ip())]
        if len(receiving_packets_len) > 0:
            return format(stats.variation(receiving_packets_len), self.floating_point_unit)
        return 0


class PacketsDeltaLenBase(Feature):
    def get_receiving_delta(self, flow: object) -> list:
        receiving_packets = utils.extract_receiving_packets(flow.get_packets(), flow.get_dst_ip())
        receiving_packets_timestamp = [packet.get_timestamp() for packet in receiving_packets]
        receiving_packets_sorted = [packet for _, packet in sorted(zip(receiving_packets_timestamp,
                                                                       receiving_packets))]
        receiving_packets_len = [len(packet) for packet in receiving_packets_sorted]
        receiving_packets_del_len = [pkt - pkt_prev for pkt_prev, pkt in
                           zip(receiving_packets_len[:-1], receiving_packets_len[1:])]
        return receiving_packets_del_len

    def get_sending_delta(self, flow: object) -> list:
        sending_packets = utils.extract_sending_packets(flow.get_packets(), flow.get_dst_ip())
        sending_packets_timestamp = [packet.get_timestamp() for packet in sending_packets]
        sending_packets_sorted = [packet for _, packet in sorted(zip(sending_packets_timestamp,
                                                                       sending_packets))]
        sending_packets_len = [len(packet) for packet in sending_packets_sorted]
        sending_packets_del_len = [pkt - pkt_prev for pkt_prev, pkt in
                           zip(sending_packets_len[:-1], sending_packets_len[1:])]
        return sending_packets_del_len


class ReceivingPacketsDeltaLenMin(PacketsDeltaLenBase):
    name = "min_receiving_packets_delta_len"
    def extract(self, flow: object) -> int:
        receiving_packets_del_len = super().get_receiving_delta(flow)
        return min(receiving_packets_del_len) if len(receiving_packets_del_len) > 0 else 0


class ReceivingPacketsDeltaLenMax(PacketsDeltaLenBase):
    name = "max_receiving_packets_delta_len"
    def extract(self, flow: object) -> int:
        receiving_packets_del_len = super().get_receiving_delta(flow)
        return max(receiving_packets_del_len) if len(receiving_packets_del_len) > 0 else 0


class ReceivingPacketsDeltaLenMean(PacketsDeltaLenBase):
    name = "mean_receiving_packets_delta_len"
    def extract(self, flow: object) -> float:
        receiving_packets_del_len = super().get_receiving_delta(flow)
        if len(receiving_packets_del_len) > 0:
            return format(statistics.mean(receiving_packets_del_len), self.floating_point_unit)
        return 0


class ReceivingPacketsDeltaLenMode(PacketsDeltaLenBase):
    name = "mode_receiving_packets_delta_len"
    def extract(self, flow: object) -> float:
        receiving_packets_del_len = super().get_receiving_delta(flow)
        if len(receiving_packets_del_len) > 0:
            return format(float(stats.mode(receiving_packets_del_len)[0]), self.floating_point_unit)
        return 0


class ReceivingPacketsDeltaLenVariance(PacketsDeltaLenBase):
    name = "variance_receiving_packets_delta_len"
    def extract(self, flow: object) -> float:
        receiving_packets_del_len = super().get_receiving_delta(flow)
        if len(receiving_packets_del_len) > 0:
            return format(statistics.pvariance(receiving_packets_del_len), self.floating_point_unit)
        return 0


class ReceivingPacketsDeltaLenStandardDeviation(PacketsDeltaLenBase):
    name = "standard_deviation_receiving_packets_delta_len"
    def extract(self, flow: object) -> float:
        receiving_packets_del_len = super().get_receiving_delta(flow)
        if len(receiving_packets_del_len) > 0:
            return format(statistics.pstdev(receiving_packets_del_len), self.floating_point_unit)
        return 0


class ReceivingPacketsDeltaLenMedian(PacketsDeltaLenBase):
    name = "median_receiving_packets_delta_len"
    def extract(self, flow: object) -> float:
        receiving_packets_del_len = super().get_receiving_delta(flow)
        if len(receiving_packets_del_len) > 0:
            return format(statistics.median(receiving_packets_del_len), self.floating_point_unit)
        return 0


class ReceivingPacketsDeltaLenSkewness(PacketsDeltaLenBase):
    name = "skewness_receiving_packets_delta_len"
    def extract(self, flow: object) -> float:
        receiving_packets_del_len = super().get_receiving_delta(flow)
        if len(receiving_packets_del_len) > 0:
            return format(float(stats.skew(receiving_packets_del_len)), self.floating_point_unit)
        return 0


class ReceivingPacketsDeltaLenCoefficientOfVariation(PacketsDeltaLenBase):
    name = "coefficient_of_variation_receiving_packets_delta_len"
    def extract(self, flow: object) -> float:
        receiving_packets_del_len = super().get_receiving_delta(flow)
        if len(receiving_packets_del_len) > 0:
            return format(stats.variation(receiving_packets_del_len), self.floating_point_unit)
        return 0


class SendingPacketsDeltaLenMin(PacketsDeltaLenBase):
    name = "min_sending_packets_delta_len"
    def extract(self, flow: object) -> int:
        sending_packets_del_len = super().get_sending_delta(flow)
        return min(sending_packets_del_len) if len(sending_packets_del_len) > 0 else 0


class SendingPacketsDeltaLenMax(PacketsDeltaLenBase):
    name = "max_sending_packets_delta_len"
    def extract(self, flow: object) -> int:
        sending_packets_del_len = super().get_sending_delta(flow)
        return max(sending_packets_del_len) if len(sending_packets_del_len) > 0 else 0


class SendingPacketsDeltaLenMean(PacketsDeltaLenBase):
    name = "mean_sending_packets_delta_len"
    def extract(self, flow: object) -> float:
        sending_packets_del_len = super().get_sending_delta(flow)
        if len(sending_packets_del_len) > 0:
            return format(statistics.mean(sending_packets_del_len), self.floating_point_unit)
        return 0


class SendingPacketsDeltaLenMode(PacketsDeltaLenBase):
    name = "mode_sending_packets_delta_len"
    def extract(self, flow: object) -> float:
        sending_packets_del_len = super().get_sending_delta(flow)
        if len(sending_packets_del_len) > 0:
            return format(float(stats.mode(sending_packets_del_len)[0]), self.floating_point_unit)
        return 0


class SendingPacketsDeltaLenVariance(PacketsDeltaLenBase):
    name = "variance_sending_packets_delta_len"
    def extract(self, flow: object) -> float:
        sending_packets_del_len = super().get_sending_delta(flow)
        if len(sending_packets_del_len) > 0:
            return format(statistics.pvariance(sending_packets_del_len), self.floating_point_unit)
        return 0


class SendingPacketsDeltaLenStandardDeviation(PacketsDeltaLenBase):
    name = "standard_deviation_sending_packets_delta_len"
    def extract(self, flow: object) -> float:
        sending_packets_del_len = super().get_sending_delta(flow)
        if len(sending_packets_del_len) > 0:
            return format(statistics.pstdev(sending_packets_del_len), self.floating_point_unit)
        return 0


class SendingPacketsDeltaLenMedian(PacketsDeltaLenBase):
    name = "median_sending_packets_delta_len"
    def extract(self, flow: object) -> float:
        sending_packets_del_len = super().get_sending_delta(flow)
        if len(sending_packets_del_len) > 0:
            return format(statistics.median(sending_packets_del_len), self.floating_point_unit)
        return 0


class SendingPacketsDeltaLenSkewness(PacketsDeltaLenBase):
    name = "skewness_sending_packets_delta_len"
    def extract(self, flow: object) -> float:
        sending_packets_del_len = super().get_sending_delta(flow)
        if len(sending_packets_del_len) > 0:
            return format(float(stats.skew(sending_packets_del_len)), self.floating_point_unit)
        return 0


class SendingPacketsDeltaLenCoefficientOfVariation(PacketsDeltaLenBase):
    name = "coefficient_of_variation_sending_packets_delta_len"
    def extract(self, flow: object) -> float:
        sending_packets_del_len = super().get_sending_delta(flow)
        if len(sending_packets_del_len) > 0:
            return format(stats.variation(sending_packets_del_len), self.floating_point_unit)
        return 0
