from extract_emails import EmailExtractor
from extract_emails.browsers import ChromeBrowser
import pandas as pd
import numpy as np
from googlesearch import search
from urllib.parse import urlsplit

file_name = "maxpages.csv"
root = "/Users/zachyamaoka/Dropbox/Projects/Face Mask/MARKETING/SCRAPING/inputs/"
data = pd.read_csv(root+file_name)

browser = ChromeBrowser(
    executable_path="/Users/zachyamaoka/Documents/chromedriver")
num_people = data.shape[0]
website_to_try = 3

# print(pd.isna(data.loc[0, 'website-href']))

# print(pd.isna(data.loc[0, 'website-href']))


for i in range(website_to_try):
    i += 1
    if i == 1:
        data['website-trial-'+str(i)] = data['website-href'].fillna("")
    else:
        data['website-trial-'+str(i)] = [""]*num_people
    data['email-trial-'+str(i)] = [""]*num_people
print(data['website-trial-1'])
print(data['website-trial-2'])


def find_website(query, num=5):
    my_results_list = []
    exlude_list = ["ratemds", "411", "yellowpages", "opendi", "canadian.dental", "allbiz", "dentistdirectorycanada",
                   "canadapages", "gcr", "tbnewswatch", "facebook", "canpages", "dnb", "dentpedia", "vymaps", "justdial", "mapquest", "pagesjaunes", "linkedin", "canadiandoctorsdirectory", "dentalcard"]
    added_list = []
    for i in search(query,        # The query you want to run
                    tld='com',  # The top level domain
                    lang='en',  # The language
                    num=num,     # Number of results per page
                    start=0,    # First result to retrieve
                    stop=num,  # Last result to retrieve
                    pause=2.0,  # Lapse between HTTP requests
                    ):
        good = True

        for exlude in exlude_list:
            if exlude in i:
                good = False
        if good:
            parts = urlsplit(i)
            candidate = "{0.scheme}://{0.netloc}".format(parts)
            if candidate not in added_list:
                added_list.append(candidate)
                my_results_list.append(candidate)

    return my_results_list


urls = data['website-trial-1']
print(data.columns)

data['num reviews'] = data['num reviews'].fillna(0)

for i in range(num_people):
    if (data.at[i, 'num reviews'] == 0):
        continue
    url = urls[i]
    print("{} of {}, url: {}".format(i+1, num_people, url))
    if url == "":
        data['email-trial-1'][i] = "no inital website"
        query = str(data["practice"][i]).lower()
        if query == "nan":
            query = str(data["person-href"][i]).lower()
        city = str(data["city"][i]).lower()
        if city not in query:
            query += " " + city
        print(query)
        candiate_urls = find_website(query, website_to_try)
        for j in range(len(candiate_urls)):
            print(candiate_urls[j])
            data['website-trial-'+str(j+1)][i] = candiate_urls[j]
#
    for k in range(website_to_try):
        k += 1
        url = data.at[i, 'website-trial-'+str(k)]
        if url == "":
            continue
        print("URL: ", url)
        email_extractor = EmailExtractor(
            url, browser, depth=2, link_filter=1)
        emails = email_extractor.get_emails()
        if len(emails):
            data['email-trial-'+str(k)][i] = emails[0].as_dict()["email"]


print(data['email-trial-1'])

# TIDY UP FILE
data.to_csv("/Users/zachyamaoka/Dropbox/Projects/Face Mask/MARKETING/SCRAPING/outputs/" +
            file_name[:-4]+"_scraped.csv")
