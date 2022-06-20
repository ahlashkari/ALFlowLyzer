#!/usr/bin/env python3

import whois
import datetime
from .feature import Feature


class DomainName(Feature):
    name = "dns_domain_name"
    def extract(self, flow: object) -> str:
        if flow.get_protocol() != "DNS":
            return "not a dns flow"
        return flow.get_domain_names()[0]


class WhoisInfo(Feature):
    whois_response = None
    res = {}
    def extract(self, flow: object) -> str:
        pass

    def get_whois_info(self, flow):
        if flow.get_protocol() != "DNS":
            return "not a dns flow"

        try:
            domain_name = flow.get_domain_names()[0]
            index = len(domain_name) - 1
            domain_name = domain_name[:index] + "" + domain_name[index + 1:]
            if domain_name in self.res:
                return self.res[domain_name]
            print(domain_name)
            self.whois_response = whois.whois(domain_name)
        except:
            pass

        self.res[domain_name] = self.whois_response
        return "No information found" if self.whois_response is None else self.whois_response


class DomainEmail(WhoisInfo):
    name = "dns_domain_email"
    def extract(self, flow: object) -> str:
        #        super().get_whois_info(flow)
        result = self.get_whois_info(flow)
#        return result if self.whois_response is None else ", ".join(self.whois_response.emails)
        return result if self.whois_response is None else self.whois_response.emails


class DomainRegistrar(WhoisInfo):
    name = "dns_domain_registrar"
    def extract(self, flow: object) -> str:
        #        super().get_whois_info(flow)
        result = self.get_whois_info(flow)
        return result if self.whois_response is None else self.whois_response.registrar


class DomainCreationDate(WhoisInfo):
    name = "dns_domain_creation_date"
    def extract(self, flow: object) -> str:
        #        super().get_whois_info(flow)
        result = self.get_whois_info(flow)
        try:
            return result if self.whois_response is None else datetime.datetime.fromtimestamp(self.whois_response.creation_date)
        except:
            return "ERROR"


class DomainExpirationDate(WhoisInfo):
    name = "dns_domain_expiration_date"
    def extract(self, flow: object) -> str:
        #        super().get_whois_info(flow)
        result = self.get_whois_info(flow)
        try:
            return result if self.whois_response is None else datetime.datetime.fromtimestamp(self.whois_response.expiration_date)
        except:
            return "ERROR"


class DomainAge(WhoisInfo):
    name = "dns_domain_age"
    def extract(self, flow: object) -> str:
        #        super().get_whois_info(flow)
        result = self.get_whois_info(flow)
        try:
            return result if self.whois_response is None else (datetime.datetime.today() - self.whois_response.creation_date).days 
        except:
            return "ERROR"


class DomainCountry(WhoisInfo):
    name = "dns_domain_country"
    def extract(self, flow: object) -> str:
        #        super().get_whois_info(flow)
        result = self.get_whois_info(flow)
        return result if self.whois_response is None else self.whois_response.country


class DomainDNSSEC(WhoisInfo):
    name = "dns_domain_dnssec"
    def extract(self, flow: object) -> str:
        #        super().get_whois_info(flow)
        result = self.get_whois_info(flow)
        return result if self.whois_response is None else self.whois_response.dnssec


class DomainOrganization(WhoisInfo):
    name = "dns_domain_dnssec"
    def extract(self, flow: object) -> str:
        #        super().get_whois_info(flow)
        result = self.get_whois_info(flow)
        return result if self.whois_response is None else self.whois_response.org


class DomainAddress(WhoisInfo):
    name = "dns_domain_address"
    def extract(self, flow: object) -> str:
        #        super().get_whois_info(flow)
        result = self.get_whois_info(flow)
        return result if self.whois_response is None else self.whois_response.address


class DomainCity(WhoisInfo):
    name = "dns_domain_city"
    def extract(self, flow: object) -> str:
        #        super().get_whois_info(flow)
        result = self.get_whois_info(flow)
        return result if self.whois_response is None else self.whois_response.city


class DomainState(WhoisInfo):
    name = "dns_domain_state"
    def extract(self, flow: object) -> str:
        #        super().get_whois_info(flow)
        result = self.get_whois_info(flow)
        return result if self.whois_response is None else self.whois_response.state


class DomainZipcode(WhoisInfo):
    name = "dns_domain_zipcode"
    def extract(self, flow: object) -> str:
        #        super().get_whois_info(flow)
        result = self.get_whois_info(flow)
        return result if self.whois_response is None else self.whois_response.zipcode


class DomainNameServers(WhoisInfo):
    name = "dns_domain_name_servers"
    def extract(self, flow: object) -> str:
        #        super().get_whois_info(flow)
        result = self.get_whois_info(flow)
        return result if self.whois_response is None else self.whois_response.name_servers


class DomainUpdatedDate(WhoisInfo):
    name = "dns_domain_updated_date"
    def extract(self, flow: object) -> str:
        #        super().get_whois_info(flow)
        result = self.get_whois_info(flow)
        return result if self.whois_response is None else self.whois_response.updated_date
