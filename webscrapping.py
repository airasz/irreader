import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Label, Button, Entry, Text, Scrollbar, END, RIGHT, Y

def scrape():
	url = url_entry.get()
	try:
		# Fetch the content from the URL
		response = requests.get(url)
		response.raise_for_status()  # Raise an error for bad responses
		soup = BeautifulSoup(response.text, 'html.parser')

		# Extract the title of the webpage
		title = soup.title.string if soup.title else 'No title found'

		# Clear the text area and insert the title
		text_area.delete(1.0, END)
		text_area.insert(END, f"Title: {title}\n")

		# titles=soup.find_all('title')
		# for title in titles:
		# 	text_area.insert(END, title.get_text() + '\n')


		scores= soup.find_all('span')
		for score in scores:
			# scr=score.select_one("div.detailScore__wrapper detailScore__live span")
			# scr=score.select_one("div.match-data_match-data__HGwNh span")
			scr=score.select_one("scores")

			# text_area.delete(1.0, END)
			text_area.insert(END,str(scr)+'\n')


		# scores= soup.find_all('section')
		# for score in scores:
		# 	# scr=score.select_one("div.detailScore__wrapper detailScore__live span")
		# 	# scr=score.select_one("div.match-data_match-data__HGwNh span")
		# 	scr=score.select_one("span.match-data_score__xQ29z")
  #
		# 	# text_area.delete(1.0, END)
		# 	text_area.insert(END,str(scr)+'\n')
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
url_entry.insert(END, "https://www.goal.com/en/match/persis-solo-vs-barito-putera/BVyTg6WsRIJTipedxMoGF")

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
