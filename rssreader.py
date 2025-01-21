import feedparser

import threading

def fetch_rss_feed(url):
    # Parse the RSS feed
    feed = feedparser.parse(url)

    # Create a list to store the titles and links
    rss_items = []

    # Loop through each entry in the feed
    for entry in feed.entries:
        # Create a formatted string for each entry
        item_string = f"Title: {entry.title}"
        # Append the string to the list
        rss_items.append(item_string)

    return rss_items


# URL of the RSS feed
rss_feed_url = "https://www.bola.net/feed/"  # Replace with a valid RSS feed URL

# Fetch the RSS feed and store the items in a list
rss_list = fetch_rss_feed(rss_feed_url)

# Print the list of RSS items
for item in rss_list:
    print(item)


def pulse():


pulse()
#
# import feedparser
#
# # URL of the RSS feed
# rss_feed_url = "https://www.bola.net/feed/"
#
# # Fetch and parse the RSS feed
# feed = feedparser.parse(rss_feed_url)
#
# # Display feed information
# for entry in feed.entries:
#     print(f"Title: {entry.title}")
#     print(f"Link: {entry.link}")
#     print(f"Date: {entry.published}")
#     print("---")
