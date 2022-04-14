#!/usr/bin/python3

from .flow_capturer import FlowCapturer
from .feature_extractor import FeatureExtractor
from .writers import Writer, CSVWriter

class AppFlowMeter(object):
    def __init__(self):
        print("You initiated Application Flow Meter!")

    def run(self, output_file: str = "output.csv"):
        flow_capturer = FlowCapturer()
#        TODO: use config file for input pcap file & output.csv file & interface name and ...
        print("> capturing started...")
        flows = flow_capturer.capture("./test.pcap")
        print("> capturing ended...")
        print("> features extracting started...")
        feature_extractor = FeatureExtractor(flows)
        data = feature_extractor.execute()
        print("> features extracting ended...")
        print("> writing results to", output_file)
        writer = Writer(CSVWriter())
        writer.write(output_file, data)
        print("results are ready!")
