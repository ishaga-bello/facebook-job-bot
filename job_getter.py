from datetime import datetime
import dateutil.parser as parser
import json

from markdownify import MarkdownConverter

import requests
from bs4 import BeautifulSoup

def get_jobs():
    url = "https://www.cameroondesks.com/search/label/jobs"

    page = requests.get(url)
    bs = BeautifulSoup(page.text, "lxml")
    article = bs.findAll("article")

    links = []
    for link in article:
        article_date = link.find("span", class_="published timeago").get("title")
        article_date = parser.parse(article_date)
        present_date = datetime().now().date()
        if present_date == article_date:
            links.append(link.find("a").get("href"))


    jobs = list()
    for url in links:
        job_listing = dict()
        job_page = requests.get(url)
        job_bs = BeautifulSoup(job_page.text, "lxml")

        article = job_bs.find("article")
        title = job_bs.find("h1", class_="post-title entry-title").text.strip()
        job_listing['title'] = title
        content = MarkdownConverter(convert=["div"]).convert_soup(article)
        job_listing['content'] = content
        jobs.append(job_listing)

    return json.dumps(jobs)

if __name__ == "__main__":
    job = get_jobs()
    with open("outfile1.json", "w") as file: json.dump(job, file)
