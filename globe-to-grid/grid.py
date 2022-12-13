import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon

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
    dfIntersectsCountries = pd.DataFrame({"country_id":dfIntersectsCountries})

    # Send output to CSV
    dfIntersectsCountries.to_csv(idDir+'grid_country_sjoin.csv',index_label="grid_id")

    return dfIntersectsCountries

def grid_city_sjoin(idDir="./data/ids/"):

    """
    Use a spatial join to find indices for overlapping grids and cities.
    """

    # Perform spatial join
    gdfIntersectsCities = gpd.sjoin(gdfGrid,gdfCities,how="left")

    # Drop NA values, and only keep the index column
    dfIntersectsCities = gdfIntersectsCities.dropna()['index_right']

    # Rename column
    dfIntersectsCities = pd.DataFrame({"city_id":dfIntersectsCities})

    # Send output to CSV
    dfIntersectsCities.to_csv(idDir+'grid_city_sjoin.csv',index_label="grid_id")

    return dfIntersectsCities

def find_country_id_grids(countryId,idPath="./data/ids/grid_country_sjoin.csv"):

    """
    Look up which grids contain a specified country index and return them as a list.
    """

    # Read the spatial join CSV
    df = pd.read_csv(idPath)

    # Find the grid IDs for a given country
    gridList = df.loc[df["country_id"]==countryId]['grid_id'].to_list()

    return gridList

def find_city_id_grids(cityId,idPath="./data/ids/grid_city_sjoin.csv"):

    """
    Look up which grids contain a specified city index and return them as a list
    """

    # Read the spatial join CSV
    df = pd.read_csv(idPath)

    # Find the grid IDs for a given country
    gridList = df.loc[df["city_id"]==cityId]['grid_id'].to_list()

    return gridList

def find_country_name_grids(country,shpDir="./data/shapefiles/",idPath="./data/ids/grid_country_sjoin.csv"):

    """
    Look up which grids contain a specified country and return them as a list.
    """

    # Read the countries shapefile
    gdfCountries = read_countries_shp(shpDir)

    # Get the ID of the given country
    countryId = gdfCountries.index[gdfCountries['COUNTRY'] == country].tolist()[0]

    # Find the country grid cells by ID
    countryGridList = find_country_id_grids(countryId)

    return countryGridList

def find_city_name_grids(city,country,shpDir="./data/shapefiles/",idPath="./data/ids/grid_city_sjoin.csv"):

    """
    Look up which grids contain a specified city and country and return them as a list.
    """

    # Read the countries shapefile
    gdfCities = read_cities_shp(shpDir)

    # Get the ID of the given country
    cityId = gdfCities.index[(gdfCities["CITY_NAME"] == city) & (gdfCities['CNTRY_NAME'] == country)]
    cityId = cityId.tolist()[0]

    # Find the country grid cells by ID
    cityGridList = find_city_id_grids(cityId)

    return cityGridList

def find_point_grids(lon,lat,shpdir="./data/shapefiles/",gridspacing=2.5):

    """
    Look up which grid cell contains a specified latitude and longitude.
    """

    # Read the grid shapefile
    gridPath = shpdir+"grid_"+str(gridspacing)+".shp"
    gdfGrid = gpd.read_file(gridPath)

    # Create point geometry
    point = Point(lon,lat)
    gdfPoint = gpd.GeoDataFrame({"geometry":[point]})

    # Get the point grid intersection
    gdfIntersection = gpd.sjoin(gdfGrid,gdfPoint,how="right")

    # Find the grid that matches the intersection
    gridId = gdfIntersection["index_left"].to_list()[0]

    return gridId
