# Import modules
import os
import urllib.request
from bs4 import BeautifulSoup
import requests

#===============================================================================
# Data download functions
#===============================================================================

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

if __name__ == "__main__":

    # Set the data directory
    dataDir = './data/'

    # Download the monthly OLR data
    download_monthly_file(dataDir) 
