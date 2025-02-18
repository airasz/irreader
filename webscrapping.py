import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Label, Button, Entry, Text, Scrollbar, END, RIGHT, Y


import json
import os.path

bg = "#ffffff"

urll = "https://www.goal.com/id/pertandingan/torino-vs-parma-calcio-1913/jreZNqxUooBMV_Z6ApGId"
count = 23


DATAFILE_ = "livescoredata.json"
classname = "match-data_score__xQ29z"
element = ""
lscore = ""

mscore = ""
mteam = ""


def scrape():
    url = url_entry.get()
    classname = entry_classname.get()
    element = entry_element.get()
    try:
        # Fetch the content from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad

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
        scores = soup.find_all(element, classname)
        scre = ""
        for score in scores:
            # scr=score.select_one("div.detailScore__wrapper detailScore__live span")
            # scr=score.select_one("div.match-data_match-data__HGwNh span")
            print(score)
            scre = score
            scr = score.select_one("." + classname)
            #
            # 	# text_area.delete(1.0, END)
            # text_area.insert(END,str(scr)+'\n')
            text_area.insert(END, score.get_text() + "\n")

        # soup = BeautifulSoup(scre, "html.parser")
        scoree = soup.find_all("sc")
        for ssc in scoree:
            info = ssc.get_text()
            text_area.insert(END, score.get_text() + "\n")
            print(ssc)
        # You can add more data extraction logic here
        # For example, to extract all paragraphs:
        # paragraphs = soup.find_all('p')
        # for p in paragraphs:
        #     text_area.insert(END, p.get_text() + '\n')

    except requests.exceptions.RequestException as e:
        text_area.delete(1.0, END)
        text_area.insert(END, f"Error: {e}")


def callback(event):
    # select text
    event.widget.select_range(0, "end")
    # move cursor to the end
    event.widget.icursor("end")
    # stop propagation
    return "break"

def custom_paste(event):
    try:
        event.widget.delete("sel.first", "sel.last")
    except:
        pass
    event.widget.insert("insert", event.widget.clipboard_get())
    return "break"


def loaddata():
    global urll
    global element
    global classname
    try:
        with open(DATAFILE_, "r") as f:
            data = json.load(f)
            urll = data.get("url", urll)
            element = data.get("element", element)
            classname = data.get("classname", classname)
    except FileNotFoundError:
        pass


loaddata()


def savedata():
    global urll
    global element
    global classname
    jdata = {"url": urll, "element": element, "classname": classname}
    with open(DATAFILE_, "w") as f:
        json.dump(jdata, f)


# Create the main window
root = Tk()
root.title("Web Scraper - Livescore") # Set the title of the window

# Create a label and entry for the URL
url_label = Label(root, text="Enter URL:")
url_label.pack()

url_entry = Entry(root, width=50)
url_entry.pack()
url_entry.bind("<Control-a>", callback)
url_entry.bind("<Control-v>", custom_paste)
url_entry.insert(
    END,
    urll,
)


# Create a label and entry for the URL
url_label_element = Label(root, text="Enter element type:")
url_label_element.pack()

entry_element = Entry(root, width=50)
entry_element.pack()
entry_element.bind("<Control-a>", callback)
entry_element.bind("<<Paste>>", custom_paste)
entry_element.insert(END, element)


# Create a label and entry for the URL
url_label1 = Label(root, text="Enter class name:")
url_label1.pack()

entry_classname = Entry(root, width=50)
entry_classname.pack()
entry_classname.bind("<Control-a>", callback)
entry_classname.bind("<<Paste>>", custom_paste)
entry_classname.insert(END, classname)

# Create a button to trigger scraping
scrape_button = Button(root, text="Scrape", command=scrape)
scrape_button.pack()

# Create a button to trigger scraping
save_button = Button(root, text="Save", command=savedata)
save_button.pack()


# Create a text area with scrollbar to display results
text_area = Text(root, width=60, height=20)
text_area.pack()

scrollbar = Scrollbar(root, command=text_area.yview)
scrollbar.pack(side=RIGHT, fill=Y)
text_area.config(yscrollcommand=scrollbar.set)

# photo = Tk.PhotoImage(file = 'Soccer-Ball-icon.png')
# root.wm_iconphoto(False, photo)

# Start the Tkinter main loop
root.mainloop()
