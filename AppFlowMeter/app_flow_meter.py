#!/usr/bin/python3

from .app_flow_capturer import AppFlowCapturer
from .feature_extractor import FeatureExtractor
from .writers import Writer, CSVWriter
from .config_loader import ConfigLoader

class AppFlowMeter(object):
    def __init__(self, config_file_address: str):
        print("You initiated Application Flow Meter!")
        self.config_file_address = config_file_address

    def run(self):
        config = ConfigLoader(self.config_file_address)
        app_flow_capturer = AppFlowCapturer(config.max_flow_duration, config.activity_timeout)
        print("> capturing started...")
        flows = app_flow_capturer.capture(config.pcap_file_address)
        print("> capturing ended...")
        print("> features extracting started...")
        feature_extractor = FeatureExtractor(flows, config.floating_point_unit)
        data = feature_extractor.execute()
        print("> features extracting ended...")
        print("> writing results to", config.output_file_address)
        writer = Writer(CSVWriter())
        writer.write(config.output_file_address, data)
        print("results are ready!")

