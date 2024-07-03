#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError as error:
    raise SystemExit(error)

version = "0.1.0"
author = "Moein Shafi"
author_email = "mosafer.moein@gmail.com"
entry_points = {
        "console_scripts": ["alflowlyzer = ALFlowLyzer.__main__:main"]
        }

setup(
        name="ALFlowLyzer",
        version=version,
        author=author,
        author_email=author_email,
        packages=[
            "ALFlowLyzer",
            "ALFlowLyzer.features",
            "ALFlowLyzer.application_flow_capturer",
            "ALFlowLyzer.writers",
        ],
        package_dir={
            "ALFlowLyzer": "ALFlowLyzer",
            "ALFlowLyzer.features": "ALFlowLyzer/features",
            "ALFlowLyzer.writers": "ALFlowLyzer/writers",
        },
        entry_points=entry_points,
)
