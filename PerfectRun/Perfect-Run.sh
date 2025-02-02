#!/bin/bash
# use large number to say "all chapters"
python ../royalroad-reader/fetch_book.py https://www.royalroad.com/fiction/36735/the-perfect-run/chapter/569225/1-quicksave 999999 ThePerfectRun

echo "Converting ThePerfectRun.html -> epub"
sudo apt install -y calibre
ebook-convert ThePerfectRun.html ThePerfectRun.epub
mv ThePerfectRun.epub ../SavedBooks/ThePerfectRun/ThePerfectRun.epub
