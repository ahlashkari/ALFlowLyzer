#!/usr/bin/env python3

from .strategy import Strategy

class CSVWriter(Strategy):
    def write(self, file_address: str, data: dict) -> str:
        print("csv writer")
        print(data)
