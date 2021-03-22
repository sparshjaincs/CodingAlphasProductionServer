import feedparser
from bs4 import BeautifulSoup

class ParseFeed():

    def __init__(self,topic):
        self.feed_url = f"http://news.google.com/news?q={topic}&hl=en-US&sort=date&gl=US&num=100&output=rss"
        self.topic = topic
        
    def clean(self, html):
        '''
        Get the text from html and do some cleaning
        '''
        soup = BeautifulSoup(html,'html.parser')
        text = soup.get_text()
        text = text.replace('\xa0', ' ')
        return text

    def parse(self):
        '''
        Parse the URL, and print all the details of the news 
        '''
        feeds = feedparser.parse(self.feed_url).entries
        data = []
        for f in feeds:
            data.append({
                'Description': self.clean(f.get("description", "")),
                'Published_Date': f.get("published", ""),
                'Title': f.get("title", ""),
                'Url': f.get("link", "")
            })
        return data
            
#feed = ParseFeed('Computer-Programming')
#data = feed.parse()