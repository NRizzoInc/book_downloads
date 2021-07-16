'''
    Converts html file from specific url to text
'''
import os
import sys
import math
import subprocess
import re
path_to_script_dir = os.path.dirname(os.path.abspath(__file__))
path_to_main_dir = os.path.join(path_to_script_dir, "..", "..")
path_to_main_dir = os.path.join(path_to_script_dir, "..")
sys.path.append(path_to_main_dir)
from numberHelper import * # contains some useful functions

import urllib.request
from bs4 import BeautifulSoup
from unidecode import unidecode
path_to_script_dir = os.path.dirname(os.path.abspath(__file__))

# https://novel80.com/245272-burn-for-me.html
# https://novel80.com/burn-for-me/page-2-2017728.html  -- 2017728 base
# https://novel80.com/burn-for-me/page-89-2017815.html
url_base = "https://novel80.com/burn-for-me/page"
url_list = []

# Parse through all urls and add them to list
for i in range(1, 90):
    if i == 1:
        full_url = f"https://novel80.com/245272-burn-for-me.html"
    else:
        base_num = 2017726 # subtract 2 bc offset
        final_num = base_num+i
        full_url = f"{url_base}-{i}-{final_num}.html"
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
    text = soup.get_text()
    page_start_index = 0
    page_end_index = 0
    # lines = text.splitlines()

    #print(text)
    if url_num == 1:
        beg_phrase = f"Burn for Me Page {url_num}"
    else:
        beg_phrase = f"Burn for Me Page {url_num}"
        #beg_phrase = "Category\n\n\n"
    #end_phrase = "online free by Ilona Andrews - Novel80"
    page_listing = "\n".join([str(i) for i in range(1,90)])
    end_phrase_start = "" if url_num == 1 else "Prev page\n\n"
    end_phrase = f"{end_phrase_start}{page_listing}"

    try:
        page_start_index = text.rindex(beg_phrase) + len(beg_phrase)
        #page_start_index = text.index(beg_phrase) + len(beg_phrase)
    except:
        print(text)
        print("There was an error scanning for start... exiting")
        sys.exit()

    try:
        page_end_index = text.index(end_phrase)
    except:
        print(text)
        print("There was an error scanning for end... exiting")
        print(f"end_phrase = {end_phrase}")
        sys.exit()

    print("Start index: {0}\nEnd Index: {1}".format(page_start_index, page_end_index))

    # If not the first chapter/page, then don't show title again
    # Use line numbers found to get rid of useless parts of book
    # writeable_text = text[page_start_index:page_end_index].rstrip()
    writeable_text = text[page_start_index:page_end_index]
    
    # remove bad spacings within text bc of html
    writeable_text = writeable_text.strip() + "\n"
    writeable_text = writeable_text.replace("                       \n", "")
    #writeable_text = writeable_text.replace("          			", "\t"
    # remove [1] or [12], etc
    #writeable_text = re.sub(r"\[\d+\]", '', writeable_text)

    # fix issue of period with no space ("hello.world" -> "hello. World")
    # capture group 1 (\1) = left word, group 2 (\2) = right word
    # do it twice bc patterns cannot overlap

    print(f"Page {url_num}:\n{writeable_text}")
    book.append(writeable_text)

name_of_txt_file = "Burn For Me.txt"
path_to_txt_file = os.path.join(path_to_script_dir, "..", "SavedBooks", "BurnForMe", name_of_txt_file)

if (not os.path.exists(os.path.dirname(path_to_txt_file))):
    print("Folder for this book does not exist! Creating it...")
    os.makedirs(os.path.dirname(path_to_txt_file))

# Save text converted html to a file
with open(path_to_txt_file, 'w+') as write_file:
   writeable_text = "\n".join(book)
   writeable_text = unidecode(writeable_text)
   write_file.write(writeable_text)

print("Program Complete!")
