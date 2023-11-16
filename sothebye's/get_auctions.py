import sys, os, pdb, numpy as np, pandas as pd, regex as re, requests, datetime as dt, json
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
from time import sleep
import numpy as np
from datetime import datetime
import pandas as pd

href_list = []

for page in range(50):
    def getProxies(script_path = None, certificate = None):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.8',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        proxies={
            "http": "http://5af337078fb54f63bceba44b0eba7ec4:@proxy.crawlera.com:8011/",
            "https": "http://5af337078fb54f63bceba44b0eba7ec4:@proxy.crawlera.com:8011/",
        }
        if( certificate is None ): certificate = _findCertificates( script_path )

        return( {'headers': headers, 'proxies': proxies, 'verify': certificate})

    def _findCertificates(script_path):
        #set environment in a manner compatible with both local execution and execution on databricks
        if( "DATABRICKS_RUNTIME_VERSION" in os.environ ):
            path_prefix = '/Workspace'
        else:
            path_prefix = ''
        
        certPath = None
        for this_basePath in script_path.resolve().parents:
            
            this_certPath  = Path(path_prefix + str(this_basePath) + 'sotheby/zyte-smartproxy-ca.crt')
            if( this_certPath.exists() ):
                certPath = str(this_certPath)
                break
        if( certPath is None ):
            print ('  >> Unable to find Zyte Smartproxy SSL certificates.')
            exit(1)
        return( certPath )

    auction_url = 'https://www.sothebys.com/en/results?locale=en'

    params = {
        'from': '',
        'to': '',
        'q': '',
        'p': page,
        '_requestType': 'ajax',
    }

    response = requests.get(
        auction_url,
        proxies={
            "http": "http://5af337078fb54f63bceba44b0eba7ec4:@proxy.crawlera.com:8011/",
            "https": "http://5af337078fb54f63bceba44b0eba7ec4:@proxy.crawlera.com:8011/",
        },
        verify='zyte-ca.crt' ,params=params
    )
    # print(response.text)
    # file_path = "response.txt"
    # # Open the file in write mode ('w')
    # with open(file_path, 'w', encoding='utf-8') as file:
    #     # Step 2: Write the response to the file
    #     file.write(response.text)

    # The file is automatically closed when the 'with' block is exited

    print("Response written to the file.")

    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all anchor tags (<a>)
    anchor_tags = soup.find_all('a')

    # Extract href attributes from anchor tags
    href_attributes = [tag.get('href') for tag in anchor_tags]

    
    # Print the extracted href attributes
    for hyperlink in href_attributes:
        href_list.append(hyperlink)
    # print(hyperlink)


unique_list = np.unique(href_list)

# Using list comprehension
selected_strings = [s for s in unique_list if s.startswith("https://www.sothebys.com")]

#Remove specific string
strings_to_remove = ["https://www.sothebys.com/en/results?locale=en&p=2", "https://www.sothebys.com/api/auth0login?lang=en"]

for item in strings_to_remove:
    if item in selected_strings:
        selected_strings.remove(item)

# Using list comprehension to filter out elements containing "https://www.sothebys.com/en/results?locale"
clean_data = [item for item in selected_strings if "https://www.sothebys.com/en/results?locale" not in item] 

print(clean_data)  

print(len(clean_data))

# Create a Pandas DataFrame from the list
df = pd.DataFrame(clean_data, columns=["AUCTION_URL"])

# print(df)
df.to_csv("current_auctions.csv", index=False)

# Replace 'your_file.csv' with the actual file path
file_path = 'current_auctions.csv'

# Read the CSV file into a Pandas DataFrame
past_auctions = pd.read_csv(file_path)

file_path_2 = 'in_house_auctions.csv'

acquired_auctions = pd.read_csv(file_path_2)

# # Merge DataFrames A and B using outer join and indicator=True
# merged = past_auctions.merge(acquired_auctions, on=['AUCTION_URL', 'AUCTION_URL'], how='outer', indicator=True)

# # Filter the merged DataFrame to get elements that are not in both A and B
# # same = merged[merged['AUCTION_URL'] == 'both']

# df = pd.DataFrame(merged, columns=["AUCTION_URL",])
# Concatenate the data frames
concatenated_df = pd.concat([past_auctions, acquired_auctions])

# Drop duplicates, keeping the first occurrence
df = concatenated_df.drop_duplicates(keep=False)

# print(df)
df.to_csv("foreign_auctions.csv", index=False)

