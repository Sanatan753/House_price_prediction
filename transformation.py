import pandas as pd
import re

# Load the CSV file
df = pd.read_csv('simplifieddata.csv')

# Define keywords and threshold
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
                return 'Yes' if distance <= distance_threshold else 'No'
    return 'No'

# Apply the function to each place
for place in places_keywords.keys():
    df[place] = df.apply(lambda row: check_nearby_places(row, place), axis=1)

# Save the transformed CSV
df.to_csv('transformed_file.csv', index=False)
