#!/usr/bin/python3

from .flow_capturer import FlowCapturer
from .feature_extractor import FeatureExtractor
from .writers import Writer, CSVWriter

class AppFlowMeter(object):
    def __init__(self):
        print("You initiated Application Flow Meter!")

    def run(self, output_file: str = "output.csv"):
        print("run")
        flow_capturer = FlowCapturer()
        flows = flow_capturer.capture()
        feature_extractor = FeatureExtractor(flows)
        data = feature_extractor.execute()
        writer = Writer(CSVWriter())
        writer.write(output_file, data)
        print("end")
