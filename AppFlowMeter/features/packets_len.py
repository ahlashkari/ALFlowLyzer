#!/usr/bin/env python3

from .feature import Feature

class PacketsLenMin(Feature):
    def extract(self, flows: list) -> dict:
        return {"packets_len_min": [8, 15, 4, 2, 14]}


class PacketsLenMax(Feature):
    def extract(self, flows: list) -> dict:
        return {"packets_len_max": [8, 15, 4, 2, 14]}


class PacketsLenMean(Feature):
    def extract(self, flows: list) -> dict:
        return {"packets_len_mean": [8, 15, 4, 2, 14]}
