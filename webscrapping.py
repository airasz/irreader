import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Label, Button, Entry, Text, Scrollbar, END, RIGHT, Y
bg="#ffffff"
def scrape():
	url = url_entry.get()
	classname= url_entry1.get()
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
		scores= soup.find_all('span',classname)
		for score in scores:
			# scr=score.select_one("div.detailScore__wrapper detailScore__live span")
			# scr=score.select_one("div.match-data_match-data__HGwNh span")
			print(score)
			scr=score.select_one("."+classname)
  #
		# 	# text_area.delete(1.0, END)
			# text_area.insert(END,str(scr)+'\n')
			text_area.insert(END,score.get_text()+'\n')
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
url_entry.insert(END, "https://www.goal.com/en/match/cska-sofia-vs-spartak-varna/cLSNig4OSCyf2IEIDrahC")

# Create a label and entry for the URL
url_label1 = Label(root, text="Enter class name:")
url_label1.pack()

url_entry1 = Entry(root, width=50)
url_entry1.pack()
url_entry1.insert(END, "match-data_score__xQ29z")

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
