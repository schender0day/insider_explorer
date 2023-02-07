import requests
import json
from datetime import datetime, timedelta


class InsiderUpdates:
    def __init__(self, api_token: str, symbol: str):
        self.api_token = api_token
        self.symbol = symbol

    def filter_by_value(self, data, value_lower_bound: float):
        filtered_data = []
        for item in data:
            # Only include transactions with type "P" (Purchase)
            if item['type'] != "S":
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


def main():
    with open("api_token.txt", "r") as f:
        api_token = f.read().strip()

    insider_updates = InsiderUpdates(api_token, "AAPL")
    data = insider_updates.get_data()
    filtered_data = insider_updates.filter_by_value(data, 1000000)
    print(f"Number of transactions found: {len(filtered_data)}")
    print(json.dumps(filtered_data, indent=4))


if __name__ == '__main__':
    main()
