import requests
from bs4 import BeautifulSoup

url = "https://www.trendyol.com/immunace/original-30-tablet-multivitamin-p-6476572?merchantId=753766"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Find the elements containing the price and seller name
price_element = soup.find("span", class_="prc-slg")
seller_element = soup.find("span", class_="seller-name")

# Extract the text from the elements
if price_element:
    price = price_element.get_text(strip=True)
else:
    price = "Price not found"

if seller_element:
    seller = seller_element.get_text(strip=True)
else:
    seller = "Seller name not found"

# Print the results
print("Product Price:", price)
print("Seller Name:", seller)
