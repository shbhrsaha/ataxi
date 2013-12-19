#!/usr/bin/env python

"""
    Imports phonebook data from the ORIGINAL_FOLDER to the database
"""
import os
import sys
import datetime
import pandas as pd
from config import *

logging.basicConfig(level=logging.INFO)

ORIGINAL_FOLDER = "files_phonebook/"

for file_name in os.listdir(ORIGINAL_FOLDER):
    logging.info("Importing %s" % file_name)

    try:
        df = pd.read_csv(ORIGINAL_FOLDER + file_name)
    except:
        continue

    for index, row in df.iterrows():
        try:
            original_addr = row["addr"]
            original_addr_split = original_addr.split("  ")
            addr = original_addr_split[0]

            city_state_zip_split = original_addr_split[1].split(" ")

            zip_code = city_state_zip_split[-1]
            state = city_state_zip_split[-2]
            city = " ".join(city_state_zip_split[:-2]).replace(",","")    

            entry = Phonebook(addr=addr,city=city,state=state,zip_code=zip_code,name=row["name"],phone=row["phone"])
            session.add(entry)
            session.commit()
        except:
            pass