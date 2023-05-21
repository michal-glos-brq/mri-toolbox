"""
This submodule implements selected processing methods for MRI data

Author: Michal Glos (michal.glos99@gmail.com)
"""

import os
from typing import Tuple
from math import floor, ceil

import numpy as np
import nibabel as nib
import nilearn.image as nimg
import SimpleITK as sitk
from brainextractor import BrainExtractor


def get_centering_affine(object_shape: Tuple[int]) -> np.array:
    """
    Create affine 4x4 matrix with origin in the objects center.

    Parameters:
        object_shape (Tuple[int]): Shape of object, tuple of 3 integers
    Returns:
        np.array: 4x4 array with affine transformation matrix
    """
    # Normalizing voxel size (1mm side)
    affine = np.eye(4)
    # Moving the coords. origin in the center of object
    affine[:3, 3] = np.array(object_shape) / 2 * (-1)
    return affine


def reshape_nifti(nifti_image: nib.Nifti1Image, target_shape: Tuple[int]) -> nib.Nifti1Image:
    """
    Adjust the dimensions of a given MRI image data.

    Parameters:
        nifti_image (nib.Nifti1Image): Input image to be processed
        target_shape (Tuple of ints): Required data shape
    Returns:
        resized/reshaped Nifti1Image instance
    """
    if len(nifti_image.shape) != len(target_shape) or any([dim <= 0 for dim in target_shape]):
        raise ValueError(
            f"Requested shape {target_shape} invalid and could not be applied to data of shape {nifti_image.shape}!"
        )

    # Obtain the new affine matrix for transformation
    new_affine = get_centering_affine(target_shape)
    # Perform the affine transformation
    new_nifti = nimg.resample_img(nifti_image, new_affine, interpolation="continuous")

    return new_nifti


def apply_N4_correction(nifti_image: nib.Nifti1Image, shrink_factor: int = 1) -> nib.Nifti1Image:
    """
    Apply Simple ITK N4 bias correction.

    Parameters:
        nifti_image (nib.Nifti1Image): Input image to be processed
        shrink_factor (int): Perform computation on shrunk data (faster)
    Returns:
        nib.Nifti1Image - N4-corrected nifti image
    """
    # Load the nifti file into sitk object, shrink it eventually
    sitk_file = sitk.GetImageFromArray(nifti_image.get_fdata().astype(np.float32))
    sitk_file_shrunk = sitk.Shrink(sitk_file, [shrink_factor] * sitk_file.GetDimension())

    # Mask empty regions to speed up the computation
    head_mask_shrunk = sitk.OtsuThreshold(sitk_file_shrunk, 0, 1, 256)

    # Instantiate and execute the N4 bias corrector on shrunk data
    corrector = sitk.N4BiasFieldCorrectionImageFilter()
    _ = corrector.Execute(sitk_file_shrunk, head_mask_shrunk)

    # Retrieve and interpolate the bias field, apply the correction on original data
    log_bias_field = corrector.GetLogBiasFieldAsImage(sitk_file)
    corrected_image = sitk_file / sitk.Exp(log_bias_field)

    # Convert sitk to nibabel - primary working format
    corrected_data = sitk.GetArrayFromImage(corrected_image)
    corrected_nifti_image = nib.Nifti1Image(
        corrected_data, get_centering_affine(corrected_data.shape)
    )

    return corrected_nifti_image


def isolate_brain_tissue(nifti_image: nib.Nifti1Image, iterations: int = 1000) -> nib.Nifti1Image:
    """
    Isolate brain tissue from NifTi file using BET from BrainExtractor module.

    Parameters:
        nifti_image (nib.Nifti1Image): Input nifti image to be processed
    Returns:
        nib.Nifti1Image - Skull-stripped input image with brain data only
    """
    # Compute the brain mask for nifti_image input
    bet = BrainExtractor(img=nifti_image)
    bet.run(iterations=iterations)
    brain_mask = bet.compute_mask()

    # Apply the mask and instantiate new nib nifti image
    extracted_brain_data = nifti_image.get_fdata() * brain_mask
    nifti_brain_file = nib.Nifti1Image(extracted_brain_data, nifti_image.affine)

    return nifti_brain_file
