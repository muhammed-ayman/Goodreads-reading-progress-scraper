import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint


class GoodReadsProgressScraper:
    def __init__(self, user_id):
        self.user_id = str(user_id)
        self.books_review_ids = []
        self.books_progress_percentages = []


    def scrape(self):
        self.get_books_ids()
        self.get_progress_percentages()


    def get_books_ids(self):
        if self.books_review_ids:
            return

        url = f'https://www.goodreads.com/review/list/{self.user_id}?shelf=currently-reading'
        req = requests.get(url)
        res = req.content.decode('utf-8')
        reviews = re.findall("cover_review_[0-9]*", res)
        books_ids = [reviews[i].split('_')[-1] for i in range(len(reviews))]
        self.books_review_ids = books_ids


    def get_progress_percentages(self):
        if not self.books_review_ids:
            return

        for book_id in self.books_review_ids:
            url = f'https://www.goodreads.com/review/show/{book_id}'
            req = requests.get(url)
            res = req.content
            soup = BeautifulSoup(res, 'html.parser')
            bookTitle = soup.find_all('a', {'class' : 'bookTitle'})[0].text
            readingTimelineRow = soup.find_all(attrs={'class' : "readingTimeline__row"})[-1]
            readingTimelineRow_text = readingTimelineRow.find_all("div", {"class":"readingTimeline__text"})[0]
            percentage = readingTimelineRow_text.find_all('a')[0].text
            self.books_progress_percentages.append({bookTitle : percentage})


if __name__ == '__main__':
    goodreads_inst = GoodReadsProgressScraper(69545251)
    goodreads_inst.scrape()
    pprint(goodreads_inst.books_progress_percentages)
