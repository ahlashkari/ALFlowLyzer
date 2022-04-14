#!/usr/bin/env python3

from .feature import Feature

class PacketsLenMin(Feature):
    def extract(self, flows: list) -> dict:
        return {}


class PacketsLenMax(Feature):
    def extract(self, flows: list) -> dict:
        return {}


class PacketsLenMean(Feature):
    def extract(self, flows: list) -> dict:
        return {}
