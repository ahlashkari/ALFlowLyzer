#!/usr/bin/env python3

import datetime
import math
import statistics
import string
import whois
from scipy import stats
from .feature import Feature

domains = {}

class DomainName(Feature):
    name = "dns_domain_name"
    def extract(self, flow: object) -> str:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        domain_name = flow.get_domain_names()[0]
        index = len(domain_name) - 1
        domain_name = domain_name[:index] + "" + domain_name[index + 1:]
        return domain_name
        return flow.get_domain_names()[0]


class WhoisInfo(Feature):
    def get_domain_name(self, flow):
        domain_name = flow.get_domain_names()[0]
        index = len(domain_name) - 1
        domain_name = domain_name[:index] + "" + domain_name[index + 1:]
        return domain_name

    def get_whois_info(self, flow):
        if flow.get_protocol() != "DNS":
            return "not a dns flow"

        try:
            domain_name = self.get_domain_name(flow)
            if domain_name not in domains:
                print(domain_name)
                whois_response = whois.whois(domain_name)
                domains[domain_name] = whois_response
        except:
            domains[domain_name] = None

        return "No information found" if domains[domain_name] is None else domains[domain_name]


class WhoisDomainName(WhoisInfo):
    name = "dns_whois_domain_name"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        return result if whois_response is None else whois_response.domain_name


class DomainEmail(WhoisInfo):
    name = "dns_domain_email"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        return result if whois_response is None else whois_response.emails


class DomainRegistrar(WhoisInfo):
    name = "dns_domain_registrar"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        return result if whois_response is None else whois_response.registrar


class DomainCreationDate(WhoisInfo):
    name = "dns_domain_creation_date"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        try:
            return result if whois_response is None else whois_response.creation_date
        except:
            return "ERROR"


class DomainExpirationDate(WhoisInfo):
    name = "dns_domain_expiration_date"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        try:
            return result if whois_response is None else whois_response.expiration_date
        except:
            return "ERROR"


class DomainAge(WhoisInfo):
    name = "dns_domain_age"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        try:
            if whois_response.creation_date is None:
                return "no creation date"
            return result if whois_response is None else (datetime.datetime.today() - whois_response.creation_date).days 
        except:
            return "ERROR"


class DomainCountry(WhoisInfo):
    name = "dns_domain_country"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        return result if whois_response is None else whois_response.country


class DomainDNSSEC(WhoisInfo):
    name = "dns_domain_dnssec"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        return result if whois_response is None else whois_response.dnssec


class DomainOrganization(WhoisInfo):
    name = "dns_domain_dnssec"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        return result if whois_response is None else whois_response.org


class DomainAddress(WhoisInfo):
    name = "dns_domain_address"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        return result if whois_response is None else whois_response.address


class DomainCity(WhoisInfo):
    name = "dns_domain_city"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        return result if whois_response is None else whois_response.city


class DomainState(WhoisInfo):
    name = "dns_domain_state"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        return result if whois_response is None else whois_response.state


class DomainZipcode(WhoisInfo):
    name = "dns_domain_zipcode"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        return result if whois_response is None else whois_response.zipcode


class DomainNameServers(WhoisInfo):
    name = "dns_domain_name_servers"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        return result if whois_response is None else whois_response.name_servers


class DomainUpdatedDate(WhoisInfo):
    name = "dns_domain_updated_date"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        return result if whois_response is None else whois_response.updated_date


class TopLevelDomain(Feature):
    name = "dns_top_level_domain"
    def extract(self, flow: object) -> str:
        tld_index = -2
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        try:
            return "." + flow.get_domain_names()[0].split(".")[tld_index]
        except:
            return "ERROR"


class SecondLevelDomain(Feature):
    name = "dns_second_level_domain"
    def extract(self, flow: object) -> str:
        tld_index = -2
        sld_index = -3
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        try:
            return "." + flow.get_domain_names()[0].split(".")[sld_index] + "." + flow.get_domain_names()[0].split(".")[tld_index]
        except:
            return "ERROR"


class DomainNameLen(Feature):
    name = "dns_domain_name_length"
    def extract(self, flow: object) -> str:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        return len(flow.get_domain_names()[0])


class SubDomainNameLen(Feature):
    name = "dns_subdomain_name_length"
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
    def extract(self, flow: object) -> float:
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


class ContinuousNumericMaxLen(Feature):
    name = "max_continuous_numeric_len"
    def extract(self, flow: object) -> int:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        domain_name = flow.get_domain_names()[0]
        max_len, max_len_temp, local_pointer, global_pointer = 0, 0, 0, 0
        while global_pointer < len(domain_name)-1:
            max_len_temp, local_pointer = 0, 0
            if domain_name[global_pointer].isnumeric():
                local_pointer = global_pointer
                while(domain_name[local_pointer].isnumeric()):
                    max_len_temp += 1
                    local_pointer += 1
                    if local_pointer >= len(domain_name):
                        break
                global_pointer = local_pointer
            else:
                global_pointer += 1
            if max_len_temp > max_len:
                max_len = max_len_temp
        return max_len


class ContinuousAlphabetMaxLen(Feature):
    name = "max_continuous_alphabet_len"
    def extract(self, flow: object) -> int:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        domain_name = flow.get_domain_names()[0]
        max_len, max_len_temp, local_pointer, global_pointer = 0, 0, 0, 0
        while global_pointer < len(domain_name)-1:
            max_len_temp, local_pointer = 0, 0
            if domain_name[global_pointer].isalpha():
                local_pointer = global_pointer
                while(domain_name[local_pointer].isalpha()):
                    max_len_temp += 1
                    local_pointer += 1
                    if local_pointer >= len(domain_name):
                        break
                global_pointer = local_pointer
            else:
                global_pointer += 1
            if max_len_temp > max_len:
                max_len = max_len_temp
        return max_len


class ContinuousConsonantsMaxLen(Feature):
    name = "max_continuous_consonants_len"
    def extract(self, flow: object) -> int:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        consonants = list("bcdfghjklmnpqrstvwxyz")
        domain_name = flow.get_domain_names()[0]
        max_len, max_len_temp, local_pointer, global_pointer = 0, 0, 0, 0
        while global_pointer < len(domain_name)-1:
            max_len_temp, local_pointer = 0, 0
            if domain_name[global_pointer] in consonants:
                local_pointer = global_pointer
                while(domain_name[local_pointer] in consonants):
                    max_len_temp += 1
                    local_pointer += 1
                    if local_pointer >= len(domain_name):
                        break
                global_pointer = local_pointer
            else:
                global_pointer += 1
            if max_len_temp > max_len:
                max_len = max_len_temp
        return max_len


class ContinuousSameAlphabetMaxLen(Feature):
    name = "max_continuous_same_alphabet_len"
    def extract(self, flow: object) -> int:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        domain_name = flow.get_domain_names()[0]
        max_len, max_len_temp, local_pointer, global_pointer = 0, 0, 0, 0
        while global_pointer < len(domain_name)-1:
            max_len_temp, local_pointer = 0, 0
            if domain_name[global_pointer].isalpha():
                alphabet = domain_name[global_pointer]
                local_pointer = global_pointer
                while(domain_name[local_pointer] == alphabet):
                    max_len_temp += 1
                    local_pointer += 1
                    if local_pointer >= len(domain_name):
                        break
            global_pointer += 1
            if max_len_temp > max_len:
                max_len = max_len_temp
        return max_len


class VowelsConsonantRatio(Feature):
    name = "vowels_consonant_ratio"
    def extract(self, flow: object) -> float:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        consonants = list("bcdfghjklmnpqrstvwxyz")
        vowels = list("aeiou")
        vowel_count, consonant_count = 0, 0
        domain_name = flow.get_domain_names()[0]
        for char in domain_name:
            if char in vowels:
                vowel_count += 1
            elif char in consonants:
                consonant_count += 1
        return vowel_count / consonant_count


class DistinctTTLValues(Feature):
    name = "distinct_ttl_values"
    def extract(self, flow: object) -> int:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"   
        ttl_values = [packet.get_dns_ttl_value() for packet in flow.get_packets()]
        return len(set(ttl_values))


class TTLValuesMin(Feature):
    name = "ttl_values_min"
    def extract(self, flow: object) -> int:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"   
        ttl_values = [packet.get_dns_ttl_value() for packet in flow.get_packets()]
        return min(ttl_values)


class TTLValuesMax(Feature):
    name = "ttl_values_max"
    def extract(self, flow: object) -> int:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"   
        ttl_values = [packet.get_dns_ttl_value() for packet in flow.get_packets()]
        return max(ttl_values)


class TTLValuesMean(Feature):
    name = "ttl_values_mean"
    def extract(self, flow: object) -> int:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"   
        ttl_values = [packet.get_dns_ttl_value() for packet in flow.get_packets()]
        return format(statistics.mean(ttl_values), self.floating_point_unit)


class TTLValuesMode(Feature):
    name = "ttl_values_mode"
    def extract(self, flow: object) -> int:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"   
        ttl_values = [packet.get_dns_ttl_value() for packet in flow.get_packets()]
        return format(float(stats.mode(ttl_values)[0]), self.floating_point_unit)


class TTLValuesVariance(Feature):
    name = "ttl_values_variance"
    def extract(self, flow: object) -> float:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"   
        ttl_values = [packet.get_dns_ttl_value() for packet in flow.get_packets()]
        return format(statistics.pvariance(ttl_values), self.floating_point_unit)


class TTLValuesStandardDeviation(Feature):
    name = "ttl_values_standard_deviation"
    def extract(self, flow: object) -> float:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"   
        ttl_values = [packet.get_dns_ttl_value() for packet in flow.get_packets()]
        return format(statistics.pstdev(ttl_values), self.floating_point_unit)


class TTLValuesMedian(Feature):
    name = "ttl_values_median"
    def extract(self, flow: object) -> float:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"   
        ttl_values = [packet.get_dns_ttl_value() for packet in flow.get_packets()]
        return format(statistics.median(ttl_values), self.floating_point_unit)


class TTLValuesSkewness(Feature):
    name = "ttl_values_skewness"
    def extract(self, flow: object) -> float:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"   
        ttl_values = [packet.get_dns_ttl_value() for packet in flow.get_packets()]
        return format(stats.skew(ttl_values), self.floating_point_unit)


class TTLValuesCoefficientOfVariation(Feature):
    name = "ttl_values_coefficient_of_variation"
    def extract(self, flow: object) -> float:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"   
        ttl_values = [packet.get_dns_ttl_value() for packet in flow.get_packets()]
        return format(stats.variation(ttl_values), self.floating_point_unit)    


class DistinctArecords(Feature):
    name = "distinct_A_records"
    def extract(self, flow: object) -> int:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        rr_type = [packet.get_dns_rr_type() for packet in flow.get_packets()]
        A_record_code = 1
        return rr_type.count(A_record_code)
