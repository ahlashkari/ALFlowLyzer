#!/usr/bin/env python3

import scapy
from multipledispatch import dispatch
from .flow import Flow

class FlowCapturer(object):
    @dispatch()
    def capture(self) -> dict:
        pass

    @dispatch(str)
    def capture(self, pcap_file: str) -> dict:
        pass
