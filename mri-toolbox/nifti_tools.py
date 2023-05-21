#! /usr/bin/env python3

"""
Simple command line interface for mri_toolbox

Author: Michal Glos (michal.glos99@gmail.com)
"""

import os
import logging
from pathlib import Path
from argparse import ArgumentParser

import nibabel as nib

import mri_toolbox


class RunIrrelevantError:
    """If neither visual or file output specified, the whole computation would be irrelevant"""


parser = ArgumentParser()

parser.add_argument("-i", "--input", type=str, help="Path to a NifTi file to be processed.")

parser.add_argument("-o", "--output", type=str, help="Path to save the resulting NifTi file.")

parser.add_argument(
    "-s",
    "--shape",
    type=int,
    nargs="+",
    help=(
        "Resize NifTi files to a specified shape. "
        "Provide either 1 integer (cube) or spedify the shape fully with 3 integers."
    ),
)

parser.add_argument(
    "-v",
    "--visualize",
    type=str,
    choices=["3D", "slices"],
    help=(
        "Visualize the MRI scan after all selected processes are finished. "
        "Could visualize as a simple 3D object or interactively sliced 3D object."
    ),
)


parser.add_argument(
    "-c",
    "--correction",
    nargs="?",
    type=int,
    default=None,
    const=1,
    help=(
        "Perform N4 correction. Optional argument specifies shrink factor"
        " to scale image when computing N4 bias to speedup (default=1)."
    ),
)

parser.add_argument(
    "-b",
    "--brain",
    type=int,
    nargs="?",
    default=None,
    const=1000,
    help=(
        "Extract brain from MRI image. Optional argument "
        "specifies number of iteration in approximating brain mask (default=1000)."
    ),
)

parser.add_argument(
    "-d", "--debug", action="store_true", help="Toggle INFO logging level instead of WARNING."
)

if __name__ == "__main__":
    args = parser.parse_args()

    if args.output is None and not args.visualize:
        raise RunIrrelevantError("No ouput specified, use --output or --visualize options!")

    if args.output is not None and os.path.isdir(args.output):
        raise FileExistsError(f"Output path {args.output} already exists!")

    if args.shape is not None and (len(args.shape) != 1 or len(args.shape) != 3):
        raise ValueError(
            f"Received invalid shape {args.shape}! Either specify a cube"
            "by a single endge size or specify the shape completely with 3 sizes!"
        )

    logging.basicConfig(encoding="utf-8", level=logging.INFO if args.debug else logging.WARNING)

    # Load input image
    nifti_image = nib.load(args.input)

    # Perform NifTi reshaping
    if args.shape:
        shape = args.shape * 3 if len(args.shape) == 1 else args.shape
        nifti_image = mri_toolbox.process.reshape_nifti(nifti_image, shape)
        logging.warning(f"Successfully reshaped image to {shape}.")

    # Perform N4 Bias correctio
    if args.correction:
        nifti_image = mri_toolbox.process.apply_N4_correction(
            nifti_image, shrink_factor=args.correction
        )
        logging.warning(
            f"Successfully finished N4 bias correction with shrink factor of {args.correction}."
        )

    # Perform brain extraction
    if args.brain:
        nifti_image = mri_toolbox.process.isolate_brain_tissue(nifti_image, iterations=args.brain)
        logging.warning(f"Succesfully finished brain extraction over {args.brain} iterations.")

    # Save the NifTi file
    if args.output is not None:
        # Make sure all parent directories exist
        os.makedirs(Path(args.output).parent, exist_ok=True)
        nib.save(nifti_image, args.output)
        logging.warning(f"NifTi file saved as {args.output}.")

    if args.visualize:
        # Instantiate the visualizer class, show the content
        if args.visualize == "slices":
            mri_visualizer = mri_toolbox.visualize.MRIVizSlicer(nifti_image.get_fdata())
            mri_visualizer.show()
        else:
            data = nifti_image.get_fdata()
            mri_toolbox.visualize.plot_3d_object(data)
