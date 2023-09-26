import requests
import time

print(f"BTC PRICE")
# api key: b4de8a18-e523-457a-917b-78f8e6093bd9
# curl -H "X-CMC_PRO_API_KEY: b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c" -H "Accept: application/json" -d "start=1&limit=5000&convert=USD" -G https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest

# Define the API endpoint URL
# url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map"
# url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

# Define the headers
headers = {
    "X-CMC_PRO_API_KEY": "b4de8a18-e523-457a-917b-78f8e6093bd9",
    "Accept": "application/json"
}

# Define the query parameters
params = {
#    "start": 1,
#    "convert": "USD"
#    "limit": 5000,
    "id": 1 #BTC
}

start_time = time.time()

while True:
    # Send the GET request
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response content
    #    print(response.json())
        data = response.json()

        end_time = time.time()
        elapsed_time = end_time - start_time


        price_usd = data["data"]["1"]["quote"]["USD"]["price"]
        price_usd = int(price_usd)
        print(f"{price_usd} ({elapsed_time}s)")

    else:
        print(f"Request failed with status code {response.status_code}")

    time.sleep(10)

