'''
    Converts html file from specific url to text
'''
import os
import sys
import math
import subprocess
path_to_script_dir = os.path.dirname(os.path.abspath(__file__))
path_to_main_dir = os.path.join(path_to_script_dir, "../")
sys.path.append(path_to_main_dir)
from numberHelper import * # contains some useful functions 
from numberHelper import * # contains some useful functions 

# pip necessary modules 
piped_modules = subprocess.check_output(['python', '-m', 'pip', 'list']).decode()
if 'bs4' not in piped_modules: subprocess.call("python -m pip install bs4")
if 'unidecode' not in piped_modules: subprocess.call("python -m pip install unidecode")

import urllib.request
from bs4 import BeautifulSoup
from unidecode import unidecode
path_to_script_dir = os.path.dirname(os.path.abspath(__file__))

#https://whatnovels.com/ninth-house-read-online/
#https://whatnovels.com/ninth-house-read-online/2/
url_base = "https://whatnovels.com/ninth-house-read-online"
url_list = []

# Parse through all urls and add them to list (goes up to 425)
for i in range(1, 426): 
    if (i == 1):
        full_url = url_base
    else:
        full_url = "{0}/{1}/".format(url_base, i)
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

    # print(text)
    if (url_num == 1):
        beg_phrase = "Series: Alex Stern"
    else:
        beg_phrase = "Series: Alex Stern"

    end_phrase = "Share on Facebook"

    page_start_index = text.index(beg_phrase) + len(beg_phrase) 
    page_end_index = text.index(end_phrase)

    print("Start index: {0}\nEnd Index: {1}".format(page_start_index, page_end_index))

    # If not the first chapter/page, then don't show title again
    # Use line numbers found to get rid of useless parts of book
    # writeable_text = text[page_start_index:page_end_index].rstrip()
    writeable_text = text[page_start_index:page_end_index]
    print(writeable_text)
    book.append(writeable_text)

name_of_txt_file = "Ninth House.txt"
path_to_txt_file = os.path.join(path_to_script_dir, '..\SavedBooks\BookClub', name_of_txt_file)

if (not os.path.exists(os.path.dirname(path_to_txt_file))):
    print("Folder for this book does not exist! Creating it...")
    os.makedirs(os.path.dirname(path_to_txt_file))

# Save text converted html to a file
with open(path_to_txt_file, 'w+') as write_file:
   writeable_text = "\n".join(book)
   writeable_text = unidecode(writeable_text)
   write_file.write(writeable_text)

print("Program Complete!")
