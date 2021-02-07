from extract_emails import EmailExtractor
from extract_emails.browsers import ChromeBrowser
import pandas as pd
import numpy as np
from googlesearch import search
from urllib.parse import urlsplit

file_name = "ontario_dentist.csv"
root = "/Users/zachyamaoka/Dropbox/Projects/Face Mask/MARKETING/SCRAPING/inputs/"
data = pd.read_csv(root+file_name)
num_people = data.shape[0]

print(data.columns)

# Names
data['names_split'] = data['person'].map(lambda person: person.split())
data['first name'] = data['names_split'].map(
    lambda names_split: names_split[1].capitalize())
data['last name'] = data['names_split'].map(
    lambda names_split: names_split[-1].capitalize())

data['website-href'] = data['website-href'].fillna("")
data['num reviews'] = data['num reviews'].fillna(0)

data['email'] = [""]*num_people

data = data.drop(columns=['web-scraper-order',
                          'web-scraper-start-url', 'website', 'names_split'])

data = data.sort_values(by=['rating'])
data = data.rename(columns={"person": "full name",
                            "website-href": "website url", "person-href": "ratemd"})
browser = ChromeBrowser(
    executable_path="/Users/zachyamaoka/Documents/chromedriver")

urls = data['website url']
for i in range(num_people):
    if (data.at[i, 'num reviews'] == 0):
        continue
    url = urls[i]
    print("{} of {}, url: {}".format(i+1, num_people, url))
    if url == "":
        continue
    email_extractor = EmailExtractor(
        url, browser, depth=2, link_filter=1)
    emails = email_extractor.get_emails()
    if len(emails):
        data.at[i, 'email'] = emails[0].as_dict()["email"]

#
print(data['email'])
#
# # TIDY UP FILE

data.to_csv("/Users/zachyamaoka/Dropbox/Projects/Face Mask/MARKETING/SCRAPING/outputs/" +
            file_name[:-4]+"_scraped.csv")
