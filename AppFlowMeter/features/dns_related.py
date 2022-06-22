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
        tld_index = -2
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        return "." + flow.get_domain_names()[0].split(".")[tld_index]


class SecondLevelDomain(Feature):
    name = "second_level_domain"
    def extract(self, flow: object) -> str:
        tld_index = -2
        sld_index = -3
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        return "." + flow.get_domain_names()[0].split(".")[sld_index] + "." + flow.get_domain_names()[0].split(".")[tld_index]


class DomainNameLen(Feature):
    name = "domain_name_length"
    def extract(self, flow: object) -> str:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        return len(flow.get_domain_names()[0])


class SubDomainNameLen(Feature):
    name = "subdomain_name_length"
    def extract(self, flow: object) -> str:
        min_fqdn_len = 4
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        elif len(flow.get_domain_names()[0].split(".")) < min_fqdn_len:
            return None
        return len(flow.get_domain_names()[0].split(".")[0])