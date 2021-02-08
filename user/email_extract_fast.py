from extract_emails import EmailExtractor
from extract_emails.browsers import ChromeBrowser
import pandas as pd
import numpy as np
from googlesearch import search
from urllib.parse import urlsplit

def scrap(file_name):
    root = "/Users/misayamaoka/Google Drive/My Drive/Ambience/Commerical/Contacts/ratemd csv files/Canada/Ontario/"
    chrome_driver = "/Users/misayamaoka/Documents/email_extractor/user/chromedriver"
    data = pd.read_csv(root+file_name)
    num_people = data.shape[0]

    print(data.columns)
    print("Number of People: ", num_people)

    # Names
    data['names_split'] = data['person'].map(lambda person: person.split())
    data['first name'] = data['names_split'].map(
        lambda names_split: names_split[1].capitalize())
    data['last name'] = data['names_split'].map(
        lambda names_split: names_split[-1].capitalize())

    data['website-href'] = data['website-href'].fillna("")
    data['num reviews'] = data['num reviews'].fillna(0)

    data['email'] = [""]*num_people
    data['notes'] = [""]*num_people

    data = data.drop(columns=['web-scraper-order',
                              'web-scraper-start-url', 'website', 'names_split'])

    data = data.sort_values(by=['rating'])
    data = data.rename(columns={"person": "full name",
                                "website-href": "website url", "person-href": "ratemd"})
    browser = ChromeBrowser(
        executable_path=chrome_driver)

    checkpoint=500
    urls = data['website url']
    for i in range(num_people):
        if (i%checkpoint)==0:
            data.to_csv(root + file_name[:-4]+"_scraped.csv")
            print("Check Point")
        # if (data.at[i, 'num reviews'] == 0):
        #     data.at[i, 'notes'] = "no reviews"
        #     continue
        url = urls[i]
        print("{} of {}, url: {}".format(i+1, num_people, url))
        if url == "":
            data.at[i, 'notes'] = "no website"
            continue
        email_extractor = EmailExtractor(
            url, browser, depth=2, link_filter=1)
        emails = email_extractor.get_emails()
        n_email = len(emails)
        print("Found Emails: ", n_email)
        for k in range(n_email):
            found_email = emails[k].as_dict()["email"]
            print("Email: ", found_email)
            if found_email == "timeout@gmail.com":
                data.at[i, 'notes'] = "timed out"
                continue
            if k > 1:
                data.at[i, 'email'] += "," + found_email
            else:
                data.at[i, 'email'] = found_email
        if n_email == 0:
            data.at[i, 'notes'] = "not found"

    # print(data['email'])

    data.to_csv(root + file_name[:-4]+"_scraped.csv")


files = ["ontario_dentist_page=[1-288].csv","ontario_dentist_page=[289-599].csv","ontario_endodontist.csv","ontario_oral_surgeon.csv","ontario_periodontist.csv"]

for file_name in files:
    scrap(file_name)
