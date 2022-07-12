#!/usr/bin/env python3

from .feature import Feature
import math

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


class UniGramDomainName(Feature):
    name = "uni_gram_domain_name"
    def extract(self, flow: object) -> list:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        return list(flow.get_domain_names()[0])


class BiGramDomainName(Feature):
    name = "bi_gram_domain_name"
    def extract(self, flow: object) -> list:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        one_gram = list(flow.get_domain_names()[0])
        bi_gram = [one_gram[i] + one_gram[i+1] for i in range(len(one_gram)-1)]
        return bi_gram


class TriGramDomainName(Feature):
    name = "tri_gram_domain_name"
    def extract(self, flow: object) -> list:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        one_gram = list(flow.get_domain_names()[0])
        tri_gram = [one_gram[i] + one_gram[i+1] + one_gram[i+2] for i in range(len(one_gram)-2)]
        return tri_gram


class NumericalPercentage(Feature):
    name = "numerical_percentage"
    def extract(self, flow: object) -> float:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        domain_name = flow.get_domain_names()[0]
        num_count = sum(char.isdigit() for char in domain_name)
        return num_count / len(flow.get_domain_names()[0])


class CharacterDistribution(Feature):
    name = "character_distribution"
    def extract(self, flow: object) -> dict:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        domain_name = flow.get_domain_names()[0]
        char_dist = {char: domain_name.count(char) for char in set(domain_name)}
        return char_dist


class CharacterEntropy(Feature):
    name = "character_entropy"
    def extract(self, flow: object) -> dict:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        domain_name = flow.get_domain_names()[0]
        char_dist = {char: domain_name.count(char) for char in set(domain_name)}
        domain_name_len = len(domain_name)
        char_entropy = 0
        for char in char_dist.keys():
            char_dist_ratio = char_dist[char] / domain_name_len
            char_entropy += -1 * char_dist_ratio * math.log2(char_dist_ratio)
        return char_entropy
