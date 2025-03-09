import tornado.ioloop
import tornado.web
from bs4 import BeautifulSoup
import requests
import asyncio
import serialdisplay
import tornado.httpclient
from time import sleep
import json
import os.path

urll = "https://www.goal.com/id/pertandingan/torino-vs-parma-calcio-1913/jreZNqxUooBMV_Z6ApGId"
count = 23

DATAFILE_ = "livescore_data.json"
display = serialdisplay.display()
classname = "match-data_score__xQ29z"
lscore = ""

mscore = ""
mteam = ""

TMP_HT = 0
SHT = ""
TMP_FT = 0
SFT = ""
OLD_MNT = ""


def interuptDisplay(msg):
    display.display(msg, False)
    # display.frezeeDisplay(5)


# Tornado Folder Paths
settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Web Scraper Running! Check the terminal for scraping logs.")
        self.render("webscr.html", wsurl=urll)

    async def post(self):
        global count
        global urll
        global TMP_HT
        global SHT
        global SFT
        global TMP_FT
        url = ""
        try:
            value = self.get_argument("url")
            print("url " + value)
        except:
            print("skiping cause argument not contain " + value)
            return
        if value != "":
            url = value
            if not url:
                self.write({"error": "Please provide a URL"})
                return
            urll = url
            interuptDisplay("#blink=1")
            count = 24
            # result = await fetch_and_scrape(url)
            scraper = Scraper(url)
            # self.write("url saved")
            jdata = {"url": urll}
            with open(DATAFILE_, "w") as f:
                json.dump(jdata, f)

            # pass
        # ok()
        self.render("webscr.html", wsurl=urll)


# Tornado request handler
class ScrapeHandler(tornado.web.RequestHandler):
    async def get(self):
        global count
        global urll
        url = self.get_argument("url", urll)
        if not url:
            self.write({"error": "Please provide a URL"})
            return
        urll = url
        count = 24
        # result = await fetch_and_scrape(url)
        scraper = Scraper(url)
        self.write("url saved")


class Scraper:
    def __init__(self, url):
        self.url = url

    async def scrape(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        global count
        global urll
        global lscore
        global mscore
        global mteam
        global TMP_HT
        global SHT
        global SFT
        global TMP_FT
        global OLD_MNT
        count += 1
        if count == 5:
            # inte  ruptDisplay("resetscreen")
            pass
        if count % 10 == 0:
            interuptDisplay(lscore)
        if count > 25:
            count = 0
            sblink = 0
            try:


                # Fetch JSON data from JSONPlaceholder
                url = "https://cfapi.n2ew2a2pia.com/gatebd3b0e8531c52da6632e1fedb98524e8472a416a76232a5e426953a9dc/api/ftb/detail?d=idn00144.tigoals180.com&lang=4&id=2591173"
                response = requests.get(urll)

                if response.status_code == 200:
                    data = response.json()
                    # print(data)  # Print the entire list of posts

                    tm = ""
                    # Example: Print the title of the first post
                    if len(data) > 0:
                        tm= data['match']['homeName'] + " vs " + data['match']['awayName']
                        scr=str(data['match']['homeScore']) + " - " + str(data['match']['awayScore'])
                        lscore = tm + "\n " + '0' + " > " + scr
                        # interuptDisplay(lscore)
                        # print("Home score:", data['match']['homeScore'])
                else:
                    print(f"Failed to fetch data: {response.status_code}")

            except Exception as e:
                print(f"Error during scraping: {e}")

    async def scraping(self):
        global count
        global urll
        global classname
        count += 1
        if count > 10:
            count = 0
            try:
                # Send HTTP GET request
                response = requests.get(self.url)
                response.raise_for_status()  # Raise an error for bad HTTP responses

                # Parse HTML content
                soup = BeautifulSoup(html, "html.parser")
                title = soup.title.string if soup.title else "No title found"
                scores = soup.find_all("span", classname)
                for score in scores:
                    # print(score)
                    scr = score.select_one("." + classname)
                # serialdisplay(score.get_text())
                result = score.get_text()
                print("result = " + result)
            except Exception as e:
                print(f"Error during scraping: {e}")


async def periodic_scraping(scraper):
    while True:
        await scraper.scrape()
        await asyncio.sleep(1)  # Wait for 1 second before the next scrape


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/scrape", ScrapeHandler),
            # (r"/(.*)", tornado.web.StaticFileHandler, {"path": "/root/static"}),
            (r"/(.*)", tornado.web.StaticFileHandler, {"path": ".//static"}),
        ],
        **settings,
    )


def loaddata():
    global urll
    try:
        with open(DATAFILE_, "r") as f:
            data = json.load(f)
            urll = data.get("url", urll)
    except FileNotFoundError:
        pass


loaddata()
if __name__ == "__main__":
    # global urll

    # interuptDisplay("dmode0")
    url_to_scrape = urll  # Replace with the target website
    scraper = Scraper(url_to_scrape)

    app = make_app()
    app.listen(8890)
    try:
        # Start periodic scraping task
        tornado.ioloop.IOLoop.current().spawn_callback(periodic_scraping, scraper)
        sleep(0.4)
        interuptDisplay("#dmode=0")
        sleep(0.3)
        # interuptDisplay("#setnote=NOTE_B7")
        sleep(0.4)
        interuptDisplay("#resetscreen")
        print("Starting Tornado server on http://localhost:8890")
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Keyboard interrupt received, exiting...")
