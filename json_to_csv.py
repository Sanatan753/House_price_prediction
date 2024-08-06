import pandas as pd
import json

# Define the file paths
json_file_path = 'D:/House_price_prediction/Data.json'
csv_file_path = 'D:/House_price_prediction/House_pricing.csv'

# Read the JSON file
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract the required data and normalize it
records = []
for item in data:
    record = item['content']
    record['srp'] = item['srp']
    records.append(record)

# Create a DataFrame from the records
df = pd.DataFrame(records)

# Save the DataFrame to a CSV file
df.to_csv(csv_file_path, index=False)

print("CSV file created successfully.")
