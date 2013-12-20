#!/usr/bin/env python

"""
    Downloads the NN CSV files from the ORF 467 web site
"""

import os
from pattern.web import URL, DOM, plaintext

BASE_URL = "http://orfe.princeton.edu/~alaink/NJ_aTaxiOrf467F13/%5bABC%5dModule7NN_New/"
NN_FOLDER = "files_nn/"

already_downloaded = os.listdir(NN_FOLDER)

url = URL(BASE_URL)
dom = DOM(url.download(cached=True))
for a in dom('a'):
    file_name = plaintext(a.href)

    if file_name in already_downloaded:
        continue

    if "csv" not in file_name:
        continue
    
    print file_name

    file_url = URL(BASE_URL + file_name)
    data = file_url.download()

    with open(NN_FOLDER + file_name, "w") as f:
        f.write(data)
        f.close()