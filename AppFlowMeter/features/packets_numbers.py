#!/usr/bin/env python3

from .feature import Feature

class PacketsNumbers(Feature):
    def extract(self, flows: list) -> dict:
        return {"packets_numbers": [8, 15, 4, 2, 14]}
