from typing import List, Set

from extract_emails.email_filters import EmailFilterInterface
from .domains import TOP_LEVEL_DOMAINS


class DefaultEmailFilter(EmailFilterInterface):
    """
    Default email filter

    """

    def __init__(self):
        self.checked_emails: Set[str] = set()
        self.black_list = ['wix.com', 'sentry.wixpress.com']
        self.adress_black_list = ["yourname", "name", "your"]

    def filter(self, emails: List[str]) -> List[str]:
        """
        Remove duplicates and filter by domain

        :param: list(str) emails: list of emails for filtering
        :return: List of emails
        """
        filtered_emails = []
        print(emails)
        for email in emails:
            email = email.replace('/', '')
            split_email = email.split("@")
            site = split_email[-1]
            adress = split_email[0]
            if adress in self.adress_black_list:
                continue
            if adress == ['nfo']:
                email = "info@"+site
            if adress == ['entist']:
                email = "dentist@"+site
            if adress == ['entists']:
                email = "dentists@"+site
            if adress == ['eception']:
                email = "reception@"+site
            domain = "." + email.split(".")[-1]
            if domain not in TOP_LEVEL_DOMAINS:
                continue
            if email in self.checked_emails:
                continue
            if site in self.black_list:
                continue
            self.checked_emails.add(email)
            filtered_emails.append(email)
        return filtered_emails
