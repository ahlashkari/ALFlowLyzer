#!/usr/bin/env python3

from datetime import datetime
from .features import *     # TODO: Imrove it


class FeatureExtractor(object):
    def __init__(self, flows: list):
        self.__flows = flows
        self.__features = [
                PacketsLenMin(),
                PacketsLenMax(),
                PacketsLenMean(),
                PacketsLenMedian(),
                PacketsLenMode(),
                PacketsLenStandardDeviation(),
                PacketsLenVariance(),
                PacketsLenCoefficientOfVariation(),
                PacketsLenSkewness(),
                ReceivingPacketsDeltaLenMin(),
                ReceivingPacketsDeltaLenMax(),
                ReceivingPacketsDeltaLenMean(),
                ReceivingPacketsDeltaLenMedian(),
                ReceivingPacketsDeltaLenStandardDeviation(),
                ReceivingPacketsDeltaLenVariance(),
                ReceivingPacketsDeltaLenMode(),
                ReceivingPacketsDeltaLenCoefficientOfVariation(),
                ReceivingPacketsDeltaLenSkewness(),
                SendingPacketsDeltaLenMin(),
                SendingPacketsDeltaLenMax(),
                SendingPacketsDeltaLenMean(),
                SendingPacketsDeltaLenMedian(),
                SendingPacketsDeltaLenStandardDeviation(),
                SendingPacketsDeltaLenVariance(),
                SendingPacketsDeltaLenMode(),
                SendingPacketsDeltaLenCoefficientOfVariation(),
                SendingPacketsDeltaLenSkewness(),
                ReceivingPacketsDeltaTimeMax(),
                ReceivingPacketsDeltaTimeMean(),
                ReceivingPacketsDeltaTimeMedian(),
                ReceivingPacketsDeltaTimeStandardDeviation(),
                ReceivingPacketsDeltaTimeVariance(),
                ReceivingPacketsDeltaTimeMode(),
                ReceivingPacketsDeltaTimeCoefficientOfVariation(),
                ReceivingPacketsDeltaTimeSkewness(),
                SendingPacketsDeltaTimeMin(),
                SendingPacketsDeltaTimeMax(),
                SendingPacketsDeltaTimeMean(),
                SendingPacketsDeltaTimeMedian(),
                SendingPacketsDeltaTimeStandardDeviation(),
                SendingPacketsDeltaTimeVariance(),
                SendingPacketsDeltaTimeMode(),
                SendingPacketsDeltaTimeCoefficientOfVariation(),
                SendingPacketsDeltaTimeSkewness(),
                PacketsNumbers(),
                IncomingPacketsNumbers(),
                OutgoingPacketsNumbers(),
                ConnectionTime(),
                PacketsRate(),
                IncomingPacketsRate(),
                OutgoingPacketsRate(),
            ]

    def execute(self) -> list:
        self.__extracted_data = []
        for flow in self.__flows:
            features_of_flow = {}
            features_of_flow["timestamp"] = datetime.fromtimestamp(flow.get_timestamp())
            features_of_flow["src_ip"] = flow.get_src_ip()
            features_of_flow["src_port"] = flow.get_src_port()
            features_of_flow["dst_ip"] = flow.get_dst_ip()
            features_of_flow["dst_port"] = flow.get_dst_port()
            features_of_flow["protocol"] = flow.get_protocol()
            for feature in self.__features:
                features_of_flow[feature.name] = feature.extract(flow)
            self.__extracted_data.append(features_of_flow.copy())
        return self.__extracted_data.copy()
