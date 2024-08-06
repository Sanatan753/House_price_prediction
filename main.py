import time
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def extract_info(content):
    # Extract price info
    price_info = re.search(r'₹[0-9.,]+\s*[A-Za-z]*', content)
    price_info = price_info.group(0) if price_info else ''

    # Extract possession info
    possession_info = re.search(r'Possession Date[A-Za-z,\s0-9]+', content)
    possession_info = possession_info.group(0) if possession_info else ''

    # Extract room info
    room_info = re.findall(r'[0-9]+(?:,\s[0-9]+)*\s*BHK', content)
    room_info = ', '.join(room_info) if room_info else ''

    # Extract size info
    size_info = re.findall(r'[0-9]+(?:,\s[0-9]+)*\s*(?:sq\.ft|sq\.m)', content)
    size_info = ', '.join(size_info) if size_info else ''

    # Extract main info and nearby places
    nearby_places_index = content.find('nearby places:')
    if nearby_places_index != -1:
        nearby_places = content[nearby_places_index + len('nearby places:'):].strip()
        main_info = content[:nearby_places_index].strip()
    else:
        nearby_places = ''
        main_info = content.strip()

    return {
        'price_info': price_info,
        'room_info': room_info,
        'size_info': size_info,
        'main_info': main_info,
        'possession_info': possession_info,
        'nearby_places': nearby_places
    }

def fetchAndSaveToFile(url,path):
    # Set up Selenium WebDriver (assuming Chrome here)
    driver = webdriver.Chrome()

    # Open the URL
    driver.get(url)

    # Scroll to load more content
    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Get page source and close the browser
    html = driver.page_source
    driver.quit()
    with open(path,"w",encoding="utf-8") as file:
        file.write(html)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    data = []
    # Find all div elements with data-pos attribute starting from srp-1 to srp-300
    for i in range(1,2000):
        div = soup.find('div', {'data-pos': f'srp-{i}'})
        if div:
            content = div.text.strip()
            extracted_info = extract_info(content)
            
            data.append({
                'srp': f'srp-{i}',
                'content': extracted_info
            })
    
    # Write data to a JSON file
    with open("Data.json", 'w', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    print("Data has been saved to Data.json")

url = "https://housing.com/in/buy/searches/P5m61sr2bx6q1gc1w"
fetchAndSaveToFile(url,"houseing.html")
