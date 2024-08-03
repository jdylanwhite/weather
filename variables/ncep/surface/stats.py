"""Methods for analyzing statistics of variables."""

# Import modules
from typing import List
import xarray


def merge_datasets(dataset_list: List[xarray.Dataset]):
    """Merge multiple datasets with overlapping dimensions.

    Args:
        dataset_list (list): a list of xarray.Dataset objects to merge.

    Returns:
        xarray.Dataset: the merged dataset object containing all variables.
    """
    return xarray.merge(dataset_list)


class VariableDataset:
    """Class for calculating statistics of a meteorological variable."""

    def __init__(self, dataset: xarray.Dataset):
        """Initialize the VariableDataset class.

        Args:
            dataset (xarray.Dataset): the dataset on which to calculate
                statistics.
        """
        # Set base class properties
        self.dataset = dataset

    def interpolate_dataset_to_lat_lon(self, lon: float, lat: float) -> xarray.Dataset:
        """Interpolate to a new geographic coordinate on a gridded dataset.

        Args:
            lon (float): the longitude to interpolate to from the gridded
                dataset.
            lat (float): the latitude to interpolate to from the gridded
                dataset.

        Returns:
            xarray.Dataset: the variable dataset interpolated to the input
                latitude and longitude.

        TODO Test if function works across periodic boundaries.
        """
        # Interpolate the dataset
        interpolated_dataset = self.dataset.interp(lon=lon, lat=lat)

        return interpolated_dataset

    def flip_longitude(self):
        """Convert 0-360 degree longitude to -180 to 180 degree longitude."""
        # Convert from 0 to 360 to -180 to 180 and sort ascending
        self.dataset.coords["lon"] = (self.dataset.coords["lon"] + 180) % 360 - 180
        self.dataset = self.dataset.sortby(self.dataset.lon)

    def time_average(self, var_name: str) -> xarray.DataArray:
        """Average over all times in the dataset.

        Args:
            var_name (str): the name of the variable in the dataset to average.

        Returns:
            xarray.DataArray: the dataset variable averaged over all times.
        """
        return self.dataset[var_name].mean(dim="time")

    def global_average(self, var_name: str) -> xarray.DataArray:
        """Average over all latitudes and longitudes in the dataset.
        Args:
            var_name (str): the name of the variable in the dataset to average.

        Returns:
            xarray.DataArray: the dataset variable averaged over all
                latitudes and longitudes.
        """
        return self.dataset[var_name].mean(dim=["lon", "lat"])
