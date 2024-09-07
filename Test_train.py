import pandas as pd
from sklearn.model_selection import train_test_split

# Load the transformed CSV file
df = pd.read_csv('transformed_file.csv')

# Split the data into training and testing sets (80-20 split)
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Save the training and testing datasets to separate CSV files
train_df.to_csv('train.csv', index=False)
test_df.to_csv('test.csv', index=False)

print("Data has been split into 'train.csv' and 'test.csv'.")
