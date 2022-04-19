#!/usr/bin/env python3

from abc import ABC, abstractmethod

class Feature(ABC):
    @abstractmethod
    def extract(self, flows: list) -> dict:
        pass
