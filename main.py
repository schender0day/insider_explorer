import requests
import json
from datetime import datetime, timedelta


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

def main():
    with open("api_token.txt", "r") as f:
        api_token = f.read().strip()

    insider_updates = InsiderUpdates(api_token, "AAPL")

    date = datetime.now().date()
    filtered_data_list = []
    for i in range(5):
        data = insider_updates.get_data(date.strftime('%Y-%m-%d'))
        filtered_data = insider_updates.filter_by_value(data, 200000)
        filtered_data_list.append(filtered_data)
        date -= timedelta(days=1)

    combined_response = combine_responses(filtered_data_list)
    print(f"Number of transactions found: {len(combined_response)}")
    print(json.dumps(combined_response, indent=4))


if __name__ == '__main__':
    main()
