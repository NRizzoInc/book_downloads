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

sys.path.append(path_to_main_dir)
from numberHelper import * # contains some useful functions

import urllib.request
from bs4 import BeautifulSoup
from unidecode import unidecode
path_to_script_dir = os.path.dirname(os.path.abspath(__file__))

# https://www.reads2020.com/fantasy/10096/10096.html - first pg
# https://www.reads2020.com/fantasy/10096/10096_2.html
# https://www.reads2020.com/fantasy/10096/10096_104.html -- last pg
url_base = "https://www.reads2020.com/fantasy/10096/10096"
url_list = []

# Parse through all urls and add them to list
for i in range(1, 105):
    if i == 1:
        full_url = f"{url_base}.html"
    else:
        full_url = f"{url_base}_{i}.html"
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
    beg_phrase = f"Author: Chloe Gong\n"
    end_phrase = "Total 105 Pages:"

    page_start_index = text.index(beg_phrase) + len(beg_phrase) 
    page_end_index = text.index(end_phrase)

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

name_of_txt_file = "These Violent Delights (#1).txt"
path_to_txt_file = os.path.join(path_to_script_dir, "..", "..", "SavedBooks", "BookClub", "TheseViolentDelights", name_of_txt_file)

if (not os.path.exists(os.path.dirname(path_to_txt_file))):
    print("Folder for this book does not exist! Creating it...")
    os.makedirs(os.path.dirname(path_to_txt_file))

# Save text converted html to a file
with open(path_to_txt_file, 'w+') as write_file:
   writeable_text = "\n".join(book)
   writeable_text = unidecode(writeable_text)
   write_file.write(writeable_text)

print("Program Complete!")
