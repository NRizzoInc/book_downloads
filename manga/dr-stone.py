#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    Converts html file from specific url to text
'''
import os
import sys
import math
import subprocess
import re
path_to_script_dir = os.path.dirname(os.path.abspath(__file__))
path_to_main_dir = os.path.join(path_to_script_dir, "..")
from pathlib import Path
import multiprocessing

sys.path.append(path_to_main_dir)
from numberHelper import * # contains some useful functions

import urllib.request
from bs4 import BeautifulSoup
from unidecode import unidecode
path_to_script_dir = os.path.dirname(os.path.abspath(__file__))
import weasyprint
from joblib import Parallel, delayed

# https://w1.dr-stone-online.com/manga/dr-stone-manga-chapter-232-5/
url_base = "https://w1.dr-stone-online.com/manga/dr-stone-chapter"
url_list = []

# Parse through all urls and add them to list
for i in range(1, 233):
    url_list.append(f"{url_base}-{i}/")
url_list.append("https://w1.dr-stone-online.com/manga/dr-stone-manga-chapter-232-5/")


# print(url_list)
#---------------------------DONE GETTING ALL LINKS-----------------------#

manga_dir_path:Path = (Path(path_to_script_dir).parent / "SavedBooks" / "manga" / "Dr-Stone")

if (not os.path.exists(manga_dir_path)):
    print("Folder for this book does not exist! Creating it...")
    os.makedirs(manga_dir_path)

#----------------- Save Each URL in multi-process to speed up downloads----------------------#

def save_url(url:str, url_num:int):
    ch_dst:Path = manga_dir_path / f"Chapter {url_num}.pdf"
    print(f"Loading from url {url} -> {ch_dst}")
    ch_pdf = weasyprint.HTML(url=url).write_pdf()
    open(ch_dst, 'wb').write(ch_pdf)
    print(f"Finished Downloading Chapter {url_num}")

nproc = multiprocessing.cpu_count()
results = Parallel(n_jobs=nproc-1)(delayed(save_url)(url, url_num) for url_num, url in enumerate(url_list, start=1))


print(f"Program Complete! Saved to {manga_dir_path}")
