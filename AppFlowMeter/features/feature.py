#!/usr/bin/env python3

from abc import ABC, abstractmethod

class Feature(ABC):
    name: str
    @abstractmethod
    def extract(self, flow: object) -> dict:
        pass
