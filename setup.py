#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError as error:
    raise SystemExit(error)

version = "0.1.0"
author = "Moein Shafi"
author_email = "mosafer.moein@gmail.com"
entry_points = {
        "console_scripts": ["app-flow-meter = AppFlowMeter.__main__:main"]
        }

setup(
        name="AppFlowMeter",
        version=version,
        author=author,
        author_email=author_email,
        packages=[
            "AppFlowMeter",
            "AppFlowMeter.features",
            "AppFlowMeter.flow_capturer",
            "AppFlowMeter.writers",
        ],
        package_dir={
            "AppFlowMeter": "AppFlowMeter",
            "AppFlowMeter.features": "AppFlowMeter/features",
            "AppFlowMeter.writers": "AppFlowMeter/writers",
        },
        entry_points=entry_points,
)
