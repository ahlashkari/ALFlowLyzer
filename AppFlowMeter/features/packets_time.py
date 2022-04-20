#!/usr/bin/env python3

import statistics
from scipy import stats
from .feature import Feature


class ConnectionTime(Feature):
    name = "connection_time"
    def extract(self, flow: object) -> float:
        packets_time = [packet.time for packet in flow.get_packets()]
        return max(packets_time) - min(packets_time)
