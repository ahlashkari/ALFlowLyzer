#!/usr/bin/env python3

from .features import *     # TODO: Imrove it


class FeatureExtractor(object):
    def __init__(self, flows: list):
        self.__flows = flows
        self.__features = [
                PacketsLenMin(),
                PacketsLenMax(),
                PacketsLenMean(),
                PacketsLenMedian(),
                PacketsLenStandardDeviation(),
                PacketsLenVariance(),
                PacketsLenMode(),
                PacketsLenCoefficientOfVariation(),
                PacketsLenSkewness(),
                PacketsDelLenMin(),
                PacketsDelLenMax(),
                PacketsDelLenMean(),
                PacketsDelLenMedian(),
                PacketsDelLenStandardDeviation(),
                PacketsDelLenVariance(),
                PacketsDelLenMode(),
                PacketsDelLenCoefficientOfVariation(),
                PacketsDelLenSkewness(),
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
            features_of_flow["src_ip"] = flow.get_src_ip()
            features_of_flow["dst_ip"] = flow.get_dst_ip()
            features_of_flow["src_port"] = flow.get_src_port()
            features_of_flow["dst_port"] = flow.get_dst_port()
            for feature in self.__features:
                features_of_flow[feature.name] = feature.extract(flow)
            self.__extracted_data.append(features_of_flow.copy())
        return self.__extracted_data.copy()
