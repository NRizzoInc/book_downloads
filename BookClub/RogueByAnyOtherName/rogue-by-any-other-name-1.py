#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    Converts html file from specific url to text
'''
import os
from typing import List, Union
import json
from pathlib import Path
import multiprocessing
import urllib.request
from joblib import Parallel, delayed
from PyPDF2 import PdfFileMerger
import requests
from requests import Response
from bs4 import BeautifulSoup, ResultSet, PageElement

def get_url_list() -> List[str]:
    # "https://novel12.com/a-rogue-by-any-other-name/page-1-1912197.htm"
    url_base = "https://novel12.com/a-rogue-by-any-other-name/page"
    rtn_url_list = []

    # get "next" url since some have parts instead of incremental
    current_url = "https://novel12.com/a-rogue-by-any-other-name/page-1-1912197.htm"
    while True:
        print(f"Found URL {current_url}")
        rtn_url_list.append(current_url)
        # try request a couple times
        cnt = 0
        html:Response = Response()
        while html.status_code != 200 and cnt < 5:
            html = requests.get(
                current_url,
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=60
            )
            cnt += 1
        if html is None:
            break

        soup = BeautifulSoup(html.text, "lxml") # lxml is just the parser for reading the html
        links:ResultSet = soup.find_all("a", href=True)
        next_url = [link for link in links if
            link["href"] != None and url_base in link["href"] and link["href"] not in rtn_url_list
        ]
        if len(next_url) == 0:
            break
        current_url = next_url[0]["href"]

    return rtn_url_list


#----------------- Save Each URL in multi-process to speed up downloads----------------------#
def save_url(url:str, url_num:int, dst: Path):
    pg_dst:Path = dst / f"Page {url_num}.txt"
    print(f"Loading from url {url} -> {pg_dst}")
    # dont load a page if it already is saved
    if os.path.exists(pg_dst):
        print(f"Page {url_num} already downloaded")
        return

    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(request).read()
    soup:BeautifulSoup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    # text:str = soup.get_text()
    text_or_none:Union[None, PageElement] = soup.find("div", {"class":"content-center"})
    text = text_or_none.text if text_or_none else ""
    # print(f"Page {url_num}:\n{text}")

    # If not the first chapter/page, then don't show title again
    # Use line numbers found to get rid of useless parts of book
    # writeable_text = text[page_start_index:page_end_index].rstrip()
    writeable_text = text

    # remove bad spacings within text bc of html
    writeable_text = writeable_text.strip() + "\n"
    writeable_text = writeable_text.replace("                       \n", "")

    with open(pg_dst, "w", encoding="utf-8") as pg_writeable:
        pg_writeable.write(writeable_text)

    print(f"Finished Downloading Page {url_num}: {url}")

def download_pages(page_urls: List[str], dst_dir):
    nproc = multiprocessing.cpu_count()
    Parallel(n_jobs=nproc-1)(
        delayed(save_url)(url, url_num, dst_dir) for url_num, url in enumerate(page_urls, start=1)
    )

def is_txt(file: str) -> bool:
    return file.endswith(".txt")

def get_all_txts(txtdir: Path, fullpath:bool=False) -> List[str]:
    files = list(filter(is_txt, os.listdir(txtdir)))
    if not fullpath:
        return files

    return [str(txtdir / f) for f in files]


def get_num_txts_in_dir(txtdir: Path) -> int:
    return len(get_all_txts(txtdir))

def merge_txts(txtdir: Path, combined:Path):
    merged_txt:List[str] = []
    def extract_ch(filename: str) -> int:
        # in format: "Page #.txt"
        end = filename.split("Page ")[1]
        return int(end.removesuffix(".txt"))
    txts_except_final = filter(lambda x: x != str(combined), get_all_txts(txtdir, True))
    txtfiles = sorted(txts_except_final, key=extract_ch)
    for file in txtfiles:
        with open(file, "r", encoding="utf-8") as page_r:
            merged_txt.append(page_r.read())

    with open(combined, "w", encoding="utf-8") as combined_w:
        combined_w.write("\n".join(merged_txt))



if __name__ == "__main__":
    path_to_script_dir = os.path.dirname(os.path.abspath(__file__))
    BOOK_TITLE:str ="A Rogue By Any Other Name"
    download_dir_path:Path = (Path(path_to_script_dir).parent.parent / "SavedBooks" / "BookClub" / BOOK_TITLE)

    if not os.path.exists(download_dir_path):
        print("Folder for this book does not exist! Creating it...")
        os.makedirs(download_dir_path)

    url_list = get_url_list()
    print(f"url_list = {json.dumps(url_list, indent=2)}")

    # account for already having merged them
    if get_num_txts_in_dir(download_dir_path) < len(url_list):
        download_pages(url_list, download_dir_path)

    print("Merging txt files into one")
    final_dst:Path = download_dir_path / f"{BOOK_TITLE}.txt"
    merge_txts(download_dir_path, final_dst)

    print(f"Pages saved to \"{download_dir_path}\"")
    print(f"Book saved to \"{final_dst}\"")
