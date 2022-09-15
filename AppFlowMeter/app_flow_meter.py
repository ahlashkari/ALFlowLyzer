#!/usr/bin/python3

import psutil
import os
from multiprocessing import Process, Manager, Lock
from threading import Thread
from .app_flow_capturer import AppFlowCapturer
from .feature_extractor import FeatureExtractor
from .writers import Writer, CSVWriter
from .config_loader import ConfigLoader


class AppFlowMeter(object):
    def __init__(self, config_file_address: str, online_capturing: bool):
        print("You initiated Application Flow Meter!")
        self.__config_file_address = config_file_address

    def run(self):
        self.__config = ConfigLoader(self.__config_file_address)
        with Manager() as manager:
            self.__flows = manager.list()
            self.__data = manager.list()
            capturers = []
            self.__threads = []
            self.__threads_pid = manager.list()
            self.__watchdog_feature_extractor_pid = manager.Value('i', 0)
            self.__data_lock = Lock()
            self.__flows_lock = Lock()

            for i in range(self.__config.number_of_threads):
                capturers.append(AppFlowCapturer(self.__config.max_flow_duration,
                                                 self.__config.activity_timeout))
                self.__threads_pid.append(0)
                self.__threads.append(Process(target=capturers[i].capture,
                                         args=(i, self.__config.pcap_file_address + str(i),
                                                self.__flows, self.__flows_lock, self.__threads_pid[i])))
            self.__watchdog_feature_extractor = Process(target=self.feature_extractor, daemon=True)
            self.__watchdog_writer = Process(target=self.writer, daemon=True)

            print("> capturing started...")
            for mythread in self.__threads:
                mythread.start()
            self.__watchdog_feature_extractor.start()
            self.__watchdog_writer.start()

            for mythread in self.__threads:
                mythread.join()
            self.__watchdog_feature_extractor.join()
            self.__watchdog_writer.join()
            print("results are ready!")

    def feature_extractor(self):
        # TODO: read from file
        label = "benign"
        self.__watchdog_feature_extractor_pid = os.getpid()
        print(10*">", self.__watchdog_writer.pid)

        feature_extractor = FeatureExtractor(self.__config.floating_point_unit)
        while 1:
            # print(10*">", self.__watchdog_writer.pid)
            # TODO: read from file
            if len(self.__flows) > 500:
                with self.__data_lock and self.__flows_lock:
                    print(50*"$")
                    self.__data.extend(feature_extractor.execute(self.__flows, label))
                    self.__flows.clear()
                    print(50*"$")
            # if not any(psutil.pid_exists(thread_pid) for thread_pid in self.__threads_pid):
            # if not any(thread.is_alive() for thread in self.__threads):
                # return

    def writer(self):
        writer = Writer(CSVWriter())
        header_writing_mode = 'w'
        data_writing_mode = 'a'
        file_address = self.__config.output_file_address
        writer.write(file_address, self.__data, header_writing_mode, only_headers=True)
        print(20*"(", self.__watchdog_writer.pid)

        while 1:
            # TODO: read from file
            if len(self.__data) > 5000:
                with self.__data_lock and self.__flows_lock:
                    print(50*"*")
                    writer.write(file_address, self.__data, data_writing_mode)
                    self.__data.clear()
                    print(50*"*")
            # if psutil.pid_exists(self.__watchdog_feature_extractor_pid):
            # # if not self.__watchdog_feature_extractor.is_alive():
            #     writer.write(file_address, self.__data, data_writing_mode)
            #     return