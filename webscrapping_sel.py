from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Label, Button, Entry, Text, Scrollbar, END, RIGHT, Y
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


bg = "#ffffff"


def scrape():
    url = url_entry.get()
    classname = url_entry1.get()
    try:
        # Fetch the content from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad

        session = HTMLSession()

        resp = session.get(url)
        resp.html.render()
        html = resp.html.html

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the title of the webpage
        title = soup.title.string if soup.title else "No title found"

        # Clear the text area and insert the title
        text_area.delete(1.0, END)
        text_area.insert(END, f"Title: {title}\n")

        # titles=soup.find_all('title')
        # for title in titles:
        # 	text_area.insert(END, title.get_text() + '\n')

        # scores= soup.find_all('span')
        # for score in scores:
        # 	# scr=score.select_one("div.detailScore__wrapper detailScore__live span")
        # 	# scr=score.select_one("div.match-data_match-data__HGwNh span")
        # 	scr=score.select_one("scores")

        # 	# text_area.delete(1.0, END)
        # 	text_area.insert(END,str(scr)+'\n')

        for dom in soup.select("span.match-data_score__xQ29z"):
            print(dom.string)
        # rslt=soup.select(".detailScore__live.detailScore__wrapper")
        # print(rslt.get_text())
        # text_area.insert(END,str(rslt)+'\n')
        scores = soup.find_all("p", classname)
        for score in scores:
            # scr=score.select_one("div.detailScore__wrapper detailScore__live span")
            # scr=score.select_one("div.match-data_match-data__HGwNh span")
            print(score)
            scr = score.select_one("." + classname)
            #
            # 	# text_area.delete(1.0, END)
            # text_area.insert(END,str(scr)+'\n')
            text_area.insert(END, score.get_text() + "\n")
        # You can add more data extraction logic here
        # For example, to extract all paragraphs:
        # paragraphs = soup.find_all('p')
        # for p in paragraphs:
        #     text_area.insert(END, p.get_text() + '\n')

    except requests.exceptions.RequestException as e:
        text_area.delete(1.0, END)
        text_area.insert(END, f"Error: {e}")


# Create the main window
root = Tk()
root.title("Web Scraper")

# Create a label and entry for the URL
url_label = Label(root, text="Enter URL:")
url_label.pack()

url_entry = Entry(root, width=50)
url_entry.pack()
url_entry.insert(
    END,
    "https://idn00100.tigoals185.com/football/2701583-tokyo-verdy-vs-shimizu-spulse.html",
)

# Create a label and entry for the URL
url_label1 = Label(root, text="Enter class name:")
url_label1.pack()

url_entry1 = Entry(root, width=50)
url_entry1.pack()
url_entry1.insert(END, "detail__tscore")

# Create a button to trigger scraping
scrape_button = Button(root, text="Scrape", command=scrape)
scrape_button.pack()

# Create a text area with scrollbar to display results
text_area = Text(root, width=60, height=20)
text_area.pack()

scrollbar = Scrollbar(root, command=text_area.yview)
scrollbar.pack(side=RIGHT, fill=Y)
text_area.config(yscrollcommand=scrollbar.set)

# Start the Tkinter main loop
root.mainloop()
