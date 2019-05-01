'''
    Converts html file from specific url to text
'''
import os
import sys
import subprocess

# pip necessary modules 
piped_modules = subprocess.check_output(['pip', 'list']).decode()
if 'bs4' not in piped_modules: os.system("pip install bs4")
if 'unidecode' not in piped_modules: os.system("pip install unidecode")

import urllib.request
from bs4 import BeautifulSoup
from unidecode import unidecode

path_to_script_dir = os.path.dirname(os.path.abspath(__file__))

url_base = "http://www.newfreenovels.com/robert-jordan/the-eye-of-the-world"
url_list = []
first_entry = url_base + ".html"
# First entry doesnt follow convention so manually add it in
url_list.append(str(first_entry))

# Parse through all urls and add them to list
for i in range(2, 200):  # Book is 199 pages long (200-1)
    url_list.append(url_base + "_" + str(i) + ".html")

# Pull from each url and concat text
book = []
for url_num, url in enumerate(url_list):

    if url_num == 1: # for some reason enumerate starts from 1
        print("Loading txt from url: " + url_list[0])
    print("Loading txt from url " + url)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()
    # text = text.replace('\u0439', '')
    page_start_index = 0
    page_end_index = 0
    start_found = False
    end_found = False
    lines = text.splitlines()

    # Parse through page and check for key words that mark the beg and end of the page
    for i, line in enumerate(lines):
        # This will always mark the beginining of the page
        if "The Eye of the World" in line and "online free by Robert Jordan" not in line and start_found is False:
            page_start_index = i
            start_found = True

        elif "199 Pages:" in line and end_found is False:
            page_end_index = i
            end_found = True

    # If not the first chapter/page, then dont show title again

    # Use line numbers found to get rid of useless parts of book
    writeable_text = '\n'.join(lines[page_start_index:page_end_index]) # TODO maybe get rid of "book" stuff
    book.append(writeable_text)
    book_final_copy = '\n'.join(book)
    # print(writeable_text)

    # Save results to a file (appends current page to book)- only save every 3
    # Deal with size issue (cant concat more than 4 into one txt file)
    #if ((url_num+1) % 5) == 0 and url_num != 0: # since url_num starts from 0, need to offset url_num by one so that first trigger happens at 4 mod 4
    #    print("Printing on url_num " + str(url_num+1))

name_of_txt_file = "The Eye of the World (Wheel of Time, Book 1)"
path_to_txt_file = os.path.join(path_to_script_dir, name_of_txt_file)

# Save text converted html to a file
with open(path_to_txt_file, 'w+') as write_file:
    writeable_text = "\n".join(book)
    writeable_text = unidecode(writeable_text)
    write_file.write(writeable_text)

