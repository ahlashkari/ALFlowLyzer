#!/usr/bin/env python3

from .feature import Feature


class DomainName(Feature):
    name = "domain_name"
    def extract(self, flow: object) -> str:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        return flow.get_domain_names()[0]


class TopLevelDomain(Feature):
    name = "top_level_domain"
    def extract(self, flow: object) -> str:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        return "." + flow.get_domain_names()[0].split(".")[-2]


class SecondLevelDomain(Feature):
    name = "second_level_domain"
    def extract(self, flow: object) -> str:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        return "." + flow.get_domain_names()[0].split(".")[-3] + "." + flow.get_domain_names()[0].split(".")[-2]
