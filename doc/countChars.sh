#!/bin/bash
# sudo apt install poppler-utils
pdftotext "$1.pdf" && cat "$1.txt" | awk NF | wc -m && rm "$1.txt"