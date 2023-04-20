# J. Dylan White
# Convert monthly average meteorological values to grid

# Import modules
import xarray
import pandas as pd
import geopandas as gpd
import grid
import matplotlib.pyplot as plt
import urllib.request

class download:

    def __init__(self,dataDir):
        """Initialize the download class"""
              
        # Specify the directory to download data
        self.dataDir = dataDir

        # Specify the list of variables to download
        self.varList = [
            "air",        # air temperature
            "pres.sfc",   # surface pressure
            "uwnd",       # zonal wind
            "vwnd",       # meridional wind
            "wspd",       # wind speed
            "rhum"        # relative humidity
        ]


    def download_surface_variable(self,var):

        # Build the file path
        filePath = f"{self.dataDir}/{var}.mon.mean.nc"
    
        # Build the file URL
        baseUrl = "https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis.derived/surface"
        fileUrl = f"{baseUrl}/{var}.mon.mean.nc"

        # Download the file
        urllib.request.urlretrieve(fileUrl, filePath)

        return filePath


    def download_all_surface_variables(self):

        # Initiate dictionary
        filePathDict = {}
    
        # Loop through the variables
        for var in self.varList:

            # Download the variables
            filePathDict[var] = self.download_surface_variable(var)

        return filePathDict

class data():

    def __init__(self,dataDir):
        """Initialize the data class"""
    
        # Specify the directory where data is stored
        self.dataDir = dataDir

        # Specify the list of variables
        self.varList = [
            "air",        # air temperature
            "pres.sfc",   # surface pressure
            "uwnd",       # zonal wind
            "vwnd",       # meridional wind
            "wspd",       # wind speed
            "rhum"        # relative humidity
        ]


    def read_dataset(self,var):
        """Read the dataset from the filepath using xarray."""

        filePath = f"{self.dataDir}/{var}.mon.mean.nc"
        
        # Open the dataset with xarray
        ds = xarray.open_dataset(filePath)

        return ds


    def convert_celsius_to_fahrenheit(self,ds,var='air'):
        """Convert the dataset variable from degrees Celsius to Fahrenheit.

        ds is the dataset.
        var is the variable containing temperatures in degrees Celsius.
        """
    
        # Convert temperatures from degrees C to F
        ds[var] = 1.8*ds[var]+32

        return ds


    # def calculate_windspeed(dsU,dsV,uVar="uwnd",vVar="vwnd",speedVar="wind"):
    #     """Calculate the horizontal wind speed from the components"""
        
    #     # Calculate the square root of the sum of squares
    #     arrWind = np.sqrt(dsU[uVar]**2+dsV[vVar]**2)

    #     # Construct dataset from resulting array
    #     dsWind = xarray.Dataset({speedVar:arrWind})

    #     return dsWind

  
    def flip_longitudes(self,ds,lonDim="lon"):
        """Flip the longitudes from 0:360 to -180:180.
        
        ds is the dataset.
        lonDim is the dimension containing longitudes."""
    
        # Convert the longitude from 0 to 360 degrees to -180 to 180
        ds.coords[lonDim] = (ds.coords[lonDim] + 180) % 360 - 180

        # Sort by longitudes to rearrage
        ds = ds.sortby(ds.lon)
    
        return ds

    
    def prepare_data(self,var,convertCelsius=True):

        # Read the dataset
        ds = self.read_dataset(var)

        # Convert degrees Celsius to Fahrenheit
        if var == "air" and convertCelsius:
            ds = self.convert_celsius_to_fahrenheit(ds)

        # Flip longitudes
        ds = self.flip_longitudes(ds)

        return ds


    def last_year_data(self,ds,nYear=1):
        """Read dataset, adjust coordinates, and select last 12 months of data.
        
        filePath is the location fo the netCDF file.
        This assumes dimensions are lon, lat, and time."""

        # Subset the time dimension to the last 10 years, or 120 months
        ds = ds.sel(time=ds['time'][-12*nYear:])

        return ds


    def monthly_means(self,ds,varName):
        """Read dataset, adjust coordinates, and return monthly means/stddevs

        filePath is the path to the netCDF file.
        nYears is the number of years used to aggregate each monthly average.
        Assumes dimensions are lon, lat, time."""

        # Now groupby and aggregate the months by averaging
        # and getting the standard deviation
        dsMonthlyAgg = ds.groupby('time.month').mean('time')
        dsMonthlyAgg = dsMonthlyAgg.rename({varName:varName+'_avg'})
        dsMonthlyAgg[varName+'_std'] = ds[varName].groupby('time.month').std('time')

        return dsMonthlyAgg

               
    def merge_data_to_grid(self,ds,gridPath="./data/shapefiles/grid_2.5.shp"):

        # Convert the dataset to a dataframe
        df = ds.to_dataframe().reset_index()

        # Read in the grid index from shapefile
        gdfGrid = gpd.read_file(gridPath)

        # Specific the grid index 
        gdfGrid['grid_id'] = gdfGrid.index

        # Merge the grid with the dataframe
        dfGrid = pd.merge(df,gdfGrid,
                          left_on=['lat','lon'],
                          right_on=['centerLat','centerLon'],
                          how='inner')

        return dfGrid


    def get_city_data_from_grid(self,dfGrid,columns,city,country,timeDim="month"):

        # Get the grid IDs for the city
        gridList = grid.find_city_name_grids(city,country)

        # Get only the columns with those grids
        dfGridData = dfGrid.loc[dfGrid['grid_id'].isin(gridList)] 

        # Fetch the information for just that city
        aggDict = {column:"mean" for column in columns}
        dfGridData = dfGridData.groupby(timeDim).agg(aggDict).reset_index()

        return dfGridData


class plot():

    def __init__(self,imageDir):

        # Specify the directory to save images to
        self.imageDir = imageDir

        # Specify the variables and the colors to associate with each color
        self.varDict = {
            "air": "blue",         # air temperature
            "pres.sfc": "black",   # surface pressure
            "uwnd": "green",       # zonal wind
            "vwnd": "orange",      # meridional wind
            "wspd": "red",         # wind speed
            "rhum": "purple"       # relative humidity
        }

    def plot_past_year(self,var,dfGrid):

        # # Limit data to just the last year
        # dsLastYearWind = self.last_year_data(dsWind)

        # # Merge the data to the grid
        # dfLastYearGridWind = variables.merge_data_to_grid(dsLastYearWind)

        # # Get data from the grid
        # gridIdList = grid.find_city_name_grids("Berlin","Germany")
        # dfLastYearBerlinWind = variables.get_data_from_grid(dfLastYearGridWind,['wind'],gridIdList,"time")

        # Get the data to plot
        x = dfLastYearBerlinWind['time'].to_list()
        y = dfLastYearBerlinWind['wind'].to_list()

        # Create plot
        fig, ax = plt.subplots(figsize=(5,5))
        ax.plot(x,y,color="black")

        # Save plot
        figFile = "./images/Berlin_mean_windspeed_last_year.png"
        fig.savefig(figFile)
        figFile

if __name__ == "__main__":

    # Download data
    # varDownload = download("./data/meteorological")
    # varDownload.download_all_surface_variables()

    # Set parameters
    var = "air"
    city = "Berlin"
    country = "Germany"

    # Read data
    varData = data("./data/meteorological")
    ds = varData.prepare_data("air")

    # Get last year's data and get the city's data from the grid
    dsLastYear = varData.last_year_data(ds)
    dfGridLastYear = varData.merge_data_to_grid(ds,"./shp/shapefiles/grid_2.5.shp")
    dfBerlinLastYear = varData.get_city_data_from_grid(dfGridLastYear,[var],city,country,timeDim="month")

    print("Done!")