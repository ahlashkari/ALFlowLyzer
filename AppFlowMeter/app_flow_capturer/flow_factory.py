#!/usr/bin/env python3

from .flow import Flow, DNSFlow


class FlowFactory(object):
    def create(self, packet) -> Flow:
        src_ip = packet.get_src_ip()
        dst_ip = packet.get_dst_ip()
        src_port = packet.get_src_port()
        dst_port = packet.get_dst_port()
        transaction_id = packet.get_transaction_id()
        timestamp = packet.get_timestamp()
        application_protocol = packet.get_application_protocol()
        network_protocol = packet.get_network_protocol()

        if "DNS" == application_protocol:
            new_flow = DNSFlow(src_ip, dst_ip, src_port, dst_port, timestamp, application_protocol,
                    network_protocol, transaction_id)
        else:
            new_flow = Flow(src_ip, dst_ip, src_port, dst_port, timestamp, application_protocol,
                    network_protocol)

        new_flow.add_packet(packet)
        return new_flow

