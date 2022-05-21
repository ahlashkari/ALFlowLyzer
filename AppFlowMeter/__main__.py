#!/usr/bin/env python3

import argparse
from .app_flow_meter import AppFlowMeter

def args_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='AppFlowMeter')
    parser.add_argument('-c', '--config-file', action='store', help='Json config file address.')
    parser.add_argument('-o', '--online-capturing', action='store_true',
                        help='Capturing mode. The default mode is offline capturing.')
    return parser


def main():
    parsed_arguments = args_parser().parse_args()
    config_file_address = "./AppFlowMeter/config.json" if parsed_arguments.config_file is None else parsed_arguments.config_file
    online_capturing = parsed_arguments.online_capturing
    app_flow_meter = AppFlowMeter(config_file_address, online_capturing)
    app_flow_meter.run()


if __name__ == "__main__":
    main()
