import os
import json
import csv
from data_loader import insert_data_to_db


def read_data_from_json(json_file):
    with open(json_file, "r") as file:
        return json.load(file)


def read_data_from_csv(csv_file):
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
        return insert_data_to_db(data, 1000, "File")


def load_data_from_file(file_name):
    if not os.path.isfile(file_name):
        print("File not found.")
        return

    if file_name.endswith(".json"):
        print(f"The file uploaded is: {file_name}")
        data = read_data_from_json(file_name)
        if data:
            insert_data_to_db(data["data"], batch_size=1000, data_source="File", file_name=file_name)
        else:
            print("No data loaded.")

    elif file_name.endswith(".csv"):
        data = read_data_from_csv(file_name)
    else:
        print("Unsupported file format. Please provide either a JSON or CSV file.")
        return

    print("Data loaded successfully.")


if __name__ == "__main__":
    load_data_from_file()
