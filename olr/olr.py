# Import modules
import os
import urllib.request
from bs4 import BeautifulSoup
import requests

def get_monthly_file_path():

    """Since the monthly averages file is overwritten with a new name
    each month, we need a way to extract the file directly"""

    # Set the directory to search in
    baseUrl =  "https://www.ncei.noaa.gov/data/"+\
               "outgoing-longwave-radiation-monthly/access/"

    # Set the file extension
    ext = ".nc"

    # Get the data from the baseUrl
    page = requests.get(baseUrl).text

    # Parse the page results
    soup = BeautifulSoup(page, 'html.parser')

    # Find all of the hyperlinked anchors on the page
    fileList = [node.get('href') for node in soup.find_all('a')
                if node.get('href').endswith(ext)]

    return baseUrl+fileList[0]

def download_monthly_file(dataDir):

    """Retrieve the monthly OLR file and download it if it doesn't
    already exist"""

    # Set the URL of the data to download
    dataUrl = get_monthly_file_path()
           
    # Grab the file name
    fileName = os.path.basename(dataUrl)
    filePath = os.path.join(dataDir,fileName)

    # Check if the file exists, and if it doesn't, download it
    if not os.path.exists(filePath):
        urllib.request.urlretrieve(dataUrl,filePath)

def get_daily_file_paths(yearList):

    """Find the files, separated by year, for daily OLR data."""

    # Set the base URL for the directory to parse files
    baseUrl = "https://www.ncei.noaa.gov/data/"+\
              "outgoing-longwave-radiation-daily/access/"

    # Set the file extension to find
    ext = ".nc"

    # Get the data from the base URL
    page = requests.get(baseUrl).text

    # Parse the page results
    soup = BeautifulSoup(page, 'html.parser')

    # Find all of the hyperlinked anchors on the page
    fileList = [node.get('href') for node in soup.find_all('a')
                if node.get('href').endswith(ext)]

    # Create an empty list
    fileListSubset = []

    # Find the file names that are within the date range
    for year in yearList:

        # Set the strings to match
        dateString = f'{year}0101_{year}'

        # Find the file that matches the year
        fileListSubset.append([baseUrl+fileName for fileName in fileList 
                               if dateString in fileName][0])

    return fileListSubset
      

def download_daily_files(dataDir,yearList):

    # Get the list of URLs
    dataUrlList = get_daily_file_paths(yearList)

    # Loop through the URLs
    for dataUrl in dataUrlList:
    
        # Grab the file name
        fileName = os.path.basename(dataUrl)
        filePath = os.path.join(dataDir,fileName)

        # Check if the file exists, and if it doesn't, download it
        if not os.path.exists(filePath):
            urllib.request.urlretrieve(dataUrl,filePath)


if __name__ == "__main__":

    # Set the data directory
    dataDir = './data/'

    # Download the monthly OLR data
    download_monthly_file(dataDir) 

    # Set the range of years to download daily data
    beginYear = 2017
    endYear = 2021
    yearList = [year for year in range(beginYear,endYear+1)]

    # Download the daily OLR data
    download_daily_files(dataDir,yearList)
