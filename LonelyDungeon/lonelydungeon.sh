#!/bin/sh
SCRIPT=$(realpath "$0")
SCRIPTDIR=$(dirname "$SCRIPT")
ROOTDIR=$(realpath "$SCRIPTDIR/..")

BOOK_NAME=LonelyDungeon
SAVE_DIR=$(realpath "$ROOTDIR/SavedBooks/$BOOK_NAME")
HTML_BOOK_PATH_NO_EXT="$SCRIPTDIR/$BOOK_NAME"
HTML_BOOK_PATH="$HTML_BOOK_PATH_NO_EXT.html"
EPUB_BOOK_PATH="$SAVE_DIR/$BOOK_NAME.epub"

# use large number to say "all chapters"
python "$ROOTDIR/royalroad-reader/fetch_book.py" https://www.royalroad.com/fiction/37231/a-lonely-dungeon/chapter/577609/chapter-1-a-lonely-dungeon 999999 "$HTML_BOOK_PATH_NO_EXT"

echo "Converting $HTML_BOOK_PATH -> $EPUB_BOOK_PATH"
mkdir -p "$SAVE_DIR"
if ! command -v "ebook-convert" >/dev/null 2>&1; then
    sudo apt install -y calibre
fi
ebook-convert "$HTML_BOOK_PATH" "$EPUB_BOOK_PATH"

