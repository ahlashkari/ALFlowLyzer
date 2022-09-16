#!/usr/bin/python3

import psutil
import os
from multiprocessing import Process, Manager, Lock
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
            self.__threads_pid = manager.list([manager.Value('i', 0) for i in range(self.__config.number_of_threads)])
            self.__watchdog_feature_extractor_pid = manager.Value('i', 0)
            self.__data_lock = Lock()
            self.__flows_lock = Lock()

            for i in range(self.__config.number_of_threads):
                capturers.append(AppFlowCapturer(self.__config.max_flow_duration,
                                                 self.__config.activity_timeout))
                self.__threads.append(Process(target=capturers[i].capture,
                                         args=(i, self.__config.pcap_file_address + str(i),
                                                self.__flows, self.__flows_lock, self.__threads_pid[i],)))
            self.__watchdog_feature_extractor = Process(target=self.feature_extractor, daemon=True)
            self.__watchdog_writer = Process(target=self.writer, daemon=True)

            print("> capturing started...")
            for thread in self.__threads:
                thread.start()
            self.__watchdog_feature_extractor.start()
            self.__watchdog_writer.start()

            for thread in self.__threads:
                thread.join()
            self.__watchdog_feature_extractor.join()
            self.__watchdog_writer.join()
            print("results are ready!")

    def feature_extractor(self):
        # TODO: read from file
        label = "benign"
        self.__watchdog_feature_extractor_pid.set(os.getpid())

        feature_extractor = FeatureExtractor(self.__config.floating_point_unit)
        while 1:
            # TODO: read from file
            if len(self.__flows) > 1000:
                with self.__data_lock and self.__flows_lock:
                    # TODO: temp = self.__flows # copy it and then work with the copy and release the lock
                    print(50*"$")
                    aa = feature_extractor.execute(self.__flows, label)
                    print("OKOKOKOKOK")
                    self.__data.extend(aa)
                    print("OK")
                    # self.__flows.clear()
                    self.__flows[:] = []
                    print(50*"$")
            if not any(psutil.pid_exists(thread_pid.get()) for thread_pid in self.__threads_pid):
                print("::::::::::")
                return

    def writer(self):
        writer = Writer(CSVWriter())
        header_writing_mode = 'w'
        data_writing_mode = 'a'
        file_address = self.__config.output_file_address
        writer.write(file_address, self.__data, header_writing_mode, only_headers=True)

        while 1:
            # TODO: read from file
            if len(self.__data) > 1000:
                with self.__data_lock and self.__flows_lock:
                    # TODO: copy data and release the lock
                    print(50*"*")
                    writer.write(file_address, self.__data, data_writing_mode)
                    self.__data[:] = []
                    # self.__data.clear()
                    print(50*"*")
            if not psutil.pid_exists(self.__watchdog_feature_extractor_pid.get()):
                print("^^^^^^^", len(self.__data))
                writer.write(file_address, self.__data, data_writing_mode)
                return