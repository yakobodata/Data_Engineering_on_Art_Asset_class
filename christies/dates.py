from dateutil import parser

def rectify_dates(date_string):
    try:
        # Split the string to extract the start and end dates
        start_date_str, end_date_str = date_string.split(" - ")

        start_date_str, end_date_str = date_string.split(" - ")

        # Parse the dates
        start_date = parser.parse(start_date_str)

        end_date = parser.parse(end_date_str)

        # Get the maximum date
        last_date = max(start_date, end_date)

        # Format and print the last date
        formatted_date = last_date.strftime("%d %B")
        print(formatted_date)
        day,month = formatted_date.split(" ")
        print("The date is ",day,month)
        return day,month

    except:
        formatted_date = date_string
        print(formatted_date)
        day,month = formatted_date.split(" ")
        # print("The day is ",day)
        print("The date is ",day,month)
        return day,month
