import logging
import time
from typing import Optional

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
    configure_python_path_for_scraping()
    process = CrawlerProcess(get_project_settings())
    process.crawl(Economist)
    process.start()
    logging.info("Scraping complete")


def configure_python_path_for_scraping():
    sys.path.append(str(Path(os.getcwd()) / "scraping"))
    os.environ["SCRAPY_SETTINGS_MODULE"] = "scraper.settings"


def upload(file: Path):
    logging.info("Uploading...")
    uploader = Uploader()
    uploader.upload_file_to_folder(str(file), "Economist")
    logging.info("Upload complete")


def setup_logging():
    ch = logging.StreamHandler(sys.stdout)
    root = logging.getLogger()
    root.addHandler(ch)


def try_upload(latest_pdf: Optional[Path]):
    if latest_pdf:
        logging.info("New PDF generated")
        upload(latest_pdf)


if __name__ == '__main__':
    while not is_connected():
        time.sleep(300)
    setup_logging()
    logging.info("Begin economist2rm")
    scrape()
    try_upload(create_latest())
    logging.info("End economist2rm")
