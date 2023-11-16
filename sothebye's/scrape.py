# Databricks notebook source
import sys, os, pdb, numpy as np, pandas as pd, regex as re, requests, datetime as dt, json
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
from time import sleep
from datetime import datetime

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

df = pd.read_csv('foreign_auctions.csv')

value_list = []
# Loop through the DataFrame using iterrows()
for auction_url in df['AUCTION_URL'].tolist():
    try:
        # auction_id = '1e6ffa2c-b7a1-41a6-ac81-6481e08ed53e'
        response = requests.get(
            auction_url,
            proxies={
                "http": "http://5af337078fb54f63bceba44b0eba7ec4:@proxy.crawlera.com:8011/",
                "https": "http://5af337078fb54f63bceba44b0eba7ec4:@proxy.crawlera.com:8011/",
            },
            verify='zyte-ca.crt' 
        )
        # print(response.text)

        soup = BeautifulSoup(response.content, "html.parser")
        auction_id = json.loads(soup.find_all(string=re.compile('auctionId'))[0])['props']['pageProps']['algoliaJson']['hits'][0]['auctionId']
        print(auction_id)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'x-algolia-api-key': 'NWJkNGI1NzQ4ZTQ4YWMyN2MzZWE2ODczNjEyNDA4NDljZWU5NmU0Zjk2MjUwMzFjMTcxNDZiN2QzOWI2OGU0ZnZhbGlkVW50aWw9MTY5MTY4ODIxOSZyZXN0cmljdEluZGljZXM9YXVjdGlvbnMlMkNwcm9kX2F1Y3Rpb25zJTJDcHJvZF9hdWN0aW9uc18qJTJDcHJvZF9hdWN0aW9uc19uYW1lX2FzYyUyQ3Byb2RfYXVjdGlvbnNfbmFtZV9kZXNjJTJDcHJvZF9hdWN0aW9uc19zdGFydERhdGVfYXNjJTJDcHJvZF9hdWN0aW9uc19zdGFydERhdGVfZGVzYyUyQ3Byb2RfYXVjdGlvbnNfZW5kRGF0ZV9hc2MlMkNwcm9kX2F1Y3Rpb25zX2VuZERhdGVfZGVzYyUyQ3Byb2RfYXVjdGlvbnNfY2xvc2VEYXRlX2FzYyUyQ3Byb2RfYXVjdGlvbnNfY2xvc2VEYXRlX2Rlc2MlMkNjcmVhdG9ycyUyQ3Byb2RfY3JlYXRvcnMlMkNwcm9kX2NyZWF0b3JzXyolMkNjcmVhdG9yc1YyJTJDcHJvZF9jcmVhdG9yc1YyJTJDcHJvZF9jcmVhdG9yc1YyXyolMkNsb3RzJTJDcHJvZF9sb3RzJTJDcHJvZF9sb3RzXyolMkNwcm9kX3N1Z2dlc3RlZF9sb3RzJTJDcHJvZF9zdWdnZXN0ZWRfbG90c18qJTJDcHJvZF91cGNvbWluZ19sb3RzXyolMkNwcm9kX2Z5ZW9fbG90c18qJTJDbG90c19lbmdsaXNoJTJDcHJvZF9sb3RzX2VuZ2xpc2glMkNwcm9kX2xvdHNfZW5nbGlzaF8qJTJDcHJvZF9sb3RzX2VuZ2xpc2hfbG90TnJfYXNjJTJDcHJvZF9sb3RzX2VuZ2xpc2hfbG90TnJfZGVzYyUyQ3Byb2RfbG90c19lbmdsaXNoX2F1Y3Rpb25EYXRlX2FzYyUyQ3Byb2RfbG90c19lbmdsaXNoX2F1Y3Rpb25EYXRlX2Rlc2MlMkNwcm9kX3VwY29taW5nX2xvdHNfZW5nbGlzaF9hc2MlMkNwcm9kX3VwY29taW5nX2xvdHNfZW5nbGlzaF9kZXNjJTJDcHJvZF9sb3RzX2VuZ2xpc2hfbG93RXN0aW1hdGVfYXNjJTJDcHJvZF9sb3RzX2VuZ2xpc2hfbG93RXN0aW1hdGVfZGVzYyUyQ3Byb2Rfc3VnZ2VzdGVkX2xvdHNfZW5nbGlzaCUyQ3Byb2RfZnllb19sb3RzX2VuZ2xpc2hfYXVjdGlvbkRhdGVfYXNjJTJDcHJvZF9meWVvX2xvdHNfZW5nbGlzaF9hdWN0aW9uRGF0ZV9kZXNjJTJDbG90c19mcmVuY2glMkNwcm9kX2xvdHNfZnJlbmNoJTJDcHJvZF9sb3RzX2ZyZW5jaF8qJTJDcHJvZF9sb3RzX2ZyZW5jaF9sb3ROcl9hc2MlMkNwcm9kX2xvdHNfZnJlbmNoX2xvdE5yX2Rlc2MlMkNwcm9kX2xvdHNfZnJlbmNoX2F1Y3Rpb25EYXRlX2FzYyUyQ3Byb2RfbG90c19mcmVuY2hfYXVjdGlvbkRhdGVfZGVzYyUyQ3Byb2RfdXBjb21pbmdfbG90c19mcmVuY2hfYXNjJTJDcHJvZF91cGNvbWluZ19sb3RzX2ZyZW5jaF9kZXNjJTJDcHJvZF9sb3RzX2ZyZW5jaF9sb3dFc3RpbWF0ZV9hc2MlMkNwcm9kX2xvdHNfZnJlbmNoX2xvd0VzdGltYXRlX2Rlc2MlMkNwcm9kX3N1Z2dlc3RlZF9sb3RzX2ZyZW5jaCUyQ3Byb2RfZnllb19sb3RzX2ZyZW5jaF9hdWN0aW9uRGF0ZV9hc2MlMkNwcm9kX2Z5ZW9fbG90c19mcmVuY2hfYXVjdGlvbkRhdGVfZGVzYyUyQ2xvdHNfZ2VybWFuJTJDcHJvZF9sb3RzX2dlcm1hbiUyQ3Byb2RfbG90c19nZXJtYW5fKiUyQ3Byb2RfbG90c19nZXJtYW5fbG90TnJfYXNjJTJDcHJvZF9sb3RzX2dlcm1hbl9sb3ROcl9kZXNjJTJDcHJvZF9sb3RzX2dlcm1hbl9hdWN0aW9uRGF0ZV9hc2MlMkNwcm9kX2xvdHNfZ2VybWFuX2F1Y3Rpb25EYXRlX2Rlc2MlMkNwcm9kX3VwY29taW5nX2xvdHNfZ2VybWFuX2FzYyUyQ3Byb2RfdXBjb21pbmdfbG90c19nZXJtYW5fZGVzYyUyQ3Byb2RfbG90c19nZXJtYW5fbG93RXN0aW1hdGVfYXNjJTJDcHJvZF9sb3RzX2dlcm1hbl9sb3dFc3RpbWF0ZV9kZXNjJTJDcHJvZF9zdWdnZXN0ZWRfbG90c19nZXJtYW4lMkNwcm9kX2Z5ZW9fbG90c19nZXJtYW5fYXVjdGlvbkRhdGVfYXNjJTJDcHJvZF9meWVvX2xvdHNfZ2VybWFuX2F1Y3Rpb25EYXRlX2Rlc2MlMkNsb3RzX2l0YWxpYW4lMkNwcm9kX2xvdHNfaXRhbGlhbiUyQ3Byb2RfbG90c19pdGFsaWFuXyolMkNwcm9kX2xvdHNfaXRhbGlhbl9sb3ROcl9hc2MlMkNwcm9kX2xvdHNfaXRhbGlhbl9sb3ROcl9kZXNjJTJDcHJvZF9sb3RzX2l0YWxpYW5fYXVjdGlvbkRhdGVfYXNjJTJDcHJvZF9sb3RzX2l0YWxpYW5fYXVjdGlvbkRhdGVfZGVzYyUyQ3Byb2RfdXBjb21pbmdfbG90c19pdGFsaWFuX2FzYyUyQ3Byb2RfdXBjb21pbmdfbG90c19pdGFsaWFuX2Rlc2MlMkNwcm9kX2xvdHNfaXRhbGlhbl9sb3dFc3RpbWF0ZV9hc2MlMkNwcm9kX2xvdHNfaXRhbGlhbl9sb3dFc3RpbWF0ZV9kZXNjJTJDcHJvZF9zdWdnZXN0ZWRfbG90c19pdGFsaWFuJTJDcHJvZF9meWVvX2xvdHNfaXRhbGlhbl9hdWN0aW9uRGF0ZV9hc2MlMkNwcm9kX2Z5ZW9fbG90c19pdGFsaWFuX2F1Y3Rpb25EYXRlX2Rlc2MlMkNsb3RzX2NoaW5lc2VfdHJhZGl0aW9uYWwlMkNwcm9kX2xvdHNfY2hpbmVzZV90cmFkaXRpb25hbCUyQ3Byb2RfbG90c19jaGluZXNlX3RyYWRpdGlvbmFsXyolMkNwcm9kX2xvdHNfY2hpbmVzZV90cmFkaXRpb25hbF9sb3ROcl9hc2MlMkNwcm9kX2xvdHNfY2hpbmVzZV90cmFkaXRpb25hbF9sb3ROcl9kZXNjJTJDcHJvZF9sb3RzX2NoaW5lc2VfdHJhZGl0aW9uYWxfYXVjdGlvbkRhdGVfYXNjJTJDcHJvZF9sb3RzX2NoaW5lc2VfdHJhZGl0aW9uYWxfYXVjdGlvbkRhdGVfZGVzYyUyQ3Byb2RfdXBjb21pbmdfbG90c19jaGluZXNlX3RyYWRpdGlvbmFsX2FzYyUyQ3Byb2RfdXBjb21pbmdfbG90c19jaGluZXNlX3RyYWRpdGlvbmFsX2Rlc2MlMkNwcm9kX2xvdHNfY2hpbmVzZV90cmFkaXRpb25hbF9sb3dFc3RpbWF0ZV9hc2MlMkNwcm9kX2xvdHNfY2hpbmVzZV90cmFkaXRpb25hbF9sb3dFc3RpbWF0ZV9kZXNjJTJDcHJvZF9zdWdnZXN0ZWRfbG90c19jaGluZXNlX3RyYWRpdGlvbmFsJTJDcHJvZF9meWVvX2xvdHNfY2hpbmVzZV90cmFkaXRpb25hbF9hdWN0aW9uRGF0ZV9hc2MlMkNwcm9kX2Z5ZW9fbG90c19jaGluZXNlX3RyYWRpdGlvbmFsX2F1Y3Rpb25EYXRlX2Rlc2MlMkNsb3RzX2NoaW5lc2Vfc2ltcGxpZmllZCUyQ3Byb2RfbG90c19jaGluZXNlX3NpbXBsaWZpZWQlMkNwcm9kX2xvdHNfY2hpbmVzZV9zaW1wbGlmaWVkXyolMkNwcm9kX2xvdHNfY2hpbmVzZV9zaW1wbGlmaWVkX2xvdE5yX2FzYyUyQ3Byb2RfbG90c19jaGluZXNlX3NpbXBsaWZpZWRfbG90TnJfZGVzYyUyQ3Byb2RfbG90c19jaGluZXNlX3NpbXBsaWZpZWRfYXVjdGlvbkRhdGVfYXNjJTJDcHJvZF9sb3RzX2NoaW5lc2Vfc2ltcGxpZmllZF9hdWN0aW9uRGF0ZV9kZXNjJTJDcHJvZF91cGNvbWluZ19sb3RzX2NoaW5lc2Vfc2ltcGxpZmllZF9hc2MlMkNwcm9kX3VwY29taW5nX2xvdHNfY2hpbmVzZV9zaW1wbGlmaWVkX2Rlc2MlMkNwcm9kX2xvdHNfY2hpbmVzZV9zaW1wbGlmaWVkX2xvd0VzdGltYXRlX2FzYyUyQ3Byb2RfbG90c19jaGluZXNlX3NpbXBsaWZpZWRfbG93RXN0aW1hdGVfZGVzYyUyQ3Byb2Rfc3VnZ2VzdGVkX2xvdHNfY2hpbmVzZV9zaW1wbGlmaWVkJTJDcHJvZF9meWVvX2xvdHNfY2hpbmVzZV9zaW1wbGlmaWVkX2F1Y3Rpb25EYXRlX2FzYyUyQ3Byb2RfZnllb19sb3RzX2NoaW5lc2Vfc2ltcGxpZmllZF9hdWN0aW9uRGF0ZV9kZXNjJTJDb2JqZWN0X3R5cGVzJTJDcHJvZF9vYmplY3RfdHlwZXMlMkNwcm9kX29iamVjdF90eXBlc18qJTJDaXRlbXMlMkNwcm9kX2l0ZW1zJTJDcHJvZF9pdGVtc18qJTJDYXR0cmlidXRlcyUyQ3Byb2RfYXR0cmlidXRlcyUyQ3Byb2RfYXR0cmlidXRlc18qJTJDYXR0cmlidXRlX2ZpeGVkX3ZhbHVlcyUyQ3Byb2RfYXR0cmlidXRlX2ZpeGVkX3ZhbHVlcyUyQ3Byb2RfYXR0cmlidXRlX2ZpeGVkX3ZhbHVlc18qJTJDcGllY2VzJTJDcHJvZF9waWVjZXMlMkNwcm9kX3BpZWNlc18qJTJDcHJvZHVjdF9pdGVtcyUyQ3Byb2RfcHJvZHVjdF9pdGVtcyUyQ3Byb2RfcHJvZHVjdF9pdGVtc18qJTJDcHJvZF9wcm9kdWN0X2l0ZW1zX2xvd0VzdGltYXRlX2FzYyUyQ3Byb2RfcHJvZHVjdF9pdGVtc19sb3dFc3RpbWF0ZV9kZXNjJTJDcHJvZF9wcm9kdWN0X2l0ZW1zX3B1Ymxpc2hEYXRlX2FzYyUyQ3Byb2RfcHJvZHVjdF9pdGVtc19wdWJsaXNoRGF0ZV9kZXNjJTJDc290aGVieXNfY2F0ZWdvcmllcyUyQ3NvdGhlYnlzX2NhdGVnb3JpZXMlMkNzb3RoZWJ5c19jYXRlZ29yaWVzXyolMkN0YWdnaW5nX3RhZ3NldHMlMkNwcm9kX3RhZ2dpbmdfdGFnc2V0cyUyQ3Byb2RfdGFnZ2luZ190YWdzZXRzXyolMkN0YWdnaW5nX3RhZ3MlMkNwcm9kX3RhZ2dpbmdfdGFncyUyQ3Byb2RfdGFnZ2luZ190YWdzXyolMkNvbmJvYXJkaW5nX3RvcGljcyUyQ3Byb2Rfb25ib2FyZGluZ190b3BpY3MlMkNwcm9kX29uYm9hcmRpbmdfdG9waWNzXyolMkNmb2xsb3dhYmxlX3RvcGljcyUyQ3Byb2RfZm9sbG93YWJsZV90b3BpY3MlMkNwcm9kX2ZvbGxvd2FibGVfdG9waWNzXyolMkN3aW5lJTJDcHJvZF93aW5lJTJDcHJvZF93aW5lXyomZmlsdGVycz1OT1Qrc3RhdGUlM0FDcmVhdGVkK0FORCtOT1Qrc3RhdGUlM0FEcmFmdCtBTkQrTk9UK2lzVGVzdFJlY29yZCUzRDErQU5EK05PVCtsb3RTdGF0ZSUzQUNyZWF0ZWQrQU5EK05PVCtsb3RTdGF0ZSUzQURyYWZ0K0FORCslMjhOT1QraXNIaWRkZW4lM0F0cnVlK09SK2xlYWRlcklkJTNBMDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAwJTI5',
            'x-algolia-application-id': 'KAR1UEUPJD',
            'content-type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.sothebys.com',
            'Connection': 'keep-alive',
            'Referer': 'https://www.sothebys.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
        }

        data1 = '{"query":"","filters":"auctionId:' + auction_id + ' AND objectTypes:\\"All\\" AND NOT isHidden:true","facetFilters":[["withdrawn:false"],[]],"hitsPerPage":1000,"page":0,"facets":["*"],"numericFilters":[]}'

        response2 = requests.post(
            'https://kar1ueupjd-1.algolianet.com/1/indexes/prod_lots/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.3)%3B%20Browser',
            headers=headers,
            data=data1,
            proxies={
                "http": "http://5af337078fb54f63bceba44b0eba7ec4:@proxy.crawlera.com:8011/",
                "https": "http://5af337078fb54f63bceba44b0eba7ec4:@proxy.crawlera.com:8011/",
            },
            verify='zyte-ca.crt'
        )
        # print(response2.content)

        object_id_list = [x['objectID'] for x in json.loads(response2.content)['hits']]

        # print(object_id_list)

        for identifier in object_id_list:
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                # 'Accept-Encoding': 'gzip, deflate, br',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'authorization,content-type',
                'Referer': 'https://www.sothebys.com/',
                'Origin': 'https://www.sothebys.com',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'Cache-Control': 'max-age=0',
            }

            json_data = {
                'operationName': 'LotQuery',
                'variables': {
                    #'id': '296b8461-4572-4e97-bcde-f37a1c1823a0',
                    'id': identifier,
                },
                'query': 'query LotQuery($id: String!) {\n  lot: lotV2(lotId: $id) {\n    __typename\n    ... on LotV2 {\n      __typename\n      ...LotV2Fragment\n      ...LotDetailNavHeaderFragment\n      ...PlaceBidTombstoneMenuFragment\n      ...PlaceBidTombstoneFragment\n      ...LotDetailCarouselFragment\n      ...LotInfoFragment\n      ...LotDetailCatalogueBSPFragment\n      ...RecommendedItemsFragment\n      ...RecommendedWatchesFragment\n      ...StickyHeaderContentFragment\n      ...PageWrapperLotFragment\n    }\n    ... on HiddenLot {\n      __typename\n      lotId\n      auction {\n        __typename\n        title\n        auctionId\n        slug {\n          __typename\n          year\n          name\n        }\n      }\n    }\n  }\n}\n\nfragment LotDetailCarouselFragment on LotV2 {\n  __typename\n  auction {\n    __typename\n    sapSaleNumber\n    departmentNames\n  }\n  lotId\n  title\n  lotNumber {\n    __typename\n    ... on VisibleLotNumber {\n      __typename\n      lotNumber\n    }\n  }\n  media(imageSizes: [Small, Medium, Large, ExtraLarge, Original]) {\n    __typename\n    images {\n      __typename\n      title\n      renditions {\n        __typename\n        url\n        width\n        height\n        imageSize\n      }\n    }\n  }\n}\n\nfragment LotDetailCatalogueBSPFragment on LotV2 {\n  __typename\n  lotId\n  auction {\n    __typename\n    enrichedCatalogueContentEnabled\n  }\n}\n\nfragment LotDetailNavHeaderFragment on LotV2 {\n  __typename\n  title\n  lotNumber {\n    __typename\n    ... on VisibleLotNumber {\n      __typename\n      lotNumber\n    }\n  }\n  auction {\n    __typename\n    title\n    auctionId\n    slug {\n      __typename\n      year\n      name\n    }\n  }\n  ...LotNavigationArrowsFragment\n  ...LotNavigationDropdownFragment\n}\n\nfragment LotNavigationArrowsFragment on LotV2 {\n  __typename\n  id\n  auction {\n    __typename\n    auctionId\n    slug {\n      __typename\n      year\n      name\n    }\n  }\n  previousLot {\n    __typename\n    slug\n    lotId\n  }\n  nextLot {\n    __typename\n    slug\n    lotId\n  }\n}\n\nfragment LotNavigationDropdownFragment on LotV2 {\n  __typename\n  lotId\n  lotNumber {\n    __typename\n    ... on VisibleLotNumber {\n      __typename\n      lotNumber\n    }\n  }\n  auction {\n    __typename\n    auctionId\n    useCreatorSplit\n    lotCards(filter: ALL) {\n      __typename\n      lotId\n      lotNumber {\n        __typename\n        ... on VisibleLotNumber {\n          __typename\n          lotNumber\n        }\n      }\n      creators {\n        __typename\n        displayName\n      }\n      creatorPrefix\n      slug {\n        __typename\n        lotSlug\n        auctionSlug {\n          __typename\n          year\n          name\n        }\n      }\n      title\n      subtitle\n    }\n  }\n}\n\nfragment LotInfoFragment on LotV2 {\n  __typename\n  auction {\n    __typename\n    sapSaleNumber\n    departmentNames\n    useCreatorSplit\n    showGuaranteeLine\n  }\n  lotId\n  description\n  saleroomNotice\n  condition {\n    __typename\n    ... on ConditionHidden {\n      __typename\n      contactEmail\n    }\n    ... on ConditionPublished {\n      __typename\n      disclaimer\n      report\n      conditionReportDisclaimers {\n        __typename\n        content\n      }\n    }\n  }\n  conditionReportDisclaimers {\n    __typename\n    content\n  }\n  generalLotNotices {\n    __typename\n    content\n  }\n  catalogueNote\n  title\n  creatorPrefix\n  creators {\n    __typename\n    id\n    displayName\n  }\n  objects {\n    __typename\n    literature\n    exhibition\n    provenance\n  }\n  lotNumber {\n    __typename\n    ... on VisibleLotNumber {\n      __typename\n      lotNumber\n    }\n  }\n}\n\nfragment LotV2Fragment on LotV2 {\n  __typename\n  auction {\n    __typename\n    auctionId\n    title\n    currency\n    location\n    departmentNames\n    type_: type\n    slug {\n      __typename\n      name\n      year\n    }\n    sessions {\n      __typename\n      id\n      sessionId\n      title\n      state: stateV2 {\n        ...SessionStateCommonFragment\n        __typename\n      }\n    }\n    recommendedLotsEnabled\n    bidIncrementTable {\n      __typename\n      id\n      bidIncrements {\n        __typename\n        from\n        increment\n      }\n    }\n    state\n    sapSaleNumber\n    bidPhase {\n      __typename\n      auctionBidPhase {\n        __typename\n        ... on TimedAuctionBidPhaseType {\n          __typename\n          timedBidPhase\n        }\n        ... on LiveAuctionBidPhaseType {\n          __typename\n          bidMethod\n        }\n      }\n    }\n    enrollment {\n      __typename\n      restrictedDate\n      result {\n        ...AuctionBaseEnrollmentResultFragment\n        __typename\n      }\n    }\n    conditionsOfSale\n    bidTypeAvailability {\n      __typename\n      online {\n        __typename\n        isAvailable\n      }\n      saleroom {\n        __typename\n        isAvailable\n      }\n      phone {\n        __typename\n        isAvailable\n        availabilityStatus {\n          __typename\n          ... on DisabledAvailabilityStatus {\n            __typename\n            auctionId\n          }\n          ... on EnabledAvailabilityStatus {\n            __typename\n            auctionId\n          }\n          ... on ScheduledAvailabilityStatus {\n            __typename\n            auctionId\n            cutoffTime\n          }\n        }\n      }\n    }\n    dates {\n      __typename\n      acceptsBids\n    }\n    ...GoToAuctionRoomFragment\n    ...PendingFragment\n  }\n  title\n  lotId\n  slug\n  lotNumber {\n    __typename\n    ... on VisibleLotNumber {\n      __typename\n      lotNumber\n    }\n  }\n  estimateV2 {\n    __typename\n    ... on LowHighEstimateV2 {\n      __typename\n    }\n  }\n  session {\n    __typename\n    sessionId\n    stateV2 {\n      __typename\n      state\n    }\n  }\n  bidState {\n    __typename\n    bidTypeV2 {\n      __typename\n      ... on TimedBidTypeV2 {\n        __typename\n        timedBidPhase\n      }\n      ... on LiveBidType {\n        __typename\n        liveBidPhase\n      }\n    }\n  }\n  brightcoveVideoId\n}\n\nfragment AuctionBaseEnrollmentResultFragment on EnrollmentResultConnection {\n  __typename\n  id\n  auctionId\n  enrollmentResult {\n    __typename\n    ... on EnrollmentAccepted {\n      __typename\n      auctionId\n      paddleId\n    }\n    ... on EnrollmentDeclined {\n      __typename\n      auctionId\n      enrollmentDeclinedReason\n    }\n    ... on EnrollmentUpForReview {\n      __typename\n      auctionId\n      enrollmentUpForReviewReason\n    }\n  }\n}\n\nfragment GoToAuctionRoomFragment on Auction {\n  __typename\n  title\n  sessions {\n    __typename\n    id\n    sessionId\n    title\n    state: stateV2 {\n      ...SessionStateCommonFragment\n      __typename\n    }\n  }\n}\n\nfragment SessionStateCommonFragment on SessionState {\n  __typename\n  id\n  state\n}\n\nfragment PendingFragment on Auction {\n  __typename\n  title\n  locationV2 {\n    __typename\n    displayLocation {\n      __typename\n      name\n    }\n  }\n}\n\nfragment PageWrapperLotFragment on LotV2 {\n  __typename\n  lotId\n  title\n  media(imageSizes: [Small, Medium, Large, ExtraLarge, Original]) {\n    __typename\n    images {\n      __typename\n      renditions {\n        __typename\n        height\n        imageSize\n        url\n        width\n      }\n      title\n    }\n  }\n  bidState {\n    __typename\n    sold {\n      __typename\n      ... on ResultVisible {\n        __typename\n        isSold\n      }\n    }\n  }\n  description\n  condition {\n    __typename\n    ... on ConditionPublished {\n      __typename\n      report\n    }\n    ... on ConditionHidden {\n      __typename\n    }\n  }\n  auction {\n    __typename\n    auctionId\n    title\n    slug {\n      __typename\n      year\n    }\n    departmentNames\n    testRecord\n  }\n}\n\nfragment PlaceBidTombstoneFragment on LotV2 {\n  __typename\n  ...TitleFragment\n  ...LotSymbolsAndTagsFragment\n  ...PlaceBidTombstoneMenuFragment\n  ...TombstoneBidFlow_lot\n}\n\nfragment LotSymbolsAndTagsFragment on LotV2 {\n  __typename\n  symbols\n  lotTags\n  parcel {\n    __typename\n    parcelName\n  }\n  acceptsCryptoPayments\n  premiumLotState {\n    __typename\n    isPremium\n  }\n}\n\nfragment PlaceBidTombstoneMenuFragment on LotV2 {\n  __typename\n  lotId\n  sapAuctionSaleNumber\n  lotNumber {\n    __typename\n    ... on VisibleLotNumber {\n      __typename\n      lotNumber\n    }\n  }\n  slug\n  creatorPrefix\n  creators {\n    __typename\n    id\n    displayName\n  }\n  bidState {\n    __typename\n    isClosed\n  }\n  auction {\n    __typename\n    currency\n    costEstimationEnabled\n    useCreatorSplit\n    slug {\n      __typename\n      name\n      year\n    }\n    type_: type\n  }\n  ...LotSaveHeartFragment\n  ...CostEstimatorFragment\n  ...TombstoneCountdown_lotTimer\n}\n\nfragment CostEstimatorFragment on LotV2 {\n  __typename\n  auction {\n    __typename\n    location\n    currency\n    sapSaleNumber\n    bidIncrementTable {\n      __typename\n      bidIncrements {\n        __typename\n        from\n        increment\n      }\n    }\n  }\n  description\n  lotId\n  title\n  subtitle\n  lotNumber {\n    __typename\n    ... on VisibleLotNumber {\n      __typename\n      lotNumber\n    }\n  }\n  estimate {\n    __typename\n    ... on LowHighEstimate {\n      __typename\n      lowEstimate\n      highEstimate\n    }\n    ... on EstimateUponRequest {\n      __typename\n    }\n  }\n}\n\nfragment LotSaveHeartFragment on LotV2 {\n  __typename\n  isSaved\n  lotId\n  session {\n    __typename\n    sessionId\n  }\n  lotNumber {\n    __typename\n    ... on VisibleLotNumber {\n      __typename\n      lotNumber\n    }\n  }\n  auction {\n    __typename\n    sapSaleNumber\n    type_: type\n  }\n}\n\nfragment TombstoneCountdown_lotTimer on LotV2 {\n  __typename\n  auction {\n    __typename\n    sessions {\n      __typename\n      sessionId\n    }\n    dates {\n      __typename\n      __typename\n      closed\n    }\n    bidPhase {\n      ...AuctionBidPhaseFragment\n      __typename\n    }\n  }\n  session {\n    __typename\n    scheduledOpeningDate\n    stateV2 {\n      ...SessionStateCommonFragment\n      __typename\n    }\n  }\n  bidState {\n    ...TombstoneCountdown_bidState\n    __typename\n  }\n}\n\nfragment AuctionBidPhaseFragment on AuctionBidPhaseConnection {\n  __typename\n  id\n  auctionBidPhase {\n    __typename\n    ... on TimedAuctionBidPhaseType {\n      __typename\n      closingInterval\n      timedBidPhase\n    }\n    ... on LiveAuctionBidPhaseType {\n      __typename\n      bidMethod\n      liveBidPhase\n    }\n  }\n}\n\nfragment TombstoneCountdown_bidState on BidState {\n  __typename\n  id\n  ...TombstoneCountdown_timedBidState\n  bidType: bidTypeV2 {\n    __typename\n    ... on LiveBidType {\n      ...TombstoneCountdown_liveBidType\n      __typename\n    }\n    ... on TimedBidTypeV2 {\n      ...TombstoneCountdown_timedBidType\n      __typename\n    }\n  }\n}\n\nfragment TombstoneCountdown_liveBidType on LiveBidType {\n  __typename\n  liveBidPhase\n}\n\nfragment TombstoneCountdown_timedBidState on BidState {\n  __typename\n  closingTime\n}\n\nfragment TombstoneCountdown_timedBidType on TimedBidTypeV2 {\n  __typename\n  timedBidPhase\n}\n\nfragment TitleFragment on LotV2 {\n  __typename\n  auction {\n    __typename\n    useCreatorSplit\n  }\n  designationLine\n  creatorPrefix\n  title\n  subtitle\n  creators {\n    __typename\n    displayName\n  }\n}\n\nfragment TombstoneBidFlow_lot on LotV2 {\n  __typename\n  lotId\n  title\n  lotNumber {\n    __typename\n    ... on VisibleLotNumber {\n      __typename\n      lotNumber\n    }\n  }\n  session {\n    __typename\n    sessionId\n  }\n  auction {\n    __typename\n    auctionId\n    sapSaleNumber\n    title\n    enrollment {\n      __typename\n      paddle\n      account {\n        __typename\n        holderName\n        accountId\n      }\n    }\n    currencyV2\n    departmentNames\n    bidPhase {\n      __typename\n      auctionBidPhase {\n        __typename\n        ... on LiveAuctionBidPhaseType {\n          __typename\n        }\n        ... on TimedAuctionBidPhaseType {\n          __typename\n        }\n      }\n    }\n    bidTypeAvailability {\n      __typename\n      advance {\n        __typename\n        availabilityStatus {\n          __typename\n          ... on DisabledAvailabilityStatus {\n            __typename\n            auctionId\n          }\n        }\n      }\n    }\n    _type: type\n    locationV2 {\n      __typename\n      name\n    }\n  }\n  withdrawnState {\n    ...TombstoneBidFlow_WithdrawnLotState\n    __typename\n  }\n  ...TombstoneBidFlow_bidCapCheck\n  latestBid {\n    ...TombstoneBidFlow_UserBidConnection\n    __typename\n  }\n  ...TombstoneBidFlow_ActionButton\n  ...TombstoneCountdown_lotTimer\n  ...TombstoneBiddingInfo_BiddingInfo\n  ...UserBidInfoFragment\n  ...TombstoneEnterBidFragment\n  ...TombstoneSelectAccountFragment\n  ...TombstoneBidDetailsFragment\n}\n\nfragment TombstoneBidDetailsFragment on LotV2 {\n  __typename\n  ...TombstoneBidDetails_BidInfo\n  ...TombstoneBidDetails_BidPlaced\n}\n\nfragment TombstoneBidDetails_BidInfo on LotV2 {\n  __typename\n  auction {\n    __typename\n    bidIncrementTable {\n      __typename\n      hasBuyersPremium\n    }\n    currencyV2\n  }\n}\n\nfragment TombstoneBidDetails_BidPlaced on LotV2 {\n  __typename\n  auction {\n    __typename\n    auctionId\n    sapSaleNumber\n    departmentNames\n    type_: type\n    locationV2 {\n      __typename\n      name\n    }\n    currencyV2\n  }\n  bidState {\n    ...TombstoneBidDetails_BidState\n    __typename\n  }\n}\n\nfragment TombstoneBidDetails_BidState on BidState {\n  __typename\n  currentBid: currentBidV2 {\n    __typename\n    amount\n  }\n}\n\nfragment TombstoneBidFlow_ActionButton on LotV2 {\n  __typename\n  auction {\n    __typename\n    sapSaleNumber\n    auctionId\n    title\n  }\n  lotId\n  title\n  lotNumber {\n    __typename\n    ... on VisibleLotNumber {\n      __typename\n      lotNumber\n    }\n  }\n  bidState {\n    ...TombstoneBidFlow_bidState\n    __typename\n  }\n  premiumLotState {\n    ...TombstoneBidFlow_PremiumLotState\n    __typename\n  }\n  ...TombstoneBidFlow_PlaceBid\n  ...TombstoneBidFlow_RegisterToBid\n}\n\nfragment TombstoneBidFlow_PlaceBid on LotV2 {\n  __typename\n  id\n  auction {\n    __typename\n    sapSaleNumber\n    auctionId\n    title\n    slug {\n      __typename\n      name\n      year\n    }\n    enrollment {\n      __typename\n      restrictedDate\n      result {\n        ...AuctionBaseEnrollmentResultFragment\n        __typename\n      }\n    }\n  }\n  title\n  lotNumber {\n    __typename\n    ... on VisibleLotNumber {\n      __typename\n      lotNumber\n    }\n  }\n  slug\n  lotId\n  session {\n    __typename\n    stateV2 {\n      ...SessionStateCommonFragment\n      __typename\n    }\n  }\n  bidState {\n    ...TombstoneBidFlow_bidState\n    __typename\n  }\n  premiumLotState {\n    ...TombstoneBidFlow_PremiumLotState\n    __typename\n  }\n  withdrawnState {\n    ...TombstoneBidFlow_WithdrawnLotState\n    __typename\n  }\n  latestBid {\n    ...TombstoneBidFlow_UserBidConnection\n    __typename\n  }\n  ...TombstoneBidFlow_bidCapCheck\n}\n\nfragment TombstoneBidFlow_PremiumLotState on PremiumLotState {\n  __typename\n  id\n  isPremium\n  userIsWhitelisted\n}\n\nfragment TombstoneBidFlow_UserBidConnection on UserBidConnection {\n  __typename\n  id\n  bid {\n    __typename\n    lotId\n    bidState\n  }\n}\n\nfragment TombstoneBidFlow_WithdrawnLotState on LotWithdrawnState {\n  __typename\n  id\n  state\n}\n\nfragment TombstoneBidFlow_bidCapCheck on LotV2 {\n  __typename\n  auction {\n    __typename\n    enrollment {\n      __typename\n      bidCap {\n        ...TombstoneBidFlow_bidCap\n        __typename\n      }\n    }\n  }\n  bidState {\n    __typename\n    bidAsk\n  }\n  latestBid {\n    __typename\n    id\n    bid {\n      __typename\n      bidState\n      amountV2 {\n        __typename\n        amount\n      }\n    }\n  }\n}\n\nfragment TombstoneBidFlow_bidCap on BidCapConnection {\n  __typename\n  id\n  bidCap {\n    __typename\n    amount\n    amountInUse\n    isCapReached\n  }\n}\n\nfragment TombstoneBidFlow_bidState on BidState {\n  __typename\n  id\n  isClosed\n  bidTypeV2 {\n    __typename\n    ... on LiveBidType {\n      __typename\n      liveBidPhase\n    }\n    ... on TimedBidTypeV2 {\n      __typename\n      timedBidPhase\n    }\n  }\n}\n\nfragment TombstoneBidFlow_RegisterToBid on LotV2 {\n  __typename\n  sapAuctionSaleNumber\n  auction {\n    __typename\n    enrollment {\n      __typename\n      restrictedDate\n    }\n  }\n}\n\nfragment TombstoneBiddingInfo_BiddingInfo on LotV2 {\n  __typename\n  auction {\n    __typename\n    currencyV2\n  }\n  estimateV2 {\n    __typename\n    ... on LowHighEstimateV2 {\n      __typename\n      lowEstimate {\n        __typename\n        amount\n      }\n      highEstimate {\n        __typename\n        amount\n      }\n    }\n    ... on EstimateUponRequest {\n      __typename\n      estimateUponRequest\n    }\n  }\n  bidState {\n    ...TombstoneBiddingInfo_BidState\n    __typename\n  }\n  latestBid {\n    __typename\n    bid {\n      __typename\n      amountV2 {\n        __typename\n        amount\n      }\n      bidState\n      additionalLotsToBuy\n    }\n  }\n  lotTags\n  premiumLotState {\n    __typename\n    isPremium\n    userIsWhitelisted\n  }\n}\n\nfragment TombstoneBiddingInfo_BidState on BidState {\n  __typename\n  id\n  isClosed\n  bidTypeV2 {\n    __typename\n    ... on LiveBidType {\n      __typename\n      bidMethod\n      liveBidPhase\n    }\n    ... on TimedBidTypeV2 {\n      __typename\n      timedBidPhase\n    }\n  }\n  ...TombstoneBiddingInfo_timedBidState\n  ...TombstoneBiddingInfo_closedBidState\n  ...TombstoneBiddingInfo_liveBidState\n}\n\nfragment TombstoneBiddingInfo_closedBidState on BidState {\n  __typename\n  sold {\n    __typename\n    ... on ResultHidden {\n      __typename\n    }\n    ... on ResultVisible {\n      __typename\n      isSold\n      premiums {\n        __typename\n        finalPriceV2 {\n          __typename\n          amount\n        }\n      }\n    }\n  }\n}\n\nfragment TombstoneBiddingInfo_liveBidState on BidState {\n  __typename\n  currentBidV2 {\n    __typename\n    amount\n  }\n  startingBidV2 {\n    __typename\n    amount\n  }\n}\n\nfragment TombstoneBiddingInfo_timedBidState on BidState {\n  __typename\n  numberOfBids\n  reserveMet\n  startingBidV2 {\n    __typename\n    amount\n  }\n  currentBidV2 {\n    __typename\n    amount\n  }\n}\n\nfragment TombstoneEnterBidFragment on LotV2 {\n  __typename\n  auction {\n    __typename\n    currency\n    bidPhase {\n      __typename\n      auctionBidPhase {\n        __typename\n        ... on LiveAuctionBidPhaseType {\n          __typename\n          bidMethod\n        }\n      }\n    }\n    enrollment {\n      __typename\n      bidCap {\n        __typename\n        bidCap {\n          __typename\n          amount\n          amountInUse\n          isCapReached\n        }\n      }\n    }\n    bidIncrementTable {\n      __typename\n      id\n      bidIncrements {\n        __typename\n        from\n        increment\n      }\n      premiumIncrements {\n        __typename\n        from\n        percentage\n      }\n    }\n    locationV2 {\n      __typename\n      name\n    }\n    bidTypeAvailability {\n      __typename\n      advance {\n        __typename\n        availabilityStatus {\n          __typename\n          ... on DisabledAvailabilityStatus {\n            __typename\n            auctionId\n          }\n        }\n      }\n    }\n  }\n  parcel {\n    __typename\n    totalLotsInParcel\n    canSellAdditionalCount\n  }\n  bidState {\n    __typename\n    bidAsk\n    bidTypeV2 {\n      __typename\n      ... on TimedBidTypeV2 {\n        __typename\n      }\n      ... on LiveBidType {\n        __typename\n      }\n    }\n    startingBidV2 {\n      __typename\n      amount\n    }\n    currentBidV2 {\n      __typename\n      amount\n    }\n  }\n  estimateV2 {\n    __typename\n    ... on LowHighEstimateV2 {\n      __typename\n      lowEstimate {\n        __typename\n        amount\n      }\n    }\n  }\n  latestBid {\n    __typename\n    bid {\n      __typename\n      bidState\n      amountV2 {\n        __typename\n        amount\n      }\n    }\n  }\n}\n\nfragment TombstoneSelectAccountFragment on LotV2 {\n  __typename\n  auction {\n    __typename\n    location\n    conditionsOfSale\n  }\n}\n\nfragment UserBidInfoFragment on LotV2 {\n  __typename\n  auction {\n    __typename\n    currencyV2\n    enrollment {\n      __typename\n      bidCap {\n        __typename\n        bidCap {\n          __typename\n          isCapReached\n          amount\n          amountInUse\n        }\n      }\n    }\n  }\n  latestBid {\n    ...UserBidInfo_latestBid\n    __typename\n  }\n  bidState {\n    ...UserBidInfo_bidState\n    __typename\n  }\n  premiumLotState {\n    __typename\n    isPremium\n    userIsWhitelisted\n  }\n}\n\nfragment UserBidInfo_bidState on BidState {\n  __typename\n  id\n  bidAsk\n  sold {\n    __typename\n    ... on ResultHidden {\n      __typename\n    }\n    ... on ResultVisible {\n      __typename\n      isSold\n      premiums {\n        __typename\n        finalPriceV2 {\n          __typename\n          amount\n        }\n      }\n    }\n  }\n}\n\nfragment UserBidInfo_latestBid on UserBidConnection {\n  __typename\n  id\n  bid {\n    __typename\n    bidState\n    amountV2 {\n      __typename\n      amount\n    }\n  }\n}\n\nfragment RecommendedItemsFragment on LotV2 {\n  __typename\n  auction {\n    __typename\n    useCreatorSplit\n  }\n  recommendations(hideNonAvailable: true) {\n    __typename\n    ... on LotCard {\n      __typename\n      auction {\n        __typename\n        auctionId\n        currency\n      }\n      lotId\n      title\n      subtitle\n      lotNumber {\n        __typename\n        ... on VisibleLotNumber {\n          __typename\n          lotNumber\n        }\n      }\n      estimateV2 {\n        __typename\n        ... on EstimateUponRequest {\n          __typename\n          estimateUponRequest\n        }\n        ... on LowHighEstimateV2 {\n          __typename\n          highEstimate {\n            __typename\n            amount\n          }\n          lowEstimate {\n            __typename\n            amount\n          }\n        }\n      }\n      creators {\n        __typename\n        displayName\n      }\n      creatorPrefix\n      slug {\n        __typename\n        auctionSlug {\n          __typename\n          name\n          year\n        }\n        lotSlug\n      }\n      withdrawnState {\n        __typename\n        state\n      }\n      bidState {\n        __typename\n        isClosed\n      }\n    }\n    ... on RetailItem {\n      __typename\n      ...MarketplaceItemFragment\n    }\n  }\n}\n\nfragment MarketplaceItemFragment on RetailItem {\n  __typename\n  id\n  retailItemId\n  retailItemSlug: slug\n  title\n  propertyType\n  creators {\n    __typename\n    displayName\n  }\n  pricing {\n    __typename\n    listPrice\n    currency\n  }\n  media(imageSizes: [Small]) {\n    __typename\n    images {\n      __typename\n      renditions {\n        __typename\n        url\n        imageSize\n        width\n        height\n      }\n    }\n  }\n}\n\nfragment RecommendedWatchesFragment on LotV2 {\n  __typename\n  auction {\n    __typename\n    testRecord\n    currencyV2\n  }\n  lotId\n  title\n  estimateV2 {\n    __typename\n    ... on EstimateUponRequest {\n      __typename\n      estimateUponRequest\n    }\n    ... on LowHighEstimateV2 {\n      __typename\n      highEstimate {\n        __typename\n        amount\n      }\n      lowEstimate {\n        __typename\n        amount\n      }\n    }\n  }\n}\n\nfragment StickyHeaderContentFragment on LotV2 {\n  __typename\n  auction {\n    __typename\n    currencyV2\n    slug {\n      __typename\n      name\n      year\n    }\n    bidPhase {\n      ...AuctionBidPhaseFragment\n      __typename\n    }\n    auctionType: type\n  }\n  slug\n  lotId\n  title\n  bidState {\n    ...StickyHeaderContentBidStateFragment\n    __typename\n  }\n  ...StickyHeaderTitleFragment\n}\n\nfragment StickyHeaderContentBidStateFragment on BidState {\n  __typename\n  id\n  startingBid: startingBidV2 {\n    __typename\n    amount\n  }\n  currentBid: currentBidV2 {\n    __typename\n    amount\n  }\n  bidTypeV2 {\n    __typename\n    ... on LiveBidType {\n      __typename\n      bidMethod\n    }\n  }\n  isClosed\n  sold {\n    __typename\n    ... on ResultHidden {\n      __typename\n    }\n    ... on ResultVisible {\n      __typename\n      isSold\n      premiums {\n        __typename\n        finalPrice: finalPriceV2 {\n          __typename\n          amount\n        }\n      }\n    }\n  }\n}\n\nfragment StickyHeaderTitleFragment on LotV2 {\n  __typename\n  title\n  subtitle\n  lotNumber {\n    __typename\n    ... on VisibleLotNumber {\n      __typename\n      lotNumber\n    }\n    ... on HiddenLotNumber {\n      __typename\n      isHidden\n    }\n  }\n  auction {\n    __typename\n    useCreatorSplit\n  }\n  creatorPrefix\n  creators {\n    __typename\n    displayName\n  }\n}\n',
            }


            response3 = requests.post('https://clientapi.prod.sothelabs.com/graphql'
                                    , headers=headers
                                    , json=json_data
                                    , proxies={
                    "http": "http://5af337078fb54f63bceba44b0eba7ec4:@proxy.crawlera.com:8011/",
                    "https": "http://5af337078fb54f63bceba44b0eba7ec4:@proxy.crawlera.com:8011/",
                }, verify='zyte-ca.crt' 
                )

            # find_out = json.loads(response3.content)['data']['lot']
            # json.loads(response3.content)['data']['lot'].keys()
            find_out = json.loads(response3.content)
            print(find_out['data']['lot'].keys())
            print("#################################################################")
            # Get the value associated with the 'lot' key
            # lot_value = find_out
            json_row = find_out['data']['lot']


            value_dict = {}

            #hammer price
            try:
                hammer_price = json_row['bidState']['currentBid']['amount']
                
                print(hammer_price)
            except:
                hammer_price = None

            #item_url
            try:
                auction_slug = json_row['slug']
                auction_slug = auction_url+'/'+auction_slug
                print(auction_slug)
            except:
                auction_slug = None
            #date when auction is open
            try:
                open_auction_date = json_row['auction']['dates']['acceptsBids']
                print(open_auction_date)
                #remove any commas
                # print("This is the auction_id",auction_id)
            except:
                open_auction_date = None

            #date when auction is closed
            try:
                close_auction_date = json_row['auction']['dates']['closed']
                original_date_string = close_auction_date
                original_date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
                desired_date_format = "%Y-%m-%d %H:%M:%S"

                # Parse the original date string
                parsed_date = datetime.strptime(original_date_string, original_date_format)

                # Format the parsed date into the desired format
                formatted_date = parsed_date.strftime(desired_date_format)

                close_auction_date = formatted_date
                # print(formatted_date)
                print(close_auction_date)
                #remove any commas
                # print("This is the auction_id",auction_id)
            except:
                close_auction_date = None

            
        #     #closing time
        #     try:
        #         closingTime = json_row['bidState']['closingTime']
        #         print("This is closingTime",closingTime)
        #     except:
        #         closingTime = None
        #         print("This is closingTime",closingTime)
        #         #print BidState

        # #     try:        
        # #         # 
        # #         Bids = json_row['bidState']['numberOfBids']
        # #         print("This is numberofBids",Bids)
        # #     except:
        # #         numberOfBids = None
        # #         print("This is numberofBids",Bids)

        # #     #currentBidV2
        # #     try:
        # #         currentBidV2 = json_row['bidState']['currentBidV2']['amount']
        # #         print("This is currentBidV2",currentBidV2)
        # #     except:
        # #         currentBidV2 = None
        # #         print("This is currentBid",currentBidV2)

            #finalPriceV2
            try:
                finalPriceV2 = json_row['bidState']['sold']['premiums']['finalPriceV2']['amount']
                print("This is finalPriceV2",finalPriceV2)
            except:
                finalPriceV2 = None
                print("This is finalPriceV2",finalPriceV2)

            #sold
            try:
                sold = json_row['bidState']['sold']['isSold']    
                print("This is sold",sold)
            except:
                sold = None
                print("This is sold",sold)

            # estimateV2
            try:
                lowestimateV2 = json_row['estimateV2']['lowEstimate']['amount']
                print("This is the lowest estimate",lowestimateV2)
            except:
                lowestimateV2 = None
                print("This is the lowest estimate",lowestimateV2)

            try:
                highEstimateV2 = json_row['estimateV2']['highEstimate']['amount']
                print("This is the high estimate",highEstimateV2)
            except:
                highEstimateV2 = None
                print("This is the high estimate",highEstimateV2)

            try:
                auction_name = json_row['auction']['title']
                #remove any commas
                my_list = auction_name.split(",")
                auction_name = "".join(my_list)
                print("This is the auction_name",auction_name)
            except:
                auction_name = None

            try:
                location = json_row['auction']['location']
                #remove any commas
                my_list = location.split(",")
                location = "".join(my_list)
                print("This is the location",location)
            except:
                location = None

            try:
                auction_id = json_row['auction']['auctionId']
                #remove any commas
                print("This is the auction_id",auction_id)
            except:
                auction_id = None

            try:
                title = json_row['title']
                #remove any commas
                
                my_list = title.split(",")
                title = unidecode("".join(my_list))
                print("This is the title",title)
            except:
                title = None

            # lotNumber
            try:
                lotNumber = json_row['lotNumber']['lotNumber']
                print("This is the lot number",lotNumber)
            except:
                lotNumber = None
            
            #currency
            try:
                currency = json_row['auction']['currency']
                print("This is the curreny",currency)
            except:
                print("There is no currency")
                currency = None

            #artist
            try:
                artist = unidecode(json_row['creators'][0]['displayName'])
                print("This is the creator's name",artist)
            except:
                print("There is no creator's name")
                artist = None

            #slug
            
            # literature
            try:
                literature = unidecode(json_row['objects'][0]['literature'])
                print("This is literature",literature)
            except:
                literature = None
                print("This is literature",literature)
                # print BidState

            #exhibition
            try:
                exhibition = unidecode(json_row['objects'][0]['exhibition'])
                print("This is exhibition",exhibition)
            except:
                exhibition = None
                print("This is exhibition",exhibition)

            #provenance
            try:
                provenance = unidecode(json_row['objects'][0]['provenance'])
                print("This is provenance",provenance)
            except:
                provenance = None
                print("This is provenance",provenance)
                #print BidState

            # Description
            try:
                description = unidecode(json_row['description'])
                my_list = description.split(",")
                description = "".join(my_list)
                print("This is the description",description)
            except:
                description = None


            # value_dict["closingTime"] = closingTime
            # value_dict["open_auction_date"] = open_auction_date
            value_dict["close_auction_date"] = close_auction_date
            value_dict["hammer_price_orig"] = hammer_price
            value_dict["hammer_price_usd"] = 'null'
            value_dict["final_price"] = finalPriceV2
            value_dict["final_price_usd"] = 'null'
            value_dict["low_estimate_orig"] = lowestimateV2
            value_dict["low_estimate_usd"] = 'null'
            value_dict["high_estimate_orig"] = highEstimateV2
            value_dict["high_estimate_usd"] = 'null'
            value_dict["auction_name"] = auction_name
            value_dict["auction_location"] = location
            value_dict["auction_id"] = auction_id
            value_dict["item_title"] = title
            value_dict["lotNumber"] = lotNumber
            value_dict["is_sold"] = sold
            value_dict["curreny"] = currency
            value_dict["artist"] = artist
            value_dict["auction_url"] = auction_url
            value_dict["item_url"] = auction_slug
            value_dict["auction_house"] = "Sothebys"
            value_dict["exhibited"] = exhibition
            value_dict["provenance"] = provenance
            value_dict["literature"] = literature
            value_dict["art_category"] = "null"
            value_dict["description"] = description
            value_dict["year_created"] = "null"
            value_dict["height"] = "null"
            value_dict["width"] = "null"
            value_dict["depth"] = "null"
            value_dict["area"] = "null"
            value_dict["unit"] = "null"
            value_dict["is_withdrawn"] = "null"
            value_dict["is_bought_in"] = "null"
            value_dict["is_signed"] = "null"
            value_dict["num_pieces"] = "null"
            value_dict["guarantee"] = "null"
            value_dict["art_type"] = "null"
            value_dict["medium"] = "null"
            value_dict["image_url"] = "null"

            #append this to a list
            value_list.append(value_dict)
    except:
    
        continue


df = pd.DataFrame(value_list)
# df['auction_date'] = pd.to_datetime(df['auction_date'], format='%d %B %Y')
# df['INSERT_TS'] = dt.datetime.now()
# # Concatenate variables with the file name
# file_name = f"{current_month}_{previous_day}_{current_year}_{current_time}.csv"
file_name = "sothebys.csv"

# Save DataFrame to the CSV file
df.to_csv(file_name, index=False)
# # print("done with", auction_title)




    
    

    
    