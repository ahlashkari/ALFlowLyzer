#!/usr/bin/env python3

import statistics
from enum import Enum
from scipy import stats
from .feature import Feature
from . import utils


class Duration(Feature):
    name = "duration"
    def extract(self, flow: object) -> float:
        return format(utils.calculate_duration(flow.get_packets()), self.floating_point_unit)


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


class HandshakingStates(Enum):
    Ideal = 0
    CLIENT_SENT_HANDSHAKE_REQUEST = 1
    SERVER_ACKNWOLEDGED_CLIENT_HANDSHAKE_REQUEST = 2
    END_OF_HANDSHAKING = 3


class Handshake(Feature):
    name = "delta_start"
    delta = None
    duration = None

    def extract_data_from_handshaking_process(self, flow: object):
        if flow.get_network_protocol() != "TCP":
            self.delta = "not a tcp connection"
            self.duration = "not a tcp connection"
            return

        packets = flow.get_packets()
        last_handshake_packet_time = 0
        first_handshake_packet_time = 0
        first_not_handshake_packet_time = 0
        STATE = HandshakingStates.Ideal
        seq_number = 0
        ack_number = 0
        for packet in packets:
            if STATE == HandshakingStates.END_OF_HANDSHAKING:
                if first_not_handshake_packet_time == 0:
                    first_not_handshake_packet_time = packet.get_timestamp()
                self.delta = format(first_not_handshake_packet_time - last_handshake_packet_time,
                        self.floating_point_unit)
                self.duration = format(last_handshake_packet_time - first_handshake_packet_time,
                        self.floating_point_unit)
                return

            if STATE == HandshakingStates.Ideal and packet.has_syn_flag():
                first_handshake_packet_time = packet.get_timestamp()
                seq_number = packet.get_seq_number()
                STATE = HandshakingStates.CLIENT_SENT_HANDSHAKE_REQUEST

            elif STATE == HandshakingStates.CLIENT_SENT_HANDSHAKE_REQUEST \
                    and packet.has_syn_flag() \
                    and packet.has_ack_flag() and seq_number == packet.get_ack_number() - 1:
                seq_number = packet.get_seq_number()
                ack_number = packet.get_ack_number()
                STATE = HandshakingStates.SERVER_ACKNWOLEDGED_CLIENT_HANDSHAKE_REQUEST

            elif STATE == HandshakingStates.SERVER_ACKNWOLEDGED_CLIENT_HANDSHAKE_REQUEST \
                    and packet.has_ack_flag() and seq_number == packet.get_ack_number() - 1 \
                    and ack_number == packet.get_seq_number():
                last_handshake_packet_time = packet.get_timestamp()
                STATE = HandshakingStates.END_OF_HANDSHAKING

            elif first_not_handshake_packet_time == 0:
                first_not_handshake_packet_time = packet.get_timestamp()

        self.delta = "not a complete handshake"
        self.duration = "not a complete handshake"

    def extract(self, flow: object) -> float:
        pass


class DeltaStart(Handshake):
    name = "delta_start"
    def extract(self, flow: object) -> float:
        self.extract_data_from_handshaking_process(flow)
        return self.delta


class HandshakeDuration(Handshake):
    name = "handshake_duration"
    def extract(self, flow: object) -> float:
        self.extract_data_from_handshaking_process(flow)
        return self.duration


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
