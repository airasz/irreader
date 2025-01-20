from bs4 import BeautifulSoup
import requests

# Fetch the webpage
response = requests.get(
    "https://www.goal.com/en/match/juventus-vs-bologna/I7nhslu6_ZM8SCwkDXBXw"
)
soup = BeautifulSoup(response.content, "html.parser")

# Use CSS selector to find elements with the specified class name
elements = soup.select(".heading_teams__ljLuQ")  # Note the dot before the class name

# Iterate through the elements and get their inner HTML
for element in elements:
    inner_html = element.decode_contents()  # Get inner HTML
    print(inner_html)
