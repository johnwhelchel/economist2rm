import os
import pathlib

import scrapy
from scrapy.http.response import Response
from bs4 import BeautifulSoup
from xhtml2pdf import pisa

from config import ARTICLES_ROOT


class Economist(scrapy.Spider):
    """
    Creates a PDF based on the latest printed edition of The Economist
    """
    name = "Economist"
    start_urls = ["https://www.economist.com/weeklyedition"]

    def parse(self, response, **kwargs):
        title: str = " | ".join(response.css("title::text").getall()[0].split(" | ")[0:2])
        if self._not_already_scraped(title):
            folder_root = self._create_folder(title)
            yield from self._parse_world_this_week(response, folder_root)
            yield from self._parse_sections(response, folder_root)

    def _create_folder(self, title: str):
        folder_root = ARTICLES_ROOT / title
        os.mkdir(folder_root)
        return folder_root

    def _parse_world_this_week(self, response: Response, folder_root: pathlib.Path):
        meta = {'folder_root': folder_root}
        yield from response.follow_all(
            css=".layout-weekly-edition-wtw .weekly-edition-wtw__item a",
            callback=self._parse_article,
            meta=meta)

    def _parse_sections(self, response: Response, folder_root: pathlib.Path):
        section_name = response.css(".ds-section-headline::text").get()
        meta = {'folder_root': folder_root}
        yield from response.follow_all(
            css=".layout-weekly-edition-section .teaser a.headline-link",
            callback=self._parse_article,
            meta=meta)

    def _parse_article(self, response: Response):
        folder_root = response.meta["folder_root"]
        title = response.css(".article__headline::text").get() + ".pdf"
        soup = BeautifulSoup(response.text, 'lxml')
        self._remove_html_node(soup.find("header", class_="ds-masthead"))
        self._remove_html_node(soup.find("div", class_="article__section"))
        self._remove_html_node(soup.find("div", class_="layout-article-links"))
        self._remove_html_node(soup.find("div", class_="newsletter-signup"))
        self._remove_html_node(soup.find("aside", class_="article__aside"))
        self._remove_html_node(soup.find("div", class_="layout-related-articles"))
        self._remove_html_node(soup.find("footer"))
        with open(folder_root / title, mode='w+b') as dest:
            pisa_status = pisa.CreatePDF(str(soup), dest=dest)

    def _remove_html_node(self, selected_soup):
        if selected_soup is not None:
            selected_soup.decompose()

    def _not_already_scraped(self, title):
        return not (ARTICLES_ROOT / title).exists()
