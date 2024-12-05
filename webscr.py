import tornado.ioloop
import tornado.web
from bs4 import BeautifulSoup
import requests
import asyncio

urll="https://www.goal.com/en/match/al-quwa-al-jawiya-vs-al-taawoun/VCix2AtlnY15A7y1Ix_OW"
count=0

classname="match-data_score__xQ29z"
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Web Scraper Running! Check the terminal for scraping logs.")

# Tornado request handler
class ScrapeHandler(tornado.web.RequestHandler):
    async def get(self):
        global count
        global urll
        url = self.get_argument("url", urll)
        if not url:
            self.write({"error": "Please provide a URL"})
            return
        urll=url
        count=24
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
        lscore=""
        count+=1
        if count>25:
            count =0
            try:
                # Send HTTP GET request
                # response = requests.get(self.url)
                # response.raise_for_status()  # Raise an error for bad HTTP responses
                response = await http_client.fetch(urll)
                html = response.body.decode('utf-8')  # Decode the HTML content
                # Parse HTML content
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.title.string if soup.title else 'No title found'

                # articles = soup.find_all("span")
                # for item in articles:
                #     print(item)
                #     category = item.select_one(".team_team-name__0U_gn span")  # <-- use item.select
                #     print(category)
                teams= soup.find_all('span', "heading_teams__ljLuQ")
                # teams=soup.select('span[data-testid="team-name"]')
                tm=""
                for team in teams:
                    # print(team['data-testid'])
                    # print("teamname"+team)
                    tmm=team.select_one("."+"heading_teams__ljLuQ")
                    tm+=team.get_text()
                    # tm=team.select_one("."+"team_team-name__0U_gn")
                minutes= soup.find_all('span', "match-period_period___hImu")
                mm=""
                for minut in minutes:
                    # print(mincute)
                    # mnt=minute.select_one("."+"match-period_period___hImu")
                    mm=minut.get_text()
                scores= soup.find_all('span',classname)
                for score in scores:
                    # print(score)
                    scr=score.select_one("."+classname)
                # serialdisplay(score.get_text())
                lscore=tm+ ""+ mm +" > "+ score.get_text()
                print(lscore)
            except Exception as e:
                print(f"Error during scraping: {e}")
    
    async def scraping(self):

        global count
        global urll
        global classname
        count+=1
        if count>10:
            count=0
            try:
                # Send HTTP GET request
                response = requests.get(self.url)
                response.raise_for_status()  # Raise an error for bad HTTP responses

                # Parse HTML content
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.title.string if soup.title else 'No title found'
                scores= soup.find_all('span',classname)
                for score in scores:
                    # print(score)
                    scr=score.select_one("."+classname)
                # serialdisplay(score.get_text())
                result = score.get_text()
                print("result = "+result)
            except Exception as e:
                print(f"Error during scraping: {e}")


async def periodic_scraping(scraper):
    while True:
        await scraper.scrape()
        await asyncio.sleep(1)  # Wait for 1 second before the next scrape


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),(r"/scrape", ScrapeHandler),
    ])


if __name__ == "__main__":
    # global urll
    url_to_scrape = urll  # Replace with the target website
    scraper = Scraper(url_to_scrape)

    app = make_app()
    app.listen(8888)

    # Start periodic scraping task
    tornado.ioloop.IOLoop.current().spawn_callback(periodic_scraping, scraper)

    print("Starting Tornado server on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
