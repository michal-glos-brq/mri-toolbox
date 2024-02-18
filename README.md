#  MRI Toolbox

This repository was developed as a part of a job interview for Alzheimer-detecting diagnosis system.

The `mri-toolbox` is a Python 3 module equipped with CLI scripts. The module offers the following capabilities:
 - Conversion of DICOM to NifTI files.
 - Reshaping and resizing of NifTi images.
 - Visualizing of 3D NifTi images
 - Correcting N4 Bias in NifTi files
 - Extracting brain from NifTi files


## Environment Setup
The requirements for `mri-toolbox` can be installed with the command `pip3 install -r requirements.txt`. However, it is recommended to use Conda or Virtualenv environment managers to avoid conflicts with your local environment.
### Conda:
Python 3.10 is recommended, hence create Python 3.10 Conda environment.
- Create new conda environment:

    ```bash
    conda create -n mri-toolbox python=3.10
    ```

- Activate the new conda environment:

    ```bash
    conda activate mri-toolbox
    ```

- Install all dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```

### VirtualEnv:
Python 3.10 is recommended. Compatibility with older versions is not guaranteed.
- Create new VirtualEnv:

    ```bash
    python3 -m venv mri-toolbox
    ```

- Activate `mri-toolbox` virtual environment:

    ```bash
    source mri-toolbox/bin/activate
    ```

- Install all dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```

## CLI interface

The module contains 2 CLI scripts for handling DICOM and NifTi files.

### `dicom_to_nifti.py`:
This script is a simple command-line interface to convert DICOM files to NifTi format.

```bash
usage: dicom_to_nifti.py [-h] -i INPUT_DIR -o OUTPUT_DIR [-c] [-r] [-d]
```

#### Options:
 - `-i`, `--input-dir`: Path to a directory with DICOM files to be converted to NifTi format. (required)
 - `-o`, `--output-dir`: Path to the directory for output NifTi files. (required)
 - `-c`, `--compress`: Compress NifTi files as .gz. (optional)
 - `-r`, `--reorient`: Reorient scans into LAS coordination system. (optional)
 - `-d`, `--debug`: Toggle INFO logging level instead of WARNING. (optional)
#### Example:
```bash
python3 dicom_to_nifti_converter.py -i /path/to/dicoms -o /path/to/output -c -r -d
```
This will convert the DICOM files found in `/path/to/dicoms` to NifTi files, saving them in `/path/to/output`, with the files being compressed and reoriented, and with toggled debug output (INFO logging level).

### `nifti_tools.py`:
A simple command-line interface to process and visualize MRI scans in NifTi format.
```bash
usage: nifti_tools.py [-h] [-i INPUT] [-o OUTPUT] [-s SHAPE [SHAPE ...]] [-v {3D,slices}] [-c [CORRECTION]] [-b [BRAIN]] [-d]
```
#### Options:
 - `-i`, `--input`: Path to a NifTi file to be processed. (required)
 - `-o`, `--output`: Path to save the resulting NifTi file. (optional, but either this or visualization must be specified)
 - `-s`, `--shape`: Resize NifTi files to a specified shape. Provide either 1 integer (for a cube) or 3 integers to specify the shape fully. (optional)
 - `-v`, `--visualize`: Visualize the MRI scan after all selected processes are finished. Could visualize as a simple 3D object or interactively sliced 3D object. Choices: ["3D", "slices"]. (optional, but either this or output must be specified)
 - `-c`, `--correction`: Perform N4 correction. An optional argument specifies the shrink factor to scale the image when computing N4 bias to speed up (default=1). (optional)
 - `-b`, `--brain`: Extract brain from MRI image. An optional argument specifies the number of iterations in approximating brain mask (default=1000). (optional)
 - `-d`, `--debug`: Toggle INFO logging level instead of WARNING. (optional)
#### Example:
```bash
`python3 mri_toolbox.py -i /path/to/input.nii -o /path/to/output.nii -s 256 256 256 -v slices -c 2 -b 500 -d
```

This will process the NifTi file `/path/to/input.nii` - resizing it to a (256, 256, 256) shape, performing N4 correction with a shrink factor of 2, extracting the brain with 500 iterations, and visualizing the result as sliced 3D object. The processed image is saved in `/path/to/output.nii`, and with toggled debug output (INFO logging level).
