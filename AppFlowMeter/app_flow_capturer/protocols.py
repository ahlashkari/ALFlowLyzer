#!/usr/bin/env python3

from enum import Enum

class Protocols(Enum):
    HTTP = 80
    HTTPS = 443
    DNS = 53

    def __str__(self):
        return str(self.value)
