#!/usr/bin/env python3

from datetime import datetime
from .features import *


class FeatureExtractor(object):
    def __init__(self, flows: list, floating_point_unit: str):
        self.__flows = flows
        self.floating_point_unit = floating_point_unit
        self.__features = [
                Duration(),
                PacketsNumbers(),
                ReceivingPacketsNumbers(),
                SendingPacketsNumbers(),
                HandshakeDuration(),
                DeltaStart(),
                SuccessfulPacketsNumbers(),
                SuccessfulPacketsRate(),
                TotalBytes(),
                ReceivingBytes(),
                SendingBytes(),
                PacketsRate(),
                ReceivingPacketsRate(),
                SendingPacketsRate(),
                PacketsLenRate(),
                ReceivingPacketsLenRate(),
                SendingPacketsLenRate(),
                PacketsLenMin(),
                PacketsLenMax(),
                PacketsLenMean(),
                PacketsLenMedian(),
                PacketsLenMode(),
                PacketsLenStandardDeviation(),
                PacketsLenVariance(),
                PacketsLenCoefficientOfVariation(),
                PacketsLenSkewness(),
                ReceivingPacketsLenMin(),
                ReceivingPacketsLenMax(),
                ReceivingPacketsLenMean(),
                ReceivingPacketsLenMedian(),
                ReceivingPacketsLenMode(),
                ReceivingPacketsLenStandardDeviation(),
                ReceivingPacketsLenVariance(),
                ReceivingPacketsLenCoefficientOfVariation(),
                ReceivingPacketsLenSkewness(),
                SendingPacketsLenMin(),
                SendingPacketsLenMax(),
                SendingPacketsLenMean(),
                SendingPacketsLenMedian(),
                SendingPacketsLenMode(),
                SendingPacketsLenStandardDeviation(),
                SendingPacketsLenVariance(),
                SendingPacketsLenCoefficientOfVariation(),
                SendingPacketsLenSkewness(),
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
            ]

        self.__dns_features = [
                DomainName(),
                WhoisDomainName(),
                TopLevelDomain(),
                SecondLevelDomain(),
                DomainNameLen(),
                SubDomainNameLen(),
                UniGramDomainName(),
                BiGramDomainName(),
                TriGramDomainName(),
                NumericalPercentage(),
                CharacterDistribution(),
                DomainEmail(),
                DomainRegistrar(),
                DomainCreationDate(),
                DomainExpirationDate(),
                DomainAge(),
                DomainCountry(),
                DomainDNSSEC(),
                DomainOrganization(),
                DomainAddress(),
                DomainCity(),
                DomainState(),
                DomainZipcode(),
                DomainNameServers(),
                DomainUpdatedDate(),
                CharacterEntropy(),
                ContinuousNumericMaxLen(),
                ContinuousAlphabetMaxLen(),
                ContinuousConsonantsMaxLen(),
                ContinuousSameAlphabetMaxLen(),
                VowelsConsonantRatio(),
                DistinctTTLValues(),
                TTLValuesMin(),
                TTLValuesMax(),
                TTLValuesMean(),
                TTLValuesMode(),
                TTLValuesVariance(),
                TTLValuesStandardDeviation(),
                TTLValuesMedian(),
                TTLValuesSkewness(),
                TTLValuesCoefficientOfVariation(),
                DistinctARecords(),
                DistinctNSRecords(),
            ]

    def execute(self, features_ignore_list: list = []) -> list:
        self.__extracted_data = []
        self.__features = self.__features + self.__dns_features
        for flow in self.__flows:
            features_of_flow = {}
            features_of_flow["flow_id"] = str(flow)
            features_of_flow["timestamp"] = datetime.fromtimestamp(flow.get_timestamp())
            features_of_flow["src_ip"] = flow.get_src_ip()
            features_of_flow["src_port"] = flow.get_src_port()
            features_of_flow["dst_ip"] = flow.get_dst_ip()
            features_of_flow["dst_port"] = flow.get_dst_port()
            features_of_flow["protocol"] = flow.get_protocol()
            for feature in self.__features:
                if feature.name in features_ignore_list:
                    continue
                feature.set_floating_point_unit(self.floating_point_unit)
                features_of_flow[feature.name] = feature.extract(flow)
            self.__extracted_data.append(features_of_flow.copy())
        return self.__extracted_data.copy()
