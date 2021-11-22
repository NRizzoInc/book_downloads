#!/bin/bash
# use large number to say "all chapters"
python ../royalroad-reader/fetch_book.py https://www.royalroad.com/fiction/21979/song-of-the-void/chapter/313860/prologue 999999 SongOfTheVoid

echo "Converting SongOfTheVoid.html -> mobi"
sudo apt install -y calibre
ebook-convert SongOfTheVoid.html SongOfTheVoid.mobi

save_dir=../SavedBooks/SongOfTheVoid
mkdir -p $save_dir
mv SongOfTheVoid.mobi $save_dir/SongOfTheVoid.mobi
