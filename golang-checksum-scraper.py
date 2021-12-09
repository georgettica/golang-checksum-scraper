#!/usr/bin/env python3
import platform
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

# this is copied from
# https://towardsdatascience.com/web-scraping-scraping-table-data-1665b6b2271c

url = "https://golang.org/dl/"
# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse HTML code for the entire site
soup = BeautifulSoup(html_content, "lxml")

divs = soup.find_all("div", attrs={"id": "go1.17"})

div = divs[0]  # Typing breaks here :(
gbp = div.find_all("table", attrs={"class": "downloadtable"})

table1 = gbp[0]
body = table1.find_all("tr")
head = body[0]  # 0th item is the header row

# Declare empty list to keep Columns names
headings = []
for item in head.find_all("th"):  # loop through all th elements
    # convert the th elements to text and strip "\n"
    item = (item.text).rstrip("\n")
    # append the clean column name to headings
    headings.append(item)

body_rows = body[1:]
all_rows = []  # will be a list for list for all rows
for row_num in range(len(body_rows)):  # A row at a time
    row = []  # this will old entries for one row
    for row_item in body_rows[row_num].find_all("td"):  # loop through all row entries
        # row_item.text removes the tags from the entries
        # the following regex is to remove \xa0 and \n and comma from row_item.text
        # xa0 encodes the flag, \n is the newline and comma
        # separates thousands in numbers
        aa = re.sub("(\xa0)|(\n)|,", "", row_item.text)
        # append aa to row - note one row entry is being appended
        row.append(aa)
    # append one row to all_rows
    all_rows.append(row)

df = pd.DataFrame(data=all_rows, columns=headings)

processor = platform.processor().replace("_", "-")
if not processor:
    processor = "x86-64"

df = df[
    (df["Kind"] == "Archive")
    & (df["OS"] == platform.system())
    & (df["Arch"] == processor)
]

print(df["SHA256 Checksum"].values[0])
