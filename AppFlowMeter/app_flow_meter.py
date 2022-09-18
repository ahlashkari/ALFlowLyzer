#!/usr/bin/python3

import multiprocessing
from multiprocessing import Process, Manager, Pool

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
            self.number_of_th = multiprocessing.cpu_count() - 1
            if self.__config.number_of_threads is not None:
                self.number_of_th = self.__config.number_of_threads

            self.__threads_pid = manager.list([manager.Value('i', 0) for i in range(self.number_of_th - 1)])
            self.__data_lock = manager.Lock()
            self.__flows_lock = manager.Lock()
            self.__feature_extractor_watchdog_lock = manager.Lock()
            self.__finish = manager.Value('i', 0)

            with Pool(processes=self.number_of_th) as pool:
                for i in range(self.number_of_th - 1):
                    capturers.append(AppFlowCapturer(self.__config.max_flow_duration,
                                                    self.__config.activity_timeout))
                    self.__threads.append(pool.starmap_async(capturers[i].capture,
                            [(i, self.__config.pcap_file_address + str(i), self.__flows, 
                            self.__flows_lock, self.__threads_pid[i],)]))

                writer_thread = Process(target=self.writer)
                writer_thread.start()
                self.feature_extractor(pool)
                pool.close()
                pool.join()
                writer_thread.join()
        print("results are ready!")

    def feature_extractor(self, pool: Pool):
        # TODO: read from file
        label = "benign"
        feature_extractor = FeatureExtractor(self.__config.floating_point_unit)
        while 1:
            # TODO: read from file
            if len(self.__flows) >= 4000:
                temp_flows = []
                with self.__flows_lock:
                    temp_flows.extend(self.__flows)
                    self.__flows[:] = []

                pool.starmap_async(feature_extractor.execute, 
                        [(self.__data, self.__data_lock, temp_flows,
                        self.__config.features_ignore_list, label)]
                )
                del temp_flows
            if not any(thread_pid.get() == 0 for thread_pid in self.__threads_pid):
                pool.starmap(feature_extractor.execute,
                        [(self.__data, self.__data_lock, self.__flows,
                        self.__config.features_ignore_list, label)]
                )
                with self.__feature_extractor_watchdog_lock:
                    self.__finish.set(1)
                return

    def writer(self):
        writer = Writer(CSVWriter())
        header_writing_mode = 'w'
        data_writing_mode = 'a+'
        file_address = self.__config.output_file_address
        first = True

        while 1:
            # TODO: read from file
            if len(self.__data) > 6000:
                if first:
                    writer.write(file_address, self.__data, header_writing_mode, only_headers=True)
                    first = False
                temp_data = []
                print("### writer", len(self.__data))
                with self.__data_lock:
                    temp_data.extend(self.__data)
                    self.__data[:] = []
                writer.write(file_address, temp_data, data_writing_mode)
                del temp_data
            with self.__feature_extractor_watchdog_lock:
                if self.__finish.get() != 0:
                    print(50*"@")
                    writer.write(file_address, self.__data, data_writing_mode)
                    return
