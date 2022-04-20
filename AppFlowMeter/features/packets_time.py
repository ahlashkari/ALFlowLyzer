#!/usr/bin/env python3

import statistics
from scipy import stats
from .feature import Feature
from . import utils


class ConnectionTime(Feature):
    name = "connection_time"
    def extract(self, flow: object) -> float:
        return utils.calculate_duration(flow.get_packets())
