import tornado.ioloop
import tornado.web
from bs4 import BeautifulSoup
import requests
import feedparser
import asyncio
import serialdisplay
import tornado.httpclient
import json
import os.path
from time import sleep
from colorama import init, Fore, Back, Style

urll = "https://www.bola.net/feed/"
itemcount = 0
rest = 0
maxrest = 5
rsssitecount = 0
DATAFILE_ = "rssdata.json"
classname = "match-data_score__xQ29z"
lscore = "0-0"

mscore = "0-0"
mteam = ""


forecol = [
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.CYAN,
    Fore.WHITE,
]
init(autoreset=True)

# def interuptDisplay(msg):
#     display.display(msg, False)
# Tornado Folder Paths
settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
)


display = serialdisplay.display()


def loaddata():
    global urll
    global SITEDATA
    SITEDATA = []
    try:
        with open(DATAFILE_, "r") as f:
            data = json.load(f)
            rssdata = data.get("url", "")
            # urll = data.get("url", urll)
            sitelist = "rss site to read:\n"
            siteindex = 0
            for item in rssdata:
                # print("rss data:"+ str(item["name"]))
                if item["enable"] is True:
                    siteindex += 1
                    sitelist += f'\n{str(siteindex)}. {str(item["name"])}'
                    SITEDATA.append(item)
                    # j=json.dumps(SITEDATA)
                    # print(j)
            display.display(sitelist, False)
    except FileNotFoundError:
        pass


loaddata()
sleep(1)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Web Scraper Running! Check the terminal for scraping logs.")
        self.render("webscr.html", wsurl=urll)

    async def post(self):
        global itemcount
        global urll
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
            itemcount = -1
            # result = await fetch_and_scrape(url)
            scraper = Scraper(url)
            # MyNextion.send_command(f'g0.txt="{urll}"')
            fetch_rss_feed(urll)
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
        global itemcount
        global urll
        url = self.get_argument("url", urll)
        if not url:
            self.write({"error": "Please provide a URL"})
            return
        urll = url
        itemcount = 24
        # result = await fetch_and_scrape(url)
        scraper = Scraper(url)
        self.write("url saved")


rss_items = []


def fetch_rss_feed(urll):
    global rss_items
    global entriess
    # Parse the RSS feed
    feed = feedparser.parse(urll)

    # Create a list to store the titles and links

    rss_items = []  # reset
    # Loop through each entry in the feed
    for entry in feed.entries:
        # Create a formatted string for each entry
        # item_string = f"Title: {entry.title}Des: {entry.description}"
        # item_string = f"Title: {entry.title}"
        content = entry.description
        if "/>" in content:
            item_string = f'Title: {content[content.index("/>")+2:]}'
        else:
            item_string = f"Title: {content}"
        # item_string = f"publish Date: {entry.pubDate}\nTitle: {entry.title}"
        # Append the string to the list
        rss_items.append(item_string)
    print(f"got total {len(rss_items)} entries")

    entriess = str(len(rss_items))
    # MyNextion.send_command(f't2.txt="{entriess}"')
    return rss_items


class Scraper:
    def __init__(self, url):
        self.url = url

    async def fetch_rss_feed(self, urll):
        global rss_items
        # Parse the RSS feed
        feed = feedparser.parse(urll)

        # Create a list to store the titles and links

        # Loop through each entry in the feed

        for entry in feed.entries:
            # Create a formatted string for each entry
            item_string = f"Title: {entry.description}"
            print(f"Title: {entry.description}")
            # Append the string to the list
            rss_items.append(item_string)

        return rss_items

    async def scrape(self):
        global rss_items
        http_client = tornado.httpclient.AsyncHTTPClient()
        global itemcount
        global urll
        global lscore
        global mscore
        global mteam
        global rsssitecount
        global rest
        global maxrest
        global entriess

        rest += 1
        # print(f'rest:{rest}')

        if rest > maxrest:
            itemcount += 1
            Title = ""
            if itemcount < (len(rss_items)):
                serdata = rss_items[itemcount].replace("Title: ", "")
                serdata += "\n"
                # interuptDisplay(serdata)
                display.display(serdata, False)
                print(f"{forecol[rsssitecount]}{itemcount}. {serdata}")
            else:
                print("reach maximum")
                itemcount = 0
                # fetch_rss_feed(urll)
                fetch_rss_feed(SITEDATA[rsssitecount]["url"])
                print(
                    f'fetching site no : {rsssitecount} > {(SITEDATA[rsssitecount]["name"])}'
                )
                rsssitecount += 1
                if rsssitecount == len(SITEDATA):
                    rsssitecount = 0
            Title = rss_items[itemcount]
            if len(Title) > 10:
                maxrest = int(len(Title) / 10)
            print(f"lengt:{len(Title)} | maxrest:{maxrest}")
            rest = 0


async def periodic_scraping(scraper):
    while True:
        await scraper.scrape()
        await asyncio.sleep(1)  # Wait for 1 second before the next scrape


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/scrape", ScrapeHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, {"path": "/root/static"}),
        ],
        **settings,
    )


# scraper.fetch_rss_feed(urll)
if __name__ == "__main__":
    url_to_scrape = urll  # Replace with the target website
    scraper = Scraper(url_to_scrape)
    # interuptDisplay("dmode1")#typing efffect
    display.display("dmode1", False)
    sleep(4)
    fetch_rss_feed(SITEDATA[rsssitecount]["url"])
    print(f'fetching site no : {rsssitecount+1} > {(SITEDATA[rsssitecount]["name"])}')

    rsssitecount += 1
    if rsssitecount == len(SITEDATA):
        rsssitecount = 0

    app = make_app()
    app.listen(8890)

    # Start periodic scraping task

    try:
        tornado.ioloop.IOLoop.current().spawn_callback(periodic_scraping, scraper)

        print("Starting Tornado server on http://localhost:8890")
        tornado.ioloop.IOLoop.current().start()

    except KeyboardInterrupt:
        # ser.close()
        print("Keyboard interrupt received, exiting...")

# {"antara", "https://www.antaranews.com/rss/sepakbola", "title"}, // bisa m5c
#    // {"jawapos", "https://www.jawapos.com/sepak-bola/sepak-bola-dunia/feed/", "title"},
#    {"sindo", "https://sports.sindonews.com/rss", "title"},
#    {"okezone", "https://sindikasi.okezone.com/index.php/rss/14/RSS2.0", "title"},
#    {"oke tehno", "https://sindikasi.okezone.com/index.php/rss/16/RSS2.0", "title"},
#    {"oke news", "https://sindikasi.okezone.com/index.php/rss/1/RSS2.0", "title"},
#    {"oke break", "https://sindikasi.okezone.com/index.php/rss/0/RSS2.0", "title"}};
