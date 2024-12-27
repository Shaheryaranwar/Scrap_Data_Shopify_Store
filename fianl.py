import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Base URL for the product category
base_url = "https://flavorpin.com/product-category/xtra-vape/"
pagination_url = "https://flavorpin.com/product-category/xtra-vape/{}/"

# Generate a unique folder name using timestamp
folder_name = f"product_images_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(folder_name, exist_ok=True)
print(f"Images will be saved in folder: {folder_name}")

# Start scraping pages
page_number = 1

while True:
    # Construct URL for the current page
    if page_number == 1:
        url = base_url
    else:
        url = pagination_url.format(page_number)

    print(f"Scraping page: {url}")

    try:
        # Fetch the page content
        response = requests.get(url)
        response.raise_for_status()  # Raise error for HTTP issues
        html_content = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_number}: {e}")
        break

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    products = soup.find_all('div', class_='box-image')

    # Break if no products found (end of pagination)
    if not products:
        print("No more products found. Ending scraping.")
        break

    # Loop through each product on the page
    for product in products:
        # Extract the product name
        name_tag = product.find('a', {'aria-label': True})
        product_name = name_tag['aria-label'] if name_tag else 'N/A'

        # Extract the image URL
        img_tag = product.find('img')
        image_url = img_tag['src'] if img_tag else None

        if image_url:
            # Get the file name from the URL
            file_name = os.path.basename(image_url)
            file_path = os.path.join(folder_name, file_name)

            try:
                # Download the image
                img_response = requests.get(image_url)
                img_response.raise_for_status()

                # Save the image locally
                with open(file_path, 'wb') as f:
                    f.write(img_response.content)
                print(f"Image saved: {file_path}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {image_url}: {e}")

        # Print product details
        print(f"Product Name: {product_name}")
        print(f"Image URL: {image_url}")
        print("-" * 40)

    # Move to the next page
    page_number += 1
