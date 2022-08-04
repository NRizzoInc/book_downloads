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
from typing import List
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
from PyPDF2 import PdfFileReader, PdfFileMerger

def get_url_list() -> List[str]:
    # https://w1.dr-stone-online.com/manga/dr-stone-manga-chapter-232-5/
    url_base = "https://w1.dr-stone-online.com/manga/dr-stone-chapter"
    url_list = []

    # Parse through all urls and add them to list
    for i in range(1, 233):
        url_list.append(f"{url_base}-{i}/")
    url_list.append("https://w1.dr-stone-online.com/manga/dr-stone-manga-chapter-232-5/")
    # print(url_list)
    return url_list

#----------------- Save Each URL in multi-process to speed up downloads----------------------#
def save_url(url:str, url_num:int, dst: Path):
    ch_dst:Path = dst / f"Chapter {url_num}.pdf"
    print(f"Loading from url {url} -> {ch_dst}")
    ch_pdf = weasyprint.HTML(url=url).write_pdf()
    open(ch_dst, 'wb').write(ch_pdf)
    print(f"Finished Downloading Chapter {url_num}")

def download_pdfs(url_list: List[str], dst_dir):
    nproc = multiprocessing.cpu_count()
    results = Parallel(n_jobs=nproc-1)(
        delayed(save_url)(url, url_num, dst_dir) for url_num, url in enumerate(url_list, start=1)
    )

def is_pdf(file: str) -> bool:
    return file.endswith(".pdf")

def get_all_pdfs(dir: Path, fullpath:bool=False) -> List[str]:
    files = list(filter(is_pdf, os.listdir(dir)))
    if not fullpath:
        return files
    else:
        return [str(dir / f) for f in files]


def get_num_pdf_in_dir(dir: Path) -> int:
    return len(get_all_pdfs(dir))

def merge_pdfs(dir: Path, combined:Path):
    merger = PdfFileMerger()
    def extract_ch(filename: str) -> int:
        # in format: "Chapter #.pdf"
        end = filename.split("Chapter ")[1]
        return int(end.removesuffix(".pdf"))
    pdfs_except_final = filter(lambda x: x != str(combined), get_all_pdfs(dir, True))
    pdfs = sorted(pdfs_except_final, key=extract_ch)
    for file in pdfs:
        merger.append(file)
    merger.write(str(combined))
    merger.close()


if __name__ == "__main__":
    download_dir_path:Path = (Path(path_to_script_dir).parent / "SavedBooks" / "manga" / "Dr-Stone")

    if (not os.path.exists(download_dir_path)):
        print("Folder for this book does not exist! Creating it...")
        os.makedirs(download_dir_path)

    url_list = get_url_list()
    # account for already having merged them
    if get_num_pdf_in_dir(download_dir_path) < len(url_list):
        download_pdfs(url_list, download_dir_path)

    final_dst:Path = download_dir_path / "Dr-Stone.pdf"
    merge_pdfs(download_dir_path, final_dst)

    print(f"Program Complete! Saved to {download_dir_path}")

