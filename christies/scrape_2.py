import requests
import json 
from unidecode import unidecode
from datetime import datetime,timedelta
import csv
import json
import os
import pandas as pd
from dateutil import parser
import dates

current_date = datetime.now()
day_before = current_date - timedelta(days=1)
current_month = str(day_before.month)
current_year = str(day_before.year)
previous_day = str(day_before.day)

print("Current day:",previous_day)
print("Current month:", current_month)
print("Current year:", current_year)

url = "https://www.christies.com/api/discoverywebsite/auctioncalendar/auctionresults?month="+current_month+"&year="+current_year+"&language=en"

response = requests.get(url)

if response.status_code == 200:
    cookies = response.cookies.get_dict()
    headers = response.headers
    print("Cookies:")
    print(cookies)
    print("Headers:")
    print(headers)

    params = {
        'language': 'en',
        'month': current_month,
        'year': current_year,
        'day' : day_before,
        'component': 'e7d92272-7bcc-4dba-ae5b-28e4f3729ae8', #still runs when this is removed but not sure what this does so leaving it for now
    }

    response_auctionList = requests.get(
        'https://www.christies.com/api/discoverywebsite/auctioncalendar/auctionresults',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    print(json.loads(response_auctionList.content)['events'])

    for auction in json.loads(response_auctionList.content)['events']:

        try:
            auction_id = auction['event_id']
            auction_id = unidecode(auction_id)
            print("This is the auction id",auction_id)
        except:
            print("There is no auction id")

        try:
            auction_url = auction['landing_url']
            auction_url = unidecode(auction_url)
            print("This is the auction url ",auction_url)
        except:
            print("No auction url")

        try:
            auction_title = auction['title_txt']
            auction_title = unidecode(auction_title)
            print("This is title of the auction",auction_title)
        except:
            print("No auction title")

        try:
            auction_date = auction['date_display_txt']
            auction_date = unidecode(auction_date)
            print("This is date of the auction ",auction_date)
            
        except:
            print("No auction date")

        try:
            auction_location = auction['location_txt']
            auction_location = unidecode(auction_location)
            print("This is location of the auction ",auction_location)
        except:
            print("No auction location")

        print(dates.rectify_dates(auction_date))

        #day
        auction_day = dates.rectify_dates(auction_date)[0] 
        auction_month = dates.rectify_dates(auction_date)[1]

        if auction_day == previous_day:
            print("This is the previous date")
            # COMMAND ----------
            page_count = 1
            list_of_lots = []
            list_of_lot_data = []
            while True:
                params = {
                    'action': 'refinecoa',
                    'language': 'en',
                    'page': page_count,
                    'saleid': auction['event_id'],
                    'salenumber': auction['analytics_id'].split('-')[1],
                    'saletype': 'Sale',
                    'sortby': 'lotnumber',
                }

                response = requests.get(
                    'https://www.christies.com/api/discoverywebsite/auctionpages/lotsearch',
                    params=params,
                    cookies=cookies,
                    headers=headers,
                )

                # COMMAND ----------
                # print(response.content)
                art_pieces_data = json.loads(response.content)['lots']

                if len(art_pieces_data) != 0:
                    list_of_lots.extend(art_pieces_data)
                    print(len(art_pieces_data))
                    page_count += 1
                else:
                    break
            print("We have ",len(list_of_lots)," lots")

            for lot in list_of_lots:
                print(lot)
                lot_data = {}
                # start_date
                try:
                    end_date = lot["start_date"]
                    end_date = unidecode(end_date)
                    print("This is the start date ",end_date)
                except:
                    print("No start date")
                #end_date
                try:
                    start_date = lot["end_date"]
                    start_date = unidecode(start_date)
                    print("End date is the end date ",start_date)
                except:
                    print("No end date")
                #lot_number
                try:
                    lot_number = lot['lot_id_txt']
                    lot_number = unidecode(lot_number)
                    print("Lot number is ",lot_number)
                except:
                    print("We have no lot number")
                #price realised
                try:
                    price_realised = lot["price_realised"]
                    print("Price realised is ",price_realised)
                except:
                    print("We have no price realised")
                #low estimate
                try:
                    low_estimate = lot["estimate_low"]
                    print("Low estimate is",low_estimate)
                except:
                    print("We have no low estimate")
                #high estimate
                try:
                    high_estimate = lot["estimate_high"]
                    print("High estimate is ",high_estimate)
                except:
                    print("We have no high estimate")
                #estimate text
                try:
                    estimate_text = lot["estimate_txt"]
                    estimate_text = estimate_text.split()
                    estimate_text = estimate_text[0]
                    print("Estimate text is ",estimate_text)
                except:
                    print("No estimate text")

                #artist
                try:
                    artist = lot["title_primary_txt"]
                    artist = artist.split(",")
                    artist = artist[0]
                    artist = unidecode(artist)
                    print("This the artist ",artist)
                except:
                    print("No artist")

                #item title
                try:
                    item_title = lot["title_secondary_txt"]
                    item_title = unidecode(item_title)
                    print("This is the item title",item_title)
                except:
                    print("This is no item title")

                #art_piece_title
                try:
                    item_url = lot["url"]
                    item_url = unidecode(item_url)
                    print("Art piece title is ",item_url)
                except:
                    print("We have no art piece title")
                #description
                try:
                    description = lot["description_txt"]
                    description = description.replace(",","").replace("\n",",")
                    description = unidecode(description)
                    print("The description is ",description)
                except:
                    print("No description")

                #add the value to one dictionary
                lot_data['auction_id'] = auction_id
                lot_data['auction_url'] = auction_url
                lot_data["start_date"] = start_date 
                lot_data["end_date"] = end_date
                lot_data['lot_id'] = lot_number
                lot_data["price_realised"] = price_realised
                lot_data["estimate_low"] = low_estimate
                lot_data["estimate_high"] = high_estimate
                lot_data["currency"] = estimate_text
                lot_data["auction_title"] = auction_title
                lot_data["auction_location"] = auction_location
                lot_data["artist"] = artist
                lot_data["item_title"] = item_title
                lot_data["item_url"] = item_url
                lot_data["description_txt"] = description

                list_of_lot_data.append(lot_data)

            
            df = pd.DataFrame(list_of_lot_data)

            df['artist'] = df['artist'].str.split(' \(').str[0]

            # Concatenate variables with the file name
            file_name = f"{current_month}_{previous_day}_{current_year}_{auction_id}.csv"

            print("This is not the previous date")

            # Save DataFrame to the CSV file
            df.to_csv(file_name, index=False)

        else:
            print("This is not the previous date")

else:
    print("Request was unsuccessful")