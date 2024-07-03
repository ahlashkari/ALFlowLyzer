#!/usr/bin/env python3

import argparse

from ALFlowLyzer.application_flow_analyzer import ALFlowLyzer

def args_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='ALFlowLyzer')
    parser.add_argument('-c', '--config-file', action='store', help='Json config file address.')
    parser.add_argument('-o', '--online-capturing', action='store_true',
                        help='Capturing mode. The default mode is offline capturing.')
    return parser


def main():
    parsed_arguments = args_parser().parse_args()
    config_file_address = "./ALFlowLyzer/config.json" if parsed_arguments.config_file is None else parsed_arguments.config_file
    online_capturing = parsed_arguments.online_capturing
    alflowlyzer = ALFlowLyzer(config_file_address, online_capturing)
    alflowlyzer.run()


if __name__ == "__main__":
    main()
