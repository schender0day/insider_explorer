import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import os
import openpyxl


class InsiderUpdates:
    def __init__(self, api_token: str, symbol: str):
        self.api_token = api_token
        self.symbol = symbol

    def filter_by_value(self, data, value_lower_bound: float):
        filtered_data = []
        us_exchange = ['NYSE', 'NAS']
        for item in data:
            # Only include transactions with type "P" (Purchase)
            if item['type'] != "S" and item['exchange'] in us_exchange:
                # Calculate the value of the transaction
                trans_value = item['cost'] * item['trans_share']
                # Only include transactions with value greater than the lower bound

                if trans_value >= value_lower_bound:
                    filtered_data.append(item)
                trans_value = '{:,.2f}'.format(trans_value)
                item['total_value'] = trans_value
        return filtered_data

    def get_data(self, date: str = None):
        if date is None:
            today = datetime.now().date()
            start_date = today
        else:
            start_date = date

        endpoint = f"https://api.gurufocus.com/public/user/{self.api_token}/insider_updates?page=1&date={start_date}"

        # Make the API request
        response = requests.get(endpoint)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON data from the response
            data = response.json()
            return data

def combine_responses(responses):
    combined_response = []
    for response in responses:
        combined_response += response
    return combined_response

def open_link(symbol):
    symbol = symbol.split(":")[1]
    link = f"https://www.google.com/search?q={symbol}"
    link += "+stock"
    return link


def export_to_excel(data):
    # Create a new workbook
    workbook = openpyxl.Workbook()

    # Select the active worksheet
    worksheet = workbook.active

    # Write the header row
    worksheet.append(["Symbol", "Exchange", "Position", "Date", "Type", "Trans Share", "Final Share", "Price", "Cost", "Insider", "Total Value", "Link"])

    # Write the data rows
    for item in data:
        worksheet.append([item["symbol"], item["exchange"], item["position"], item["date"], item["type"], item["trans_share"], item["final_share"], item["price"], item["cost"], item["insider"], item["total_value"], item["link"]])

    # Make the Link column a hyperlink
    for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, min_col=12, max_col=12):
        for cell in row:
            cell.hyperlink = cell.value
            cell.value = f"{cell.value}"

    # Save the workbook
    workbook.save("insider_updates.xlsx")

def main():
    with open("api_token.txt", "r") as f:
        api_token = f.read().strip()

    insider_updates = InsiderUpdates(api_token, "AAPL")

    date = datetime.now().date()
    filtered_data_list = []
    for i in range(2):
        data = insider_updates.get_data(date.strftime('%Y-%m-%d'))
        filtered_data = insider_updates.filter_by_value(data, 200000)
        filtered_data_list.append(filtered_data)
        date -= timedelta(days=1)

    combined_response = combine_responses(filtered_data_list)
    for item in combined_response:
        item['link'] = open_link(item['symbol'])

    print(f"Number of transactions found: {len(combined_response)}")
    print(json.dumps(combined_response, indent=4))
    export_to_excel(combined_response)

if __name__ == '__main__':
    main()
