"""
This module implements visualization tools for mri scans

Author: Michal Glos (michal.glos99@gmail.com)
"""

import pyvista as pv
import nibabel as nib
from functools import partial

import numpy as np


def plot_3d_object(data):
    """
    Plot simply a 3D object in pyvista UnifromGrid

    Parameters:
        data (np.array): 3D numpy array to be plotted
    """
    grid = pv.UniformGrid()
    grid.dimensions = data.shape
    grid.point_data["values"] = data.flatten(order="F")
    plotter = pv.Plotter()
    plotter.add_volume(grid)
    plotter.show()
    plotter.close()


class MRIVizSlicer:
    """Class providing data visualization, encapsulating the plotter state and methods"""

    def __init__(self, data):
        # Save data and default slice
        self.data = data
        self.data_slice = [1 for dim in data.shape]

        # Instantiate the grid
        self.grid = pv.UniformGrid()
        self.grid.dimensions = data.shape
        self.grid.point_data["values"] = data.flatten(order="F")
        self.slice_object = self.grid.slice_orthogonal(*self.data_slice)

        # Init plotter and widgets
        self.plotter = pv.Plotter()
        self.plotter.add_mesh(self.slice_object, show_scalar_bar=False)

        # Add axis X slider widget
        self.plotter.add_slider_widget(
            callback=partial(self.reslice, dimension=0),
            rng=[0.0, self.data.shape[0] - 1],
            value=1,
            title="X",
            pointa=(0.025, 0.1),
            pointb=(0.31, 0.1),
            style="modern",
        )
        # Add axis Y slider widget
        self.plotter.add_slider_widget(
            callback=partial(self.reslice, dimension=1),
            rng=[0.0, self.data.shape[1] - 1],
            value=1,
            title="Y",
            pointa=(0.35, 0.1),
            pointb=(0.64, 0.1),
            style="modern",
        )
        # Add axis Z slider widget
        self.plotter.add_slider_widget(
            callback=partial(self.reslice, dimension=2),
            rng=[0.0, self.data.shape[2] - 1],
            value=1,
            title="Z",
            pointa=(0.67, 0.1),
            pointb=(0.98, 0.1),
            style="modern",
        )
        self.plotter.add_axes(viewport=(0.0, 0.8, 0.2, 1))

    def reslice(self, value, dimension=0):
        """
        Update a plotter slice

        Parameters:
            value (int): New coordinates for slicing the object
            dimension (int): Specify the dimension to slice
        """
        # Specify the new position of slice
        self.data_slice[dimension] = value
        # Setup the normal vector to the and position of the slice surface
        normal = np.zeros(3)
        normal[dimension] = 1
        origin = np.zeros(3)
        origin[dimension] = value
        # Perform the slicing and update the plotted grid
        new_slice = self.grid.slice(normal=normal, origin=origin)
        self.slice_object.get(dimension).copy_from(new_slice)

    def show(self):
        """Show the plot, close it evantually"""
        self.plotter.show()
        self.plotter.close()

