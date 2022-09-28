import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon

def read_cities_shp(shpdir="./data/shapefiles/"):

    """
    Read the shapefile for cities, and only keep certain columns.
    """

    # Read the cities shapefile
    gdfCities = gpd.read_file(shpdir+"World_Cities.shp")

    # Limit the columns to what we need
    keepColumns = ["CITY_NAME","CNTRY_NAME","geometry"]
    gdfCities = gdfCities.loc[:,keepColumns]

    return gdfCities

def read_countries_shp(shpdir="./data/shapefiles/"):

    """
    Read the shapefile for countries, and only keep certain columns.
    """

    # Read the countries shapefile
    gdfCountries = gpd.read_file(shpdir+"World_Countries__Generalized_.shp")

    # Limit the columns to what we need
    keepColumns = ["COUNTRY","geometry"]
    gdfCountries = gdfCountries.loc[:,keepColumns]

    return gdfCountries

def construct_grid_arrays(gridspacing=2.5):

    """
    Using a given gridspacing, build an evenly spaced
    latitude and longitude array.
    """

    # Build the latitude and longitude array
    latitude = np.arange(-90,90,gridspacing)
    longitude = np.arange(-180,180,gridspacing)

    return longitude, latitude

def construct_grid(shpdir="./data/shapefiles/",gridspacing=2.5):

    """
    Create the grid as a series of square tiles, then write the
    results to a shapefile
    """

    # Construct the lat/lon arrays
    longitude, latitude = construct_grid_arrays(gridspacing)

    # Create each grid cell as a polygon
    polygonList = []
    for lat in latitude:
        for lon in longitude:
            polygonList.append(Polygon([(lon, lat),
                                        (lon+gridspacing, lat),
                                        (lon+gridspacing, lat+gridspacing),
                                        (lon, lat+gridspacing)]))

    # Create the grid geodataframe and send to shapefile
    gdfGrid = gpd.GeoDataFrame({'geometry':polygonList})
    gdfGrid.to_file(shpdir+"grid_"+str(gridspacing)+".shp")

    return gdfGrid

def grid_country_sjoin(idDir="./data/ids/"):

    """
    Use a spatial join to find indices for overlapping grids and countries.
    """

    # Perform spatial join
    gdfIntersectsCountries = gpd.sjoin(gdfGrid,gdfCountries,how="left")

    # Drop NA values, and only keep the index column
    dfIntersectsCountries = gdfIntersectsCountries.dropna()['index_right']

    # Rename column
    dfIntersectsCountries.columns = ['country_id']

    # Send output to CSV
    dfIntersectsCountries.to_csv(idDir+'grid_country_sjoin.csv',index_label="grid_id")

    return dfIntersectsCountries

def grid_city_sjoin(idDir="./data/indices/"):

    """
    Use a spatial join to find indices for overlapping grids and cities.
    """

    # Perform spatial join
    gdfIntersectsCities = gpd.sjoin(gdfGrid,gdfCities,how="left")

    # Drop NA values, and only keep the index column
    dfIntersectsCities = gdfIntersectsCities.dropna()['index_right']

    # Rename column
    dfIntersectsCities.columns = ['city_id']

    # Send output to CSV
    dfIntersectsCities.to_csv(idDir+'grid_city_sjoin.csv',index_label="grid_id")

    return dfIntersectsCities
