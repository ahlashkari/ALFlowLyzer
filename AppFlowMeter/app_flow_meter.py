#!/usr/bin/python3

import threading
from multiprocessing import Process

from .app_flow_capturer import AppFlowCapturer
from .feature_extractor import FeatureExtractor
from .writers import Writer, CSVWriter
from .config_loader import ConfigLoader



def test(config, i):
    app_flow_capturer = AppFlowCapturer(config.max_flow_duration, config.activity_timeout)
    print("> capturing started...")
    flows = app_flow_capturer.capture(i, config.pcap_file_address + str(i))
    return flows


class AppFlowMeter(object):
    def __init__(self, config_file_address: str, online_capturing: bool):
        print("You initiated Application Flow Meter!")
        self.config_file_address = config_file_address

    def run(self):
        config = ConfigLoader(self.config_file_address)
        # flows = test(config, 0)
        mythreads = []
        for i in range(4):
            # mythreads.append(threading.Thread(target=test, args=(config, i,)))
            mythreads.append(Process(target=test, args=(config, i,)))


        for mythread in mythreads:
            mythread.start()

        for mythread in mythreads:
            mythread.join()


        # app_flow_capturer = AppFlowCapturer(config.max_flow_duration, config.activity_timeout)
        # print("> capturing started...")
        # flows = app_flow_capturer.run(config.pcap_file_address)
        print("> capturing ended...")
        print("> features extracting started...")
        feature_extractor = FeatureExtractor(flows, config.floating_point_unit)
        data = feature_extractor.execute(config.features_ignore_list)
        print("> features extracting ended...")
        print("> writing results to", config.output_file_address)
        writer = Writer(CSVWriter())
        writer.write(config.output_file_address, data)
        print("results are ready!")

