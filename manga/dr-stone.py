#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    Converts html file from specific url to text
'''
import os
from typing import List
import json
from pathlib import Path
import multiprocessing
import weasyprint
from joblib import Parallel, delayed
from PyPDF2 import PdfFileMerger
import requests
from requests import Response
from bs4 import BeautifulSoup, ResultSet


def get_url_list() -> List[str]:
    # https://w1.dr-stone-online.com/manga/dr-stone-manga-chapter-232-5/
    url_base = "https://w1.dr-stone-online.com/manga/dr-stone-chapter-1/"
    rtn_url_list = []

    # get "next" url since some have parts instead of incremental
    current_url = url_base
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
            link.get("rel") != None and "next" in link.get("rel")
        ]
        if len(next_url) == 0:
            break
        current_url = next_url[0]["href"]

    return rtn_url_list


#----------------- Save Each URL in multi-process to speed up downloads----------------------#
def save_url(url:str, url_num:int, dst: Path):
    ch_dst:Path = dst / f"Chapter {url_num}.pdf"
    print(f"Loading from url {url} -> {ch_dst}")
    # dont load a page if it already is saved
    if not os.path.exists(ch_dst):
        ch_pdf = weasyprint.HTML(url=url).write_pdf()
        if ch_pdf != None:
            open(ch_dst, 'wb').write(ch_pdf)
        print(f"Finished Downloading Chapter {url_num}")
    else:
        print(f"Chapter {url_num} already downloaded")

def download_pdfs(pdf_urls: List[str], dst_dir):
    nproc = multiprocessing.cpu_count()
    Parallel(n_jobs=nproc-1)(
        delayed(save_url)(url, url_num, dst_dir) for url_num, url in enumerate(pdf_urls, start=1)
    )

def is_pdf(file: str) -> bool:
    return file.endswith(".pdf")

def get_all_pdfs(pdfdir: Path, fullpath:bool=False) -> List[str]:
    files = list(filter(is_pdf, os.listdir(pdfdir)))
    if not fullpath:
        return files

    return [str(pdfdir / f) for f in files]


def get_num_pdf_in_dir(pdfdir: Path) -> int:
    return len(get_all_pdfs(pdfdir))

def merge_pdfs(pdfdir: Path, combined:Path):
    merger = PdfFileMerger()
    def extract_ch(filename: str) -> int:
        # in format: "Chapter #.pdf"
        end = filename.split("Chapter ")[1]
        return int(end.removesuffix(".pdf"))
    pdfs_except_final = filter(lambda x: x != str(combined), get_all_pdfs(pdfdir, True))
    pdfs = sorted(pdfs_except_final, key=extract_ch)
    for file in pdfs:
        merger.append(file)
    merger.write(str(combined))
    merger.close()


if __name__ == "__main__":
    path_to_script_dir = os.path.dirname(os.path.abspath(__file__))
    download_dir_path:Path = (Path(path_to_script_dir).parent / "SavedBooks" / "manga" / "Dr-Stone")

    if (not os.path.exists(download_dir_path)):
        print("Folder for this book does not exist! Creating it...")
        os.makedirs(download_dir_path)

    url_list = get_url_list()
    print(f"url_list = {json.dumps(url_list, indent=2)}")
    # account for already having merged them
    if get_num_pdf_in_dir(download_dir_path) < len(url_list):
        download_pdfs(url_list, download_dir_path)

    print("Merging pdfs into one")
    final_dst:Path = download_dir_path / "Dr-Stone.pdf"
    merge_pdfs(download_dir_path, final_dst)

    print(f"Chapters saved to {download_dir_path}")
    print(f"Manga saved to {final_dst}")

