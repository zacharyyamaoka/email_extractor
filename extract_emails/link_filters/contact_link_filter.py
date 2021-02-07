from typing import List, Set
from urllib.parse import urljoin, urlparse, urlsplit

from extract_emails.link_filters import LinkFilterInterface


class ContactInfoLinkFilter(LinkFilterInterface):
    """
    Contact information filter for links.
    Filter out the links without ['about', 'contact', 'about-us', 'contact-us', ... ].
    Only keep the links might contain the contact information.

    :param list(str) links: List of URLs
    """
    checked_links: Set[str] = set()

    def __init__(self, website_address: str, **kwargs):
        super().__init__(website_address, **kwargs)
        # where to use all the urls in the same domain or not,
        # if there are not any urls after filtering by contactinfo candidates
        self.use_default = kwargs.get('use_default', False)
        self._contruct_candidates()
        parts = urlsplit(website_address)
        self.website_name = parts.netloc

    def _contruct_candidates(self):
        self.candidates = ['about', 'about-us', 'aboutus',
                           'contact', 'contact-us', 'contactus', 'location', 'the-team', 'get-in-contact']

    def filter(self, links: List[str]) -> List[str]:
        filtered_urls = []
        for url in links:
            url = urljoin(self.website, url)
            if self.website_name in url and url not in self.checked_links:
                self.checked_links.add(url)
                filtered_urls.append(url)

        contactinfo_urls = []
        for url in filtered_urls:
            for cand in self.candidates:
                if cand in url.lower():
                    contactinfo_urls.append(url)

        if len(contactinfo_urls) == 0 and self.use_default:
            # no contactinfo urls found and return filtered_urls
            return filtered_urls
        else:
            return contactinfo_urls

    @staticmethod
    def get_website_address(url: str) -> str:
        """
        Get website address from an URL

        Example:
            >>> DefaultLinkFilter.get_website_address('https://example.com/page.html?param=123')
            ... 'https://example.com/'

        :param str url: some URL
        :return: website address
        """
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}/"
