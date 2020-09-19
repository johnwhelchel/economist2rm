import logging
import time

from internet import is_connected
from remarkable.uploader import Uploader
from scraping.scraper.spiders.economist import Economist
from pdf.creator import create_latest

from pathlib import Path

import os, sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def scrape():
    logging.info("Scraping...")
    os.environ["SCRAPY_PROJECT"] = str(Path(os.getcwd()) / "scraping")
    process = CrawlerProcess(get_project_settings())
    breakpoint()
    sys.exit()
    process.crawl(Economist)
    process.start()
    logging.info("Scraping complete")


def upload(file: Path):
    logging.info("Uploading...")
    uploader = Uploader()
    uploader.upload_file_to_folder(str(file), "Economist")
    logging.info("Upload complete")


if __name__ == '__main__':
    while not is_connected():
        time.sleep(300)
    ch = logging.StreamHandler(sys.stdout)
    root = logging.getLogger()
    root.addHandler(ch)
    logging.info("Begin economist2rm")
    scrape()
    latest_pdf = create_latest()
    if latest_pdf:
        logging.info("New PDF generated")
        upload(latest_pdf)
    logging.info("End economist2rm")
