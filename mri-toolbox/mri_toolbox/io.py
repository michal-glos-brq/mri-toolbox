"""
This module implements io functions for NifTi files

Author: Michal Glos (michal.glos99@gmail.com)
"""

import os
import logging
import re
from typing import Dict, List, Tuple

import dicom2nifti


def convert_dicoms_to_niftis(
    dicom_dir: str, nifti_dir: str, compression: bool = True, reorient: bool = False
) -> None:
    """
    Looks for dicom files in dicom_dir, groups them by globally unique SeriesInstanceUID
    and converts each group into nifti file format then saved into nifti_dir.

    For more detail about dicom2nifti.convert_directory function see:
        https://github.com/icometrix/dicom2nifti/blob/main/dicom2nifti/convert_dir.py#L24

    Args:
        dicom_dir:    Path to the directory with DICOM files
        nifti_dir:    Path to write nifti files
        compression:  Compress (or not) final nifti files as .gz
        reorient:     Reorient data into LAS coordinates
    """
    if not os.path.isdir(dicom_dir):
        raise ValueError(
            f"Supposed directory {dicom_dir} {'is a file!' if os.path.isfile(dicom_dir) else 'does not exist!'}"
        )

    # Convert DICOM files to NifTi and group them by Series Instance UID
    dicom2nifti.convert_directory(dicom_dir, nifti_dir, compression=compression, reorient=reorient)
    logging.warning(
        f"Succesfully converted DIMCOM files from {dicom_dir}"
        f" to NifTi file format, stored in {nifti_dir}."
    )
