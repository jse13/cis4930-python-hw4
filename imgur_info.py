#!/usr/bin/env python
'''
Julian Engel
jse13
'''

import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

imgur_url = "http://imgur.com/user/<username>/index/newest/page/<num>/hit.json?scrolling"

def check_url(url):
    result = requests.get(url)
    if result.status_code is not 200:
        logging.error("URL {} returned error code {}".format(url, result.status_code))
        return False
    else:
        return True


def get_comment_data(url):
    to_return = list()
    more_comments = True
    page_num = 0

    # Iterate until there are no more pages left
    while more_comments:
        result = requests.get(url.replace("<num>", str(page_num)))
        if len(result.text) is 0:
            more_comments = False
        else:
            json_data = json.loads(result.text)
            to_return.extend(json_data['data']['captions']['data'])
            logging.debug("Adding {} item(s) to list of length {}".format(len(json_data['data']['captions']['data']), len(to_return)))

        page_num += 1


    return to_return


def get_top_five(comments):
    top_five = list()

    idx = 0
    current_highest = 0
    current_highest_idx = 0
    
    for counter in range(0, 5):
        idx = 0
        current_highest = 0
        current_highest_idx = 0

        for item in comments:
            if item['points'] > current_highest:
                current_highest = item['points']
                current_highest_idx = idx
            elif item['points'] == current_highest:
                if item['hash'].lower() < comments[current_highest_idx]['hash'].lower():
                    current_highest_idx = idx
            idx += 1
        
        top_five.append(comments[current_highest_idx])
        comments.pop(current_highest_idx)
    
    return top_five


def print_comments(comments):
    count = 1
    for item in comments:
        print "{}.".format(count),
        print item['hash']
        print "Points: {}".format(item['points'])
        print "Title: {}".format(item['title'])
        print "Date: {}".format(item['datetime'])
        print ""

        count += 1


if __name__ == "__main__":

    username = raw_input("Enter username: ")

    # Replace <username> in URL with given username
    imgur_url = imgur_url.replace("<username>", username)
    logging.debug("Using the URL {}".format(imgur_url))

    comments = list()

    if check_url(imgur_url.replace("<num>", "0")):
        comments = get_comment_data(imgur_url)

        if len(comments) is 0:
            print "That user has no comments, exiting..."
            exit()

        comments = get_top_five(comments)
        print_comments(comments)
    else:
        print "User doesn't exist, exiting..."
        exit()
    
