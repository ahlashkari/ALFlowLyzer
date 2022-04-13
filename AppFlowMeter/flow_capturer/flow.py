#!/usr/bin/env python3


class Flow(object):
    def __init__(self):
        self.src_ip = ""
        self.dst_ip = ""
        self.src_port = ""
        self.dst_port = ""
        self.packets = list

    def add_packet(self, pcap_file: str) -> None:
        pass
