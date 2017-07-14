#!/usr/bin/env python
'''
Julian Engel
jse13
'''
import requests
import re
import logging

logging.basicConfig(level=logging.INFO)

ROOT_PAGE = "http://www.cs.fsu.edu/department/faculty/"
LINE_SEP = "****************************************" 


def populate_directory():

    # My code doesn't hang, I swear!
    print "Scraping faculty pages, this may take a minute or two..."

    # Contains all the sub-pages of the faculty page
    sub_pages = set()

    # Contains dicts of information unique to each faculty member
    listing = list()

    root = requests.get(ROOT_PAGE)    

    # Make sure request didn't error out
    if root.status_code is not 200:
        logging.error("Error fetching the faculty page, got status code {}".append(root.status_code))
        return None

    # Look through the text and find the links to the faculty pages
    for url in re.findall("http://www.cs.fsu.edu/department/faculty/[a-z]+", root.text):
        sub_pages.add(url)

    # Use those links to populate the specific information of each faculty member
    for url in sub_pages:
        listing.append(fetch_faculty_info(url))

    return listing


def fetch_faculty_info(url):
    to_return = {"Name" : None, "Office" : None, "Telephone" : None, "Email" : None}

    info_page = requests.get(url)

    # Make sure request didn't error out
    if info_page.status_code is not 200:
        logging.error("Error fetching the faculty page, got status code {}".append(info_page.status_code))
        return None

    # Get the name
    name = re.search(".*main_title\">(.*)</h1>", info_page.text)
    if name is not None:
        to_return["Name"] = name.group(1).encode('utf-8')
        logging.debug("Matched name: {}".format(to_return["Name"]))
    else:
        logging.error("Could not match a name on page {}".format(url))

    # Get the office
    office = re.search(".*Office:.*</td>\n<td>(.*)</td>", info_page.text)
    if office is not None:
        to_return["Office"] = office.group(1).encode('utf-8').decode("ascii", "ignore")
        logging.debug("Matched office: {}".format(to_return["Office"]))
    else:
        logging.error("Could not match an office on page {}".format(url))

    # Get the phone number
    telephone = re.search(".*Telephone:.*</td>\n<td>(.*)</td>", info_page.text)
    if telephone is not None:
        to_return["Telephone"] = telephone.group(1).encode('utf-8').decode("ascii", "ignore")
        logging.debug("Matched telephone: {}".format(to_return["Telephone"]))
    else:
        logging.error("Could not match a telephone number on page {}".format(url))

    # Get the email
    email = re.search(".*E-Mail:.*</td>\n<td>([a-z0-9]+.*\[.*\]).*</td>", info_page.text)
    if email is not None:
        to_return["Email"] = email.group(1).encode('utf-8').decode("ascii", "ignore")
        logging.debug("Matched email: {}".format(to_return["Email"]))
    else:
        logging.error("Could not match an email address on page {}".format(url))

    return to_return


def print_directory(listing):
    for item in listing:

        print "Name: {}".format(item["Name"])

        if len(item["Office"]) is 0:
            print "Office: N/A"
        else:
            print "Office: {}".format(item["Office"])
        
        if len(item["Telephone"]) is 0:
            print "Telephone: N/A"
        else:
            print "Telephone: {}".format(item["Telephone"])

        if len(item["Email"]) is 0:
            print "E-mail: N/A"
        else:
            print "E-mail: {}".format(item["Email"])

        print LINE_SEP


if __name__ == "__main__":

    listing = populate_directory()
    print_directory(listing)
