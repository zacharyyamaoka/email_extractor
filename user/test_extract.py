from extract_emails.browsers import ChromeBrowser
from extract_emails import EmailExtractor
# url = "http://www.adcottawa.com/"
# url = "https://dentistryonking.net/"
# url = "https://conklindental.ca/"
# url = "http://elliotlakedentalcentre.com/"
# url = "http://www.sudburysmiles.ca/"
# url = "https://www.downtowndentistry.com/contact-us"
url = "http://www.downtowndental.ca//"
chrome_driver = "/Users/zachyamaoka/Documents/extract-emails/user/chromedriver"

with ChromeBrowser(executable_path=chrome_driver) as browser:
    email_extractor = EmailExtractor(url, browser, depth=2, link_filter=1)
    emails = email_extractor.get_emails()


for email in emails:
    print(email)
    print(email.as_dict())
