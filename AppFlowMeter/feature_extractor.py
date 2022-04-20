#!/usr/bin/env python3

from .app_flow_capturer import Flow
from .features import *     # TODO: Imrove it


class FeatureExtractor(object):
    def __init__(self, flows: Flow):
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
                PacketsNumbers()
            ]

    def execute(self) -> dict:
        self.__extracted_data = {"description": "application layer feature extractor"}
        for feature in self.__features:
            self.__extracted_data.update(feature.extract(self.__flows))
        return self.__extracted_data.copy()
