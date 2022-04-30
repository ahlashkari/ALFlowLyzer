#!/usr/bin/env python3

from abc import ABC, abstractmethod

class Feature(ABC):
    name: str
    # TODO: read this from config file
    floating_point_unit = '.64f'
    @abstractmethod
    def extract(self, flow: object) -> dict:
        pass
