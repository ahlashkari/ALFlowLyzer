#!/usr/bin/env python3

import whois
import datetime
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
    def extract(self, flow: object) -> str:
        pass

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
#                domains[domain_name] = whois_response.copy()
                domains[domain_name] = whois_response
        except:
            domains[domain_name] = None

        return "No information found" if domains[domain_name] is None else domains[domain_name]


class WhoisDomainName(WhoisInfo):
    name = "dns_whois_domain_name"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
#        return result if whois_response is None else ", ".join(whois_response.emails)
        return result if whois_response is None else whois_response.domain_name


class DomainEmail(WhoisInfo):
    name = "dns_domain_email"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
#        return result if whois_response is None else ", ".join(whois_response.emails)
        return result if whois_response is None else whois_response.emails


class DomainRegistrar(WhoisInfo):
    name = "dns_domain_registrar"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
#        print(whois_response)
        return result if whois_response is None else whois_response.registrar


class DomainCreationDate(WhoisInfo):
    name = "dns_domain_creation_date"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        try:
            return result if whois_response is None else datetime.datetime.fromtimestamp(whois_response.creation_date)
        except:
            return "ERROR"


class DomainExpirationDate(WhoisInfo):
    name = "dns_domain_expiration_date"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        try:
            return result if whois_response is None else datetime.datetime.fromtimestamp(whois_response.expiration_date)
        except:
            return "ERROR"


class DomainAge(WhoisInfo):
    name = "dns_domain_age"
    def extract(self, flow: object) -> str:
        result = self.get_whois_info(flow)
        whois_response = domains[self.get_domain_name(flow)]
        try:
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
