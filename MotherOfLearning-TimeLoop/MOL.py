#!/usr/bin/python3
'''
    Converts html file from specific url to text
'''
import os
import sys
import math
import subprocess
import re
path_to_script_dir = os.path.dirname(os.path.abspath(__file__))
path_to_main_dir = os.path.join(path_to_script_dir, "../")
sys.path.append(path_to_main_dir)
import numberHelper # contains some useful functions 

import urllib.request
from bs4 import BeautifulSoup
from unidecode import unidecode
path_to_script_dir = os.path.dirname(os.path.abspath(__file__))

# https://www.fictionpress.com/s/2961893/1/Mother-of-Learning
# https://www.fictionpress.com/s/2961893/2/Mother-of-Learning
# https://www.fictionpress.com/s/2961893/108/Mother-of-Learning -- last page
url_base = "https://www.fictionpress.com/s/2961893"
url_list = []

# Parse through all urls and add them to list (goes up to 108)
for i in range(1, 109):
    full_url = f"{url_base}/{i}/Mother-of-Learning"
    url_list.append(full_url)


# print(url_list)
#---------------------------DONE GETTING ALL LINKS-----------------------#


#-----------------PULL TEXT FROM EACH URL----------------------#
book = []
for url_num, url in enumerate(url_list, start=1):

    print("Loading txt from url " + url)
    
    # sometimes need to make a request before extracting from url
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    title = soup.find('title').string
    text = soup.get_text()
    page_start_index = 0
    page_end_index = 0
    # lines = text.splitlines()

    # print(text)

    beg_phrase = f"Chapter {numberHelper.extendDigits(url_num, 3)}" 
    end_phrase = "< Prev 1. Good Morning Brother" if url_num != 1 else " 1. Good Morning Brother2."

    text_to_skip = f"Chapter {url_num}: "
    page_fake_start_idx = text.find(text_to_skip) # repeated text so start here
    page_fake_start_idx = page_fake_start_idx + len(text_to_skip) if page_fake_start_idx != -1 else 0 # edge case of it not existing
    if url_num < 107:
        page_start_index = text.index(beg_phrase, page_fake_start_idx) #+ len(beg_phrase)
    elif url_num == 107:
        page_start_index = text.index("Zorian's eyes abruptly shot open", page_fake_start_idx) #+ len(beg_phrase)
    elif url_num == 108:
        page_start_index = text.index("You have reached the end of the story. What follows is merely", page_fake_start_idx) #+ len(beg_phrase)

    page_end_index = text.index(end_phrase, page_start_index)

    print("Start index: {0}\nEnd Index: {1}".format(page_start_index, page_end_index))

    # If not the first chapter/page, then don't show title again
    # Use line numbers found to get rid of useless parts of book
    # writeable_text = text[page_start_index:page_end_index].rstrip()
    writeable_text = text[page_start_index:page_end_index]

    # adjustments
    writeable_text = writeable_text.replace('""', '"') # replace double quotes
    # add space between chapter# and text

    # parse title to format chapter start
    chap_name_start = title.find(text_to_skip) + len(text_to_skip)
    chap_name_end = title.find(", a fantasy fiction", chap_name_start)
    chap_name = title[chap_name_start : chap_name_end]
    writeable_text = writeable_text.replace(beg_phrase, f"{beg_phrase}: {chap_name}\n\n")
    
    print(writeable_text)
    book.append(writeable_text)

name_of_txt_file = "Mother of Learning(Time Loop).txt"
path_to_txt_file = os.path.join(path_to_script_dir, '..', 'SavedBooks', 'Mother of Learning(Time Loop)', name_of_txt_file)

if (not os.path.exists(os.path.dirname(path_to_txt_file))):
    print("Folder for this book does not exist! Creating it...")
    os.makedirs(os.path.dirname(path_to_txt_file))

# writeable_text = "".join(book)
# whiteSpaceExpr = r'(\s{2,})' # extra whitespace (more than one space)
# matches = re.findall(whiteSpaceExpr, writeable_text)
# print(matches)
# for match in matches:
#     writeable_text = writeable_text.replace(match, '')

# garb1 = r'(<br />)'
# matches = re.findall(garb1, writeable_text)
# print("expr 1")
# print(matches)
# for match in matches:
#     writeable_text = writeable_text.replace(match, ' ')

# garb2 = r'(&nbsp; )'
# matches = re.findall(garb2, writeable_text)
# print("expr 2")
# print(matches)
# for match in matches:
#     writeable_text = writeable_text.replace(match, '')


# Save text converted html to a file
with open(path_to_txt_file, 'w+') as write_file:
   writeable_text = "\n".join(book) # -done already
   writeable_text = unidecode(writeable_text)
   write_file.write(writeable_text)

print("Program Complete!")
