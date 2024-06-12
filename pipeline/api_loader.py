import os
import requests
import psycopg2
import json
from dotenv import load_dotenv
from datetime import datetime
from data_loader import insert_data_to_db

# Load environment variables from .env file
load_dotenv()

# API endpoint and bearer token from environment variables
API_URL = os.getenv('API_URL')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

# Function to get data from API
def get_data_from_api():
    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}',
        'Content-Type': 'application/json',
    }
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()['data']


# Main function
def main():
    try:
        print("Requesting the Vyaguta API for the data.")
        data = get_data_from_api()
        print(f"Data successfully received from API.")

        print("Inserting the data into `raw_leave_data` table.")
        insert_data_to_db(data, 1000, 'API')
        print(f"Data successfully inserted into the database. - {len(data)}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the API request: {e}")
    except psycopg2.Error as e:
        print(f"An error occurred while interacting with the database: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
