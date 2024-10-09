#!/usr/bin/env python3

import warnings
from datetime import datetime
from multiprocessing import Lock
from .features import *


class FeatureExtractor(object):
    def __init__(self, floating_point_unit: str):
        warnings.filterwarnings("ignore")
        self.floating_point_unit = floating_point_unit
        self.__features = [
                Duration(),
                PacketsNumbers(),
                ReceivingPacketsNumbers(),
                SendingPacketsNumbers(),
                HandshakeDuration(),
                DeltaStart(),
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
                ConvFreqVowelsConsonants(),
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
                AvgAuthorityResourceRecords(),
                AvgAdditionalResourceRecords(),
                AvgAnswerResourceRecords(),
                QueryResourceRecordType(),
                AnsResourceRecordType(),
                QueryResourceRecordClass(),
                AnsResourceRecordClass(),
            ]
        self.__features = self.__features + self.__dns_features

    def execute(self, data: list, data_lock, flows: list, features_ignore_list: list = [],
            label: str = "") -> list:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            extracted_data = []
            for flow in flows:
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
                    try:
                        features_of_flow[feature.name] = feature.extract(flow)
                    except Exception as e:
                        print(f">> Error occurred in feature extraction for extracting >> {feature.name} << for the flow with {str(flow)} id.\n{e}\n")
                        pass
                features_of_flow["label"] = label
                extracted_data.append(features_of_flow)
            with data_lock:
                data.extend(extracted_data)
                del extracted_data