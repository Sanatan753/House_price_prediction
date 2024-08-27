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

## Notes

- The script is configured to scrape up to 2000 listings, but you can adjust this limit by modifying the loop in the `fetchAndSaveToFile` function.
- Ensure that you comply with the website's `robots.txt` and terms of service when scraping data.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to create a pull request or open an issue.
pls do find any issue 