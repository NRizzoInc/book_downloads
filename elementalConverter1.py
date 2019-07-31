'''
    Converts html file from specific url to text
'''
import os
import sys
import subprocess
import math

# pip necessary modules 
piped_modules = subprocess.check_output(['python', '-m', 'pip', 'list']).decode()
if 'bs4' not in piped_modules: subprocess.call("python -m pip install bs4")
if 'unidecode' not in piped_modules: subprocess.call("python -m pip install unidecode")

import urllib.request
from bs4 import BeautifulSoup
from unidecode import unidecode
path_to_script_dir = os.path.dirname(os.path.abspath(__file__))


def numToWord(num):
    numDict = {
        # there will never be a chapter zero, but this is needed
        # for numbers whos ones place of is zero (10, 20, 30, ...)
        '0': '', 
        '1': 'one',
        '2': 'two',
        '3': 'three',
        '4': 'four',
        '5': 'five',
        '6': 'six',
        '7': 'seven',
        '8': 'eight',
        '9': 'nine',
        '10': 'ten',
        '11': 'eleven',
        '12': 'twelve',
        '13': 'thirteen',
        '14': 'fourteen',
        '15': 'fifteen',
        '16': 'sixteen',
        '17': 'seventeen',
        '18': 'eighteen',
        '19': 'nineteen'
    }

    tensDigitDict = {
        '2': 'twenty',
        '3': 'thirty',
        '4': 'fourty',
        '5': 'fifty',
        '6': 'sixty',
        '7': 'seventy',
        '8': 'eighty',
        '9': 'ninety'
    }

    if num < 20:
        # since numbers 1-20 are weird have to hard code them
        toReturn = numDict[str(num)]
    
    elif num >= 20:
        # get the number that is contained in the tens and one digit
        tensDigit = math.trunc(num/10)
        onesDigit = num % 10 # mod by ten to get one's digit

        prefix =  tensDigitDict[str(tensDigit)]
        suffix = numDict[str(onesDigit)]

        if onesDigit != 0:
            toReturn = prefix + '-' + suffix
        else:
            toReturn = prefix

    return toReturn

# http://www.readfreenovelsonline.com/spark/page-1-1065772
url_base = "http://www.readfreenovelsonline.com/spark/page-"
ending_num_base = 1065772
url_list = []

# Parse through all urls and add them to list
for i in range(1, 107): # there are 106 pages (starting from 1 to 106 = 107)
    ending_num = ending_num_base + i - 1 # subtract 1 to account for starting at 1 (not zero)  
    full_url = url_base + "{0}-{1}".format(i, ending_num)
    url_list.append(full_url)


print(url_list)
#---------------------------DONE GETTING ALL LINKS-----------------------#


#-----------------PULL TEXT FROM EACH URL----------------------#
#book = []
#for url_num, url in enumerate(url_list):
#
#    print("Loading txt from url " + url)
#    
#    # sometimes need to make a request before extracting from url
#    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
#    html = urllib.request.urlopen(request).read()
#    soup = BeautifulSoup(html, features="html.parser")
#
#    # kill all script and style elements
#    for script in soup(["script", "style"]):
#        script.extract()    # rip it out
#
#    # get text
#    text = soup.get_text()
#    page_start_index = 0
#    page_end_index = 0
#    lines = text.splitlines()
#
#    # print(text)
#
#    # Parse through page and check for key words that mark the beg and end of the page
#    # This will always mark the beginining of the page
#    if url_num == 0:
#        # first page is different
#        beg_phrase = "        Next Book One"
#    else:
#        beg_phrase = "        Next "
#    end_phrase = "Loading...     Prev"
#    page_start_index = text.index(beg_phrase) + len(beg_phrase) 
#    page_end_index = text.index(end_phrase)
#
#    print("Start index: {0}\nEnd Index: {1}".format(page_start_index, page_end_index))
#
#    # If not the first chapter/page, then dont show title again
#    # Use line numbers found to get rid of useless parts of book
#    writeable_text = text[page_start_index:page_end_index]
#    book.append(writeable_text)
#    # print(writeable_text)
#
#name_of_txt_file = "Dune (Book 1)"
#path_to_txt_file = os.path.join(path_to_script_dir, 'SavedBooks', name_of_txt_file)
#
## Save text converted html to a file
#with open(path_to_txt_file, 'w+') as write_file:
#   writeable_text = "\n".join(book)
#   writeable_text = unidecode(writeable_text)
#   write_file.write(writeable_text)
#
#