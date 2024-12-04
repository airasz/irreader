import tornado.ioloop
import tornado.web
import tornado.httpclient
from bs4 import BeautifulSoup
import asyncio
import subprocess

import threading

import serial
from time import sleep
import json
urll="https://www.goal.com/en/match/cska-sofia-vs-spartak-varna/cLSNig4OSCyf2IEIDrahC"
count=0
classname="match-data_score__xQ29z"



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

# cekport()
# con = serial.Serial(
#     port=sport,
#     baudrate=9600,
#     parity=serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,
#     bytesize=serial.EIGHTBITS,
# )

def serialdisplay(msg):
    data= str.encode(msg)
    # con.write(data)




# Asynchronous function to fetch and scrape a web page
async def fetch_and_scrape(url):
    http_client = tornado.httpclient.AsyncHTTPClient()
    global classname
    try:
        response = await http_client.fetch(url)
        html = response.body.decode('utf-8')  # Decode the HTML content
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else 'No title found'
        scores= soup.find_all('span',classname)
        for score in scores:
            print(score)
            scr=score.select_one("."+classname)
        return {"title": title, "url": url, "result": score.get_text()}
    except Exception as e:
        return {"error": str(e), "url": url}

# Asynchronous function to fetch and scrape a web page
async def fetch_n_scrape(url):
    print("scrapping web")
    http_client = tornado.httpclient.AsyncHTTPClient()
    global classname
    try:
        response = await http_client.fetch(url)
        html = response.body.decode('utf-8')  # Decode the HTML content
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else 'No title found'
        scores= soup.find_all('span',classname)
        for score in scores:
            print(score)
            scr=score.select_one("."+classname)
        # serialdisplay(score.get_text())
        print(score.get_text())
        # return {"title": title, "url": url, "result": score.get_text()}
    except Exception as e:
        pass
        # serialdisplay ("error"+ str(e))

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
        result = await fetch_and_scrape(url)
        self.write(result)

# Tornado application setup
def make_app():
    return tornado.web.Application([
        (r"/scrape", ScrapeHandler),
    ])

# def loopy():
#     global count
#     global urll
#     count+=1
#     if count> 25:
#         count=0
#         if urll!="":
#              fetch_n_scrape(urll)
#     threading.Timer(1, loopy).start()

# loopy()
async def periodic_task():
    while True:

        global count
        global urll
        count+=1
        if count> 25:
            count=0
            if urll!="":
                await fetch_n_scrape(urll)
        print("Task executed")
        await asyncio.sleep(1)  # Wait for 1 second before the next iteration

async def main():
    task = asyncio.create_task(periodic_task())  # Create the periodic task

    # threading.Timer(1, loopy).start()
    # Run for 10 seconds
    await asyncio.sleep(10)

    # task.cancel()  # Cancel the periodic task
    try:

        await task  # Await the cancellation
    except asyncio.CancelledError:
        print("Periodic task cancelled.")

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server started at http://localhost:8888")
    asyncio.run(main())
    tornado.ioloop.IOLoop.current().start()
    print("starting app")
