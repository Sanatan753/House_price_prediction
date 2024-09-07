# House_price_prediction
This program is for displaying information about  house pricing in the area 


# Web Scraper for Real Estate Listings

This project is a Python-based web scraper designed to extract detailed information about real estate listings from a specified URL using Selenium and BeautifulSoup. The scraper automates the process of loading, scrolling through, and parsing the web page to collect data such as price, room details, size, and nearby amenities. The extracted information is then saved in a structured JSON format.

## Features

- **Automated Web Scraping**: The scraper uses Selenium to navigate and scroll through web pages, ensuring that all dynamic content is loaded.
- **Data Extraction**: BeautifulSoup is used to parse the HTML content and extract relevant details such as:
  - Price Information
  - Room Details (e.g., number of BHKs)
  - Property Size
  - Possession Date
  - Main Property Description
  - Nearby Places and Amenities
- **JSON Output**: The scraped data is stored in a well-structured JSON file, making it easy to analyze or import into other applications.

## Requirements

To run this project, you'll need the following dependencies:

- Python 3.x
- Selenium
- BeautifulSoup4
- A compatible WebDriver (e.g., ChromeDriver for Chrome)

You can install the necessary Python packages using `pip`:

```bash
pip install selenium beautifulsoup4
```

Ensure that you have a compatible WebDriver installed and that it matches the version of your web browser. For Chrome, you can download ChromeDriver from [here](https://sites.google.com/chromium.org/driver/).

## Usage

1. **Set Up the WebDriver**: Download the WebDriver for your browser and make sure it's accessible in your system's PATH.

2. **Run the Script**: Execute the script by passing the target URL and the path where you want to save the HTML content. The script will automatically scroll through the page to load all listings and then extract the relevant information.

```python
url = "https://housing.com/in/buy/searches/P5m61sr2bx6q1gc1w"
fetchAndSaveToFile(url, "houseing.html")
```

3. **Extracted Data**: After the script completes, the extracted data will be saved in a file named `Data.json`.

## Example Output

The JSON output will have the following structure:

```json
[
    {
        "srp": "srp-1",
        "content": {
            "price_info": "₹1.47 Cr - 2.17 Cr",
            "room_info": "3 BHK",
            "size_info": "2160 sq.ft",
            "main_info": "Motwani Anantara",
            "possession_info": "Possession Date: Dec 2023",
            "nearby_places": "Jharapada, Bhubaneswar"
        }
    },
    ...
]
```

## Data Transformation Script

### Requirements

- Python 3.x
- `pandas`
- `numpy`
- `datetime`

You can install the necessary Python libraries using pip:

```bash
pip install pandas numpy
```

### Script Overview

**Transformation Steps:**

1. **Load Data:** Reads the CSV file (`simplifieddata.csv`) into a DataFrame.
2. **Process Nearby Places:** Checks and flags nearby places (Airport, Hospital, Market) within a specified distance.
3. **Extract Room Types:** Extracts and creates columns for different BHK types based on `room_info`.
4. **Handle Missing Values:** Sets default values for missing `room_info` and adjusts `size_info_numeric`.
5. **Price and Size Calculations:** Extracts price ranges and calculates sales prices. Converts and fills missing price values.
6. **Possession and Property Type:** Extracts possession year and calculates time to possession. Identifies property types (Flat, Duplex, Apartment).
7. **Save Transformed Data:** Saves the transformed DataFrame to a CSV file (`transformed_file.csv`).

**Functions:**

- `check_nearby_places(row, place)`: Checks if a place is within the distance threshold.
- `extract_bhk_types(room_info)`: Extracts BHK types from `room_info`.
- `handle_missing_room_info(room_info)`: Sets default room type if missing.
- `extract_size(size_info)`: Extracts numeric size from `size_info`.
- `assign_size(row)`: Assigns size based on `room_info`.
- `emi_to_total_amount(emi_str, tenure_years=5)`: Converts EMI to total amount.
- `convert_price(price_str)`: Converts price to numeric value.
- `extract_price_range(main_info)`: Extracts price range from `main_info`.
- `handle_missing_prices(price_info, min_price, max_price)`: Handles missing price values.
- `calculate_sales_price(row)`: Calculates sales price based on available price information.
- `extract_possession_year(possession_info)`: Extracts possession year from `possession_info`.
- `identify_property_type(main_info)`: Identifies property type based on `main_info`.

### Usage

1. Ensure the `simplifieddata.csv` file is present in the same directory as the script.
2. Run the script:

   ```bash
   python data_transformation_script.py
   ```

   Replace `data_transformation_script.py` with the name of your Python script file.

3. The script will process the data and save the cleaned data to `transformed_file.csv`.

## Notes

- The script is configured to scrape up to 2000 listings, but you can adjust this limit by modifying the loop in the `fetchAndSaveToFile` function.
- Ensure that you comply with the website's `robots.txt` and terms of service when scraping data.


Feel free to adjust the README based on additional requirements or details specific to your project.
## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to create a pull request or open an issue.
pls do find any issue 
