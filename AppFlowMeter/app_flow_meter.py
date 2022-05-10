#!/usr/bin/python3

import json
from .app_flow_capturer import AppFlowCapturer
from .feature_extractor import FeatureExtractor
from .writers import Writer, CSVWriter

class AppFlowMeter(object):
    config_file = "config.json"
    def __init__(self):
        print("You initiated Application Flow Meter!")

    def run(self):
        app_flow_capturer = AppFlowCapturer()
        print("> capturing started...")
        flows = app_flow_capturer.capture(self.pcap_file)
        print("> capturing ended...")
        print("> features extracting started...")
        feature_extractor = FeatureExtractor(flows)
        data = feature_extractor.execute()
        print("> features extracting ended...")
        print("> writing results to", self.output_file)
        writer = Writer(CSVWriter())
        writer.write(self.output_file, data)
        print("results are ready!")

    # TODO: Add checking for the correctness of the input data.
    # TODO: Check the types of different inputs.
    # TODO: Add ConfigLoader class.
    def config_loader(self):
        with open(config_loader, 'r') as input_config_file:
            input_config = json.load(input_config)
            if "input_pcap_address" in input_config:
                self.pcap_file = input_config["input_pcap_address"]
            else:
                self.pcap_file = "./test.pcap"

            if "output_file_address" in input_config:
                self.output_file = input_config["output_file_address"]
            else:
                self.output_file = "./"

            if "interface_name" in input_config:
                self.pcap_file = input_config["interface_name"]
            else:
                self.pcap_file = "eth0"

            if "max_flow_duration" in input_config:
                self.max_flow_duration = input_config["max_flow_duration"]
            else:
                self.max_flow_duration = 120000

            if "activity_timeout" in input_config:
                self.activity_timeout = input_config["activity_timeout"]
            else:
                self.activity_timeout = 5000

            if "protocols" in input_config:
                self.protocols = input_config["protocols"]
            else:
                self.protocols = []

            if "floating_point_unit " in input_config:
                self.floating_point_unit = input_config["floating_point_unit"]
            else:
                self.floating_point_unit = '.64f'
