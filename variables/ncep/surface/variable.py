"""Download NCEP surface variables."""

# TODO Combine several datasets with matching dimensions.
# TODO Combine all datasets with matching dimensions.
# TODO Combine zonal and meridional wind into windspeed

# Import modules
import os
import urllib.request
import xarray


class BaseVariable:
    """Base class for NCEP surface variable classes."""

    # TODO Add check for existing NCEP surface variables
    # TODO Raise error if var_name is not an existing variables
    # TODO Check if there is a newer version of data to be downloaded
    # TODO Add global averaging function
    # TODO Add temporal averaging function
    # TODO Add temporal averaging function over past N years
    # TODO Add plotting for variables
    
    def __init__(self, var_name: str, data_dir: str):
        """Initialize the base variable class.

        Args:
            var_name (str): the name of the surface variable to download.
            data_dir (str): path to directory for downloading and reading data
        """
        # Set base class properties
        self.data_dir = data_dir
        self.var_name = var_name
        self.base_url = (
            "https://downloads.psl.noaa.gov/Datasets/"
            + "ncep.reanalysis.derived/surface"
        )

    def download_data(self) -> str:
        """Download the NCEP surface level variable.

        Returns:
            str: the output path of the downloaded file.
        """
        # Build the file path
        download_path = os.path.join(self.data_dir, f"{self.var_name}.mon.mean.nc")

        # Build the file URL
        file_url = f"{self.base_url}/{self.var_name}.mon.mean.nc"

        # Download the file
        urllib.request.urlretrieve(file_url, download_path)

        return download_path

    def read_dataset(self) -> xarray.Dataset:
        """Read the dataset from the file path using xarray.

        Returns:
            xarray.Dataset: the dataset for the variable.
        """
        # Set the file path to open
        dataset_path = f"{self.data_dir}/{self.var_name}.mon.mean.nc"

        # Open the dataset with xarray
        dataset = xarray.open_dataset(dataset_path)
        self.dataset = dataset

        return dataset


class ZonalWind(BaseVariable):
    """Zonal wind NCEP surface variable class."""

    def __init__(self, data_dir: str):
        """Initialize the zonal wind variable class.

        Args:
            data_dir (str): path to directory for downloading and reading data
        """
        # Set class properties
        self.var_name = "uwnd"
        self.data_dir = data_dir
        super().__init__(var_name=self.var_name, data_dir=self.data_dir)


class MeridionalWind(BaseVariable):
    """Meridional wind NCEP surface variable class."""

    def __init__(self, data_dir: str):
        """Initialize the meridional wind variable class.

        Args:
            data_dir (str): path to directory for downloading and reading data
        """
        # Set class properties
        self.var_name = "vwnd"
        self.data_dir = data_dir
        super().__init__(var_name=self.var_name, data_dir=self.data_dir)


class VerticalWind(BaseVariable):
    """Vertical wind NCEP surface variable class."""

    def __init__(self, data_dir: str):
        """Initialize the vertical wind, omega, variable class.

        Args:
            data_dir (str): path to directory for downloading and reading data
        """
        # Set class properties
        self.var_name = "omega.sig995"
        self.data_dir = data_dir
        super().__init__(var_name=self.var_name, data_dir=self.data_dir)


class SeaLevelPressure(BaseVariable):
    """Sea level pressure NCEP surface variable class."""

    def __init__(self, data_dir: str):
        """Initialize the sea level pressure variable class.

        Args:
            data_dir (str): path to directory for downloading and reading data
        """
        # Set class properties
        self.var_name = "slp"
        self.data_dir = data_dir
        super().__init__(var_name=self.var_name, data_dir=self.data_dir)


class RelativeHumidity(BaseVariable):
    """Relative humidity NCEP surface variable class."""

    def __init__(self, data_dir: str):
        """Initialize the relative humidity variable class.

        Args:
            data_dir (str): path to directory for downloading and reading data
        """
        # Set class properties
        self.var_name = "rhum"
        self.data_dir = data_dir
        super().__init__(var_name=self.var_name, data_dir=self.data_dir)


class PrecipitableWater(BaseVariable):
    """Precipital water NCEP surface variable class."""

    def __init__(self, data_dir: str):
        """Initialize the percipitable water variable class.

        Args:
            data_dir (str): path to directory for downloading and reading data
        """
        # Set class properties
        self.var_name = "pr_wtr"
        self.data_dir = data_dir
        super().__init__(var_name=self.var_name, data_dir=self.data_dir)


class Pressure(BaseVariable):
    """Surface pressure NCEP variable class."""

    def __init__(self, data_dir: str):
        """Initialize the pressure variable class.

        Args:
            data_dir (str): path to directory for downloading and reading data
        """
        # Set class properties
        self.var_name = "pres"
        self.data_dir = data_dir
        super().__init__(var_name=self.var_name, data_dir=self.data_dir)


class PotentialTemperature(BaseVariable):
    """Potential temperature NCEP surface variable class."""

    def __init__(self, data_dir: str):
        """Initialize the potential temperature variable class.

        Args:
            data_dir (str): path to directory for downloading and reading data
        """
        # Set class properties
        self.var_name = "pottmp.sig995"
        self.data_dir = data_dir
        super().__init__(var_name=self.var_name, data_dir=self.data_dir)


class Temperature(BaseVariable):
    """Temperature NCEP surface variable class."""

    # TODO Convert from K to degrees F or C

    def __init__(self, data_dir: str):
        """Initialize the vertical wind, omega, variable class.

        Args:
            data_dir (str): path to directory for downloading and reading data
        """
        # Set class properties
        self.var_name = "air"
        self.data_dir = data_dir
        super().__init__(var_name=self.var_name, data_dir=self.data_dir)


if __name__ == "__main__":

    # Download all of the data
    download_dir = "./data"
    uwnd_var = ZonalWind(download_dir)
    uwnd_var.download_data()
    vwnd_var = MeridionalWind(download_dir)
    vwnd_var.download_data()
    omega_var = VerticalWind(download_dir)
    omega_var.download_data()
    slp_var = SeaLevelPressure(download_dir)
    slp_var.download_data()
    rhum_var = RelativeHumidity(download_dir)
    rhum_var.download_data()
    pwat_var = PrecipitableWater(download_dir)
    pwat_var.download_data()
    pres_var = Pressure(download_dir)
    pres_var.download_data()
    pot_temp_var = PotentialTemperature(download_dir)
    pot_temp_var.download_data()
    temp_var = Temperature(download_dir)
    temp_var.download_data()
