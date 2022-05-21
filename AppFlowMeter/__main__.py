#!/usr/bin/env python3

from .app_flow_meter import AppFlowMeter

def main():
    config_file_address = "./AppFlowMeter/config.json"
    app_flow_meter = AppFlowMeter(config_file_address)
    app_flow_meter.run()


if __name__ == "__main__":
    main()
