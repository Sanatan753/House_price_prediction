import pandas as pd
import re
import numpy as np
from datetime import datetime

# Load the CSV file
df = pd.read_csv('simplifieddata.csv')

# Define keywords and threshold for nearby places
places_keywords = {
    'Airport': ['airport'],
    'Hospital': ['hospital', 'clinic', 'medical'],
    'Market': ['market', 'mall', 'supermarket']
}
distance_threshold = 5  # km

# Function to extract and check if a place is within the threshold
def check_nearby_places(row, place):
    nearby_places = row['nearby_places']
    
    # Ensure nearby_places is a string
    if isinstance(nearby_places, str):
        # Search for the place keyword in the nearby_places column
        place_mentioned = any(keyword in nearby_places.lower() for keyword in places_keywords[place])
        if place_mentioned:
            # Extract the distance using regex
            match = re.search(r'(\d+\.?\d*)\s*km', nearby_places)
            if match:
                distance = float(match.group(1))
                return 1 if distance <= distance_threshold else 0
    return 0

# Apply the function to each place
for place in places_keywords.keys():
    df[place] = df.apply(lambda row: check_nearby_places(row, place), axis=1)

# Function to extract unique BHK types
def extract_bhk_types(room_info):
    if isinstance(room_info, str):
        bhk_list = re.findall(r'(\d)\s*BHK', room_info)
        return ','.join(bhk_list)
    return ''

# Apply the function to create room types
df['room_types'] = df['room_info'].apply(extract_bhk_types)

# Split the room_types into separate columns for each BHK type
for bhk in ['2','3', '4', '5']:
    df[bhk + ' BHK'] = df['room_types'].apply(lambda x: 1 if bhk in x else 0)

# Function to handle missing room_info by setting a default value
def handle_missing_room_info(room_info):
    if pd.isna(room_info) or room_info.strip() == '':
        return '3 BHK'
    return room_info

# Apply the function to handle missing room_info
df['room_info'] = df['room_info'].apply(handle_missing_room_info)

# Reapply the BHK type extraction to reflect any changes
df['room_types'] = df['room_info'].apply(extract_bhk_types)

# Function to extract the size (sq.ft) from the string
def extract_size(size_info):
    if isinstance(size_info, str):
        size = re.findall(r'(\d+)', size_info)
        if size:
            return int(size[0])
    return np.nan

# Apply the function to create size_info_numeric
df['size_info_numeric'] = df['size_info'].apply(extract_size)

# Define default size
default_sizes = {
    '2 BHK': 1200,
    '3 BHK': 1500,
    '4 BHK': 2800,
    '5 BHK': 4760
}

# Fill missing room_info with '3 BHK'
df['room_info'].fillna('3 BHK', inplace=True)

# Ensure that size_info_numeric is set correctly if it's missing
df['size_info_numeric'].fillna(default_sizes.get('3 BHK', np.nan), inplace=True)

# Convert size_info to numeric values
df['size_info_numeric'] = df['size_info'].apply(extract_size)

# Function to extract and assign size based on room_info
def assign_size(row):
    room_info = row['room_info']
    if isinstance(room_info, str):
        if '5 BHK' in room_info:
            return 4760
        elif '4 BHK' in room_info:
            return 2800
        elif '3 BHK' in room_info:
            return 1500
        elif '2 BHK' in room_info:
            return 1200
        elif '1 BHK' in room_info:
            return 900
    return np.nan

# Apply the function to create size_info_numeric
df['size_info_numeric'] = df.apply(assign_size, axis=1)

# Function to convert EMI to total amount over a 5-year period
def emi_to_total_amount(emi_str, tenure_years=5):
    if isinstance(emi_str, str):
        emi_str = emi_str.replace('₹', '').replace(',', '').strip()
        if 'K' in emi_str:
            emi_amount = float(emi_str.replace('K', '')) * 1000
        else:
            emi_amount = float(emi_str)
        return emi_amount * 12 * tenure_years
    return np.nan

# Function to convert price to float
def convert_price(price_str):
    if isinstance(price_str, str):
        price_str = price_str.replace('₹', '').replace(',', '').strip()
        if 'Cr' in price_str:
            if 'CrEMI' in price_str:
                return float(price_str.replace('CrEMI', '').strip()) * 600000000
            return float(price_str.replace('Cr', '').strip()) * 10000000
        elif 'L' in price_str:
            if 'LEMI' in price_str:
                return float(price_str.replace('LEMI', '').strip()) * 6000000
            return float(price_str.replace('L', '').strip()) * 100000
    return np.nan

# Function to extract price range from main_info
def extract_price_range(main_info):
    if isinstance(main_info, str):
        # Extract standard price ranges
        price_range = re.findall(r'₹([\d.,]+)\s*(Cr|L)', main_info)
        if len(price_range) == 2:
            min_price = float(price_range[0][0].replace(',', '')) * (10000000 if price_range[0][1] == 'Cr' else 100000)
            max_price = float(price_range[1][0].replace(',', '')) * (10000000 if price_range[1][1] == 'Cr' else 100000)
            return min_price, max_price
        
        # Extract prices following 'starts at'
        starts_at_price = re.search(r'starts at ₹([\d.,]+)\s*(Cr|L)', main_info)
        if starts_at_price:
            price = float(starts_at_price.group(1).replace(',', ''))
            if starts_at_price.group(2) == 'Cr':
                return price * 10000000, price * 10000000  # Set both min and max to the same if only starts at price is present
            elif starts_at_price.group(2) == 'L':
                return price * 100000, price * 100000  # Set both min and max to the same if only starts at price is present
        
        # Extract EMI values
        emi_value = re.search(r'EMI starts at ₹([\d.,]+)\s*(K|L)?', main_info)
        if emi_value:
            emi_total = emi_to_total_amount(emi_value.group(1) + (emi_value.group(2) if emi_value.group(2) else ''))
            return emi_total, emi_total  # Set both min and max to the same if only EMI value is present

    return np.nan, np.nan

# Function to handle missing prices
def handle_missing_prices(price_info, min_price, max_price):
    if pd.isna(min_price):
        if pd.isna(max_price):
            max_price = convert_price(price_info)
            if isinstance(price_info, str):  # Ensure price_info is a string
                if 'Cr' in price_info:
                    min_price = max_price - 500000  # Subtract ₹5 Lakhs
                elif 'L' in price_info:
                    min_price = max_price - 50000  # Subtract ₹50,000
            else:
                min_price = np.nan  # Set min_price to NaN if price_info is not a string
        else:
            if isinstance(price_info, str):  # Ensure price_info is a string
                min_price = max_price - 500000 if 'Cr' in price_info else max_price - 50000
    elif pd.isna(max_price):
        max_price = convert_price(price_info)
        if isinstance(price_info, str):  # Ensure price_info is a string
            min_price = max_price - 500000 if 'Cr' in price_info else max_price - 50000

    return min_price, max_price

# Apply the function to create min_price and max_price columns
df['min_price'], df['max_price'] = zip(*df['main_info'].apply(extract_price_range))

# Handle missing prices
df['min_price'], df['max_price'] = zip(*df.apply(lambda row: handle_missing_prices(row['price_info'], row['min_price'], row['max_price']), axis=1))

# Function to calculate Sales_price
def calculate_sales_price(row):
    min_price = row['min_price']
    max_price = row['max_price']
    default_price = row['price_info']
    
    # If both min_price and max_price are valid, calculate the average
    if pd.notna(min_price) and pd.notna(max_price) and min_price > 0 and max_price > 0:
        return (min_price + max_price) / 2
    else:
        # If either is missing or 0, use the default price
        return convert_price(default_price)

# Apply the function to create the Sales_price column
df['Sales_price'] = df.apply(calculate_sales_price, axis=1)

# Convert Sales_price to numeric (float) to ensure proper data type
df['Sales_price'] = pd.to_numeric(df['Sales_price'], errors='coerce')

# Remove rows where Sales_price is NaN or zero
df = df[df['Sales_price'].notna() & (df['Sales_price'] != 0)]

# Function to extract the possession year
def extract_possession_year(possession_info):
    if isinstance(possession_info, str):
        match = re.search(r'(\w{3}),?\s*(\d{4})', possession_info)
        if match:
            return int(match.group(2))
    return np.nan

# Apply the function to create possession_year and time_to_possession
df['possession_year'] = df['possession_info'].apply(extract_possession_year)

# Fill missing possession_year with 2026
df['possession_year'].fillna(2026, inplace=True)

current_year = datetime.now().year
df['time_to_possession'] = df['possession_year'] - current_year

# Function to identify property types (Flat, Duplex, Apartment)
def identify_property_type(main_info):
    if isinstance(main_info, str):
        # Check for keywords in the main_info
        is_flat = 1 if re.search(r'\bflat\b', main_info.lower()) else 0
        is_duplex = 1 if re.search(r'\bduplex\b', main_info.lower()) else 0
        is_apartment = 1 if re.search(r'\bapartment\b', main_info.lower()) else 0
        return is_flat, is_duplex, is_apartment
    return 0, 0, 0  # Default if no match

# Apply the function to create is_flat, is_duplex, is_apartment columns
df['is_flat'], df['is_duplex'], df['is_apartment'] = zip(*df['main_info'].apply(identify_property_type))

# Apply the function to convert price_info
df['price_info'] = df['price_info'].apply(convert_price)

# Drop rows where price_info is NaN or zero
df = df[df['price_info'].notna() & (df['price_info'] > 0)]

# Save the transformed CSV
df.to_csv('transformed_file.csv', index=False)

print("Transformation complete and CSV saved as 'transformed_file.csv'.")
