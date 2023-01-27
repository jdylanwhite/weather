# J. Dylan White
# Convert monthly average meteorological values to grid

# Import modules
import xarray
import pandas as pd
import geopandas as gpd
import grid
import matplotlib.pyplot as plt

def read_dataset(filePath="./data/meteorological/air.mon.mean.nc"):
    """Read the dataset from the filepath using xarray."""
    
    # Open the dataset with xarray
    ds = xarray.open_dataset(filePath)

    return ds

def convert_celsius_to_fahrenheit(ds,var='air'):
    """Convert the dataset variable from degrees Celsius to Fahrenheit.

    ds is the dataset.
    var is the variable containing temperatures in degrees Celsius.
    """
    
    # Convert temperatures from degrees C to F
    ds[var] = 1.8*ds[var]+32

    return ds

def calculate_windspeed(dsU,dsV,uVar="uwnd",vVar="vwnd",speedVar="wind"):

      # Calculate the square root of the sum of squares
      arrWind = np.sqrt(dsU[uVar]**2+dsV[vVar]**2)

      # Construct dataset from resulting array
      dsWind = xarray.Dataset({speedVar:arrWind})

      return dsWind

def flip_longitudes(ds,lonDim="lon"):
    """Flip the longitudes from 0:360 to -180:180.

    ds is the dataset.
    lonDim is the dimension containing longitudes."""
    
    # Convert the longitude from 0 to 360 degrees to -180 to 180
    ds.coords[lonDim] = (ds.coords[lonDim] + 180) % 360 - 180

    # Sort by longitudes to rearrage
    ds = ds.sortby(ds.lon)

    return ds

def last_year_data(ds,nYear=1):
    """Read dataset, adjust coordinates, and select last 12 months of data.

    filePath is the location fo the netCDF file.
    This assumes dimensions are lon, lat, and time."""

    # Subset the time dimension to the last 10 years, or 120 months
    ds = ds.sel(time=ds['time'][-12*nYear:])

    return ds

def monthly_means(ds,varName):
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

def merge_data_to_grid(ds,gridPath="./data/shapefiles/grid_2.5.shp"):

    # Convert the dataset to a dataframe
    df = ds.to_dataframe().reset_index()

    # Read in the grid index from shapefile
    gdfGrid = gpd.read_file("./data/shapefiles/grid_2.5.shp")

    # Specific the grid index 
    gdfGrid['grid_id'] = gdfGrid.index

    # Merge the grid with the dataframe
    dfGrid = pd.merge(df,gdfGrid,
                      left_on=['lat','lon'],
                      right_on=['centerLat','centerLon'],
                      how='inner')

    return dfGrid

def get_data_from_grid(dfGrid,columns,gridList,timeDim="month"):

    # Get only the columns with those grids
    dfGridData = dfGrid.loc[dfGrid['grid_id'].isin(gridList)] 

    # Fetch the information for just that city
    aggDict = {column:"mean" for column in columns}
    dfGridData = dfGridData.groupby(timeDim).agg(aggDict).reset_index()

    return dfGridData
