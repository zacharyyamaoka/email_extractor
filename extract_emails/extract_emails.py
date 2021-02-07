#!/usr/local/bin/python3
# -*- coding: utf-8
from typing import List, Type

from .email import Email
from extract_emails.browsers import BrowserInterface
from extract_emails.html_handlers import DefaultHTMLHandler
from extract_emails.email_filters import DefaultEmailFilter
from extract_emails.link_filters import DefaultLinkFilter, ContactInfoLinkFilter
from urllib.parse import urlsplit

FILTERS = {0: DefaultLinkFilter, 1: ContactInfoLinkFilter}


class EmailExtractor:
    """
    Extract emails from a website

    Example:
        >>> extractor = EmailExtractor(browser, depth=10, max_links_from_page=-1)
        >>> emails = extractor.get_emails()

    :param str website_url: website for scan, e.g. https://example.com
    :param browser: browser to get page source by URL
    :param int depth: scan's depth, default 10
    :param int max_links_from_page: how many links a script shall get from each page, default -1 (all)
    :param int link_filter: which filter is used to extract url. default 0. 0 - DefaultLinkFilter,
        1 - ContactInfoLinkFilter
    """

    def __init__(
            self,
            website_url: str,
            browser: Type[BrowserInterface],
            depth: int = 10,
            max_links_from_page: int = -1,
            link_filter: int = 0,
            **kwargs
    ):
        parts = urlsplit(website_url)
        self.website = "{0.scheme}://{0.netloc}".format(parts)
        self.browser = browser
        self.depth = depth
        self.max_links_from_page = max_links_from_page

        self._links: List[str] = [self.website]
        self._checked_links: List[str] = []
        self._emails: List[Email] = []
        self._current_depth: int = 0
        self.html_handler = DefaultHTMLHandler()
        self.links_filter = FILTERS[link_filter](self.website, **kwargs)
        self.emails_filter = DefaultEmailFilter()

    def get_emails(self) -> List[Email]:
        """Extract emails from webpages
        """
        urls = self._get_urls()
        self._current_depth += 1
        if not len(urls) or self._current_depth > self.depth:
            return self._emails

        for url in urls:
            self._get_emails(url)
        return self.get_emails()

    def _get_emails(self, url: str):
        self.browser.open()
        page_source = self.browser.get_page_source(url)
        self.browser.close()
        emails = self.html_handler.get_emails(page_source)
        filtered_emails = self.emails_filter.filter(emails)
        self._emails.extend([Email(email, url) for email in filtered_emails])

        links = self.html_handler.get_links(page_source)

        filtered_links = self.links_filter.filter(links)
        if self.max_links_from_page != -1:
            filtered_links = filtered_links[: self.max_links_from_page]
        for fl in filtered_links:
            if fl not in self._checked_links:
                self._checked_links.append(fl)
                self._links.append(fl)

    def _get_urls(self) -> List[str]:
        links = self._links[:]
        self._links = []
        return links
