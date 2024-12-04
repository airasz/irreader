import requests
from bs4 import BeautifulSoup

import threading
import json
#!/usr/bin/python
import serial
from time import sleep

sport=''
def cekport():
    global sport
    output = result= subprocess.check_output("dmesg | grep tty", shell=True)
    tty =  output.decode("utf-8")
    if "ttyUSB" in tty:
       itty=tty.index("ttyUSB")
       sport = '/dev/'+tty[itty:(itty+7)]
       # sport = '/dev/ttyUSB0'
    else:
       sport = '/dev/ttyS1'

cekport()
con = serial.Serial(
    port=sport,
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)


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

		for dom in soup.select("span.match-data_score__xQ29z"):
			print(dom.string)
		scores= soup.find_all('span',classname)
		for score in scores:
			print(score)
			scr=score.select_one("."+classname)
			text_area.insert(END,score.get_text()+'\n')

	except requests.exceptions.RequestException as e:
		text_area.delete(1.0, END)
		text_area.insert(END, f"Error: {e}")
        