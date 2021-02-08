url = "http://www.drannatucka.com/"

from extract_emails import EmailExtractor
from extract_emails.browsers import ChromeBrowser

chrome_driver = "/Users/misayamaoka/Documents/email_extractor/user/chromedriver"

with ChromeBrowser(executable_path=chrome_driver) as browser:
    email_extractor = EmailExtractor(url, browser, depth=2)
    emails = email_extractor.get_emails()


for email in emails:
    print(email)
    print(email.as_dict())
