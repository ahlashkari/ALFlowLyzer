#!/usr/bin/env python3

import csv
from .strategy import Strategy

class CSVWriter(Strategy):
    #TODO: Improve it
    def write(self, file_address: str, data: dict) -> str:
        with open(file_address, 'w') as f:
            writer = csv.writer(f)
            headers = list(data.keys())
            headers.pop(0)
            writer.writerow(headers)
            for i in range(len(data["src_ip"])):
                row = []
                for header in headers:
                    row.append(data[header][i])
                writer.writerow(row)
