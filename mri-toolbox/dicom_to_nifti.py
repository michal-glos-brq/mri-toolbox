#! /usr/bin/env python3

"""
Simple command line interface for convert_dicoms_to_niftis function

Author: Michal Glos (michal.glos99@gmail.com)
"""

import os
import argparse
import logging

from mri_toolbox.io import convert_dicoms_to_niftis

parser = argparse.ArgumentParser()

parser.add_argument(
    "-i",
    "--input-dir",
    type=str,
    required=True,
    help="Path to a directory with DICOM files to be converted to NifTi format.",
)

parser.add_argument(
    "-o",
    "--output-dir",
    type=str,
    required=True,
    help="Path to the directory for resulting NifTi files.",
)

parser.add_argument("-c", "--compress", action="store_true", help="Compress NifTi files as .gz.")
parser.add_argument(
    "-r", "--reorient", action="store_true", help="Reorient scans to LAS coordination system."
)

parser.add_argument("-d", "--debug", action="store_true", help="Toggle INFO logging level instead of WARNING.")

if __name__ == "__main__":

    args = parser.parse_args()

    # Set logging level to debug if required, set to INFO otherwise
    logging.basicConfig(encoding='utf-8', level=logging.INFO if args.debug else logging.WARNING)

    # Convert DICOM to Nifti
    convert_dicoms_to_niftis(
        args.input_dir, args.output_dir, compression=args.compress, reorient=args.reorient
    )
