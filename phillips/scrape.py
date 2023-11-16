from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import csv
import re
import pandas as pd
import time 
import pycountry
import requests
from unidecode import unidecode
#open the browser
driver = webdriver.Chrome()
#go ahead and open the auction url 

past_auctions_art_work_info = []
with open('past_auctions_art_work_info.json', 'a') as f:
    global auction_id
    global lot_number
    global low_estimate
    global high_estimate 
    global is_sold
    global currency 
    global code
    global date
    global auction_url 
    global auction_title 
    global title
    global location
    global art_maker
    global description
    # global provenance
    # global exhibited
    # global literature

    auction_url = 'https://www.phillips.com/auctions/auction/UK050223'
    # auction_url_value = auction_url
    driver.get(auction_url)
    auction_id = auction_url.split("/")
    auction_id = auction_id[5]
    # auction_id_value = auction_id
    print("The auction_id is ",auction_id)
    sleep(10)

    try:
        #get the starting lot number
        starting_lot_number_div = driver.find_element(By.CSS_SELECTOR,".auction-page__grid__nav__select-lot")
        
        # starting_lot_number_select = starting_lot_number_div.find_element(By.CSS_SELECTOR,".lot-number-dropdown")
        print("Got the select element of the ",starting_lot_number_div)
        #the selector now
        lot_number_selector = driver.find_element(By.CSS_SELECTOR,".lot-number-dropdown")
        print("This is the selector ",lot_number_selector)
        #loop through the selector
        art_pieces_list = lot_number_selector.find_elements(By.TAG_NAME,"option")
        print("We have over ",len(art_pieces_list) , "art pieces")
        #list elements is already a list so we just have to loop through it 
        art_pieces_url_list = []
        for art_piece in art_pieces_list:

            art_piece_url = art_piece.get_attribute("value")
            #save to list
            art_pieces_url_list.append(art_piece_url)
        #now look at the list of url lists
        print(art_pieces_url_list) 

        counter = 0

        for art_piece in art_pieces_url_list:
            #open the url
            driver.get(art_piece)
            #auction_title
            try:
                info_field = driver.find_element(By.CLASS_NAME,"sale-title-banner__link")
                # print("Found the auction_title_tag",info_field)
                auction_title = info_field.find_element(By.CSS_SELECTOR,"h3.neueHaasMedium:nth-child(1)")
                auction_title = auction_title.text
                print("This is the auction title",auction_title)

                auction_title_lower = auction_title.lower()
                # Search for the pattern 'brown' in the string
                match = re.search(r'online', auction_title_lower)

                # If a match is found, print the matched substring
                if match:
                    print("Match is found")
                    #Location and date
                    date = info_field.find_element(By.CSS_SELECTOR,"h3.neueHaasMedium:nth-child(2)")

                    # print("This is date",date.text)
                    #split them up
                    date = date.text

                    char_to_find = "-"

                    index = date.index(char_to_find)

                    date = date[index+1:]

                    print(date)

                    location = "Online"

                    print("The location is ",location)
                    
                    #currency 
                    # use the auction instead
                    try:
                        currency_code = auction_id[:2]
                        print("This is the currency code",currency_code)
                        if currency_code == "UK":
                            currency = "GBP"
                            print("This is the currency",currency)
                        elif currency_code == "Hk":
                            currency = "HKD"
                            print("This is the currency",currency)
                        elif currency_code == "NY":
                            currency = "USD"
                            print("This is the currency",currency)
                    except:
                        currency = None
                        print("No currency found")
                                    
                else:
                    print("No match found.")
                    location_and_date = info_field.find_element(By.CSS_SELECTOR,"h3.neueHaasMedium:nth-child(2)")

                    print("This is location and date",location_and_date.text)
                    #split them up
                    location_and_date = location_and_date.text
                    splitted_str = location_and_date.split()
                    print(splitted_str)

                    try:
                        # location = splitted_str[0]
                        location = auction_id[:2]
                        print("This is the location",location)
                        if location == "UK":
                            location = 'London'
                            print("This is the location",location)
                        elif location == "HK":
                            location = 'Hong Kong'
                            print("This is the location",location)
                        elif location== "NY":
                            location  = 'New York'
                            print("This is the currency",location)
                        # location_value = location
                        # print("This is location",location)
                        try:
                            #capital
                            # currencies = CountryInfo(str(splitted_str[0])).currencies()
                            currency = pycountry.countries.search_fuzzy(str(splitted_str[0]))
                            #print
                            currency = currency[0]
                            currency = currency.alpha_3
                            if currency == 'GBR':
                                currency = 'GBP'
                                # currency_value = currency
                                print("This is the curreny",currency)
                            elif currency == 'HKG':
                                currency = 'HKD'
                                print("This is the curreny",currency)
                            else:
                                print("This is the curreny",currency)
                        except:
                            print("No currency came up")
                    except:
                        print("No location")
                    
                    try:
                        date = splitted_str[2:]
                        # date_value = date
                        delimiter = ', '
                        date = delimiter.join(date)
                        date = date.replace(",", " ")

                        char_to_find = "-"

                        index = date.index(char_to_find)

                        date = date[index+1:]

                        print("The date is ",date)
                    except:
                        print("No date")
                    
            except:
                auction_title = None
            #lot_number
            try:
                info_field = driver.find_element(By.CSS_SELECTOR,".lot-page__lot")
                # print("This is the element that holds some fields ",info_field)
                #find the lot number 
                lot_number = info_field.find_element(By.CLASS_NAME,"lot-page__lot__number")

                lot_number = lot_number.text.rstrip()

                lot_number = re.sub(r"\D", "", lot_number)

                # lot_number_value = lot_number
                print("This is the lot number",lot_number)

            except:

                lot_number = "None"

            #art_maker
            try:
                art_maker = info_field.find_element(By.CLASS_NAME,"lot-page__lot__maker__name")

                art_maker = art_maker.text.rstrip()

                # art_maker_value = art_maker

                print("This is the art maker",art_maker)

            except:

                art_maker = "None"

            #title
            try:
                title = info_field.find_element(By.CLASS_NAME,"lot-page__lot__title")

                title = title.text.rstrip()

                title = unidecode(title)

                # title_value = title
                print("This is the title ",title)

            except:

                title = "None"

            #Medium 
            try:
                composition = info_field.find_element(By.CLASS_NAME,"lot-page__lot__additional-info")

                three_inside_elements = composition.find_elements(By.TAG_NAME,"span")
                
                medium = ', '.join(three_inside_elements)

                print("This is the medium",medium)

                # size = three_inside_elements[1].text.rstrip()

                # print(size)

                # created = three_inside_elements[2].text.rstrip()

                # print(created)

            except:
                medium = "None"

                # size = "None"

                # created = "None"

            #estimate
            try:
                # info_field = driver.find_element(By.CSS_SELECTOR,".lot-page__lot")

                estimate = info_field.find_element(By.CLASS_NAME,"lot-page__lot__estimate")

                estimate = estimate.text.rstrip()

                print("This is the estimate",estimate)

                #am splitting the string such that i can analyze it
                estimate_in_usd = estimate.split()

                print(estimate_in_usd)
                
                low_estimate = estimate_in_usd[1]
                low_estimate = re.sub(r"\D", "", low_estimate)
                # low_estimate_value = low_estimate
                high_estimate = estimate_in_usd[3]
                high_estimate = re.sub(r"\D", "", high_estimate)
                # high_estimate_value = high_estimate
                print("This is a low estimate",low_estimate)
                print("This is a high estimate",high_estimate)
            except:
                estimate = "None"

            #sold
            try:
                info_field_6 = driver.find_element(By.CLASS_NAME,"lot-page__lot__sold")
                final_price = info_field_6.text.rstrip()
                final_price = final_price.split()
                final_price = final_price[-1]
                # string_with_digits = "abc123def456ghi"
                final_price = re.sub(r"\D", "", final_price)
                # final_price_value = final_price
                
                print("This art piece is the sold for ", final_price)
                is_sold = True
            except:
                final_price = "None"
                is_sold = False

            try:
                # description
                
                info_field_6 = driver.find_element(By.CSS_SELECTOR,".lot-page__lot")

                description = info_field_6.find_element(By.CLASS_NAME,"lot-page__lot__additional-info")

                description = description.text.strip()

                description = description.replace("\n",";")

                description = unidecode(description)

                # description_value = description
                print("This is the descritption ",description)

                # info_field_2 = info_field_2.text
            except:
                description = "None"
            #Add every detail to the dictionary act as a row
            #Lot page details
            info_field_7 = driver.find_element(By.CSS_SELECTOR,".lot-page__details")

            ul = info_field_7.find_element(By.TAG_NAME,"ul")

            list_items = ul.find_elements(By.NAME,"-stickyNav")

            print(len(list_items))
            for item in list_items:
                try:
                    header = item.find_element(By.TAG_NAME,"h4")

                    header = header.text

                    print("This is the ",header)

                    sleep(5)
                    try:
                        if str(header) == "Provenance":
                        
                            provenance = item.find_element(By.CLASS_NAME,"lot-page__details__list__item__value")

                            provenance = provenance.text.rstrip()

                            provenance = provenance.replace("\n","")

                            provenance = unidecode(provenance)

                            print("This is cleaned provenance ",provenance)

                        elif str(header) == "Exhibited":
                            exhibited = item.find_element(By.CLASS_NAME,"lot-page__details__list__item__value")

                            exhibited = exhibited.text.rstrip()

                            exhibited = exhibited.replace("\n","")

                            exhibited = unidecode(exhibited)

                            print("This is cleaned exhibited ",exhibited)

                        elif str(header) == "Literature":
                            literature = item.find_element(By.CLASS_NAME,"lot-page__details__list__item__value")

                            literature = literature.text.rstrip()

                            literature = literature.replace("\n","")

                            literature = unidecode(literature)

                            print("This is cleaned literature ",literature)

                        else:
                            print("No More lot page details")
                            # provenance = "None"
                            # exhibited = "None"
                            # literature = "None"
                    except:
                        continue
                    
                except:
                    continue

            value = {'auction_id':auction_id,'lot_number':lot_number,'final_price':final_price,'low_estimate':low_estimate
                     ,'high_estimate':high_estimate,'is_sold':is_sold,'currency':currency,'date':date,'auction_url':auction_url
                     ,'item_url':art_piece,'auction_title':auction_title,'art_title':title,'location':location,'art_maker':art_maker
                     ,'description':description
                     }
            
            past_auctions_art_work_info.append(value)

            # # print("This is art piece number ",counter," for ", auction_name)

            # # Writing the updated dictionary to the JSON file
            
            # json.dump(past_auctions_art_work_info, f)

            # # # df = df.drop(index)

            # # # Writing the modified DataFrame back to a CSV file
            # # df.to_csv('past_auctions_names_clean_list.csv', index=False)

            # # #increase the counter 
            counter += 1            
    except:

        pass

    json.dump(past_auctions_art_work_info, f)

# df = pd.Dataframe(past_auctions_art_work_info)

# df.to_csv('phillps.csv',index=False)