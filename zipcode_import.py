"""
    Imports zip code data from ZIP_CODE_FILE to the database
"""
import os
import sys
import datetime
import numpy as np
import pandas as pd

from config import *

ZIP_CODE_FILE = "zipcode.csv"

df = pd.read_csv(ZIP_CODE_FILE, dtype={"zip":np.str_})

total_row_count = len(df.index)

logging.info("Import %s entries" % total_row_count)

for index, row in df.iterrows():
    entry = Zipcodes(zip_code=row["zip"],city=row["city"],state=row["state"],latitude=row["latitude"],longitude=row["longitude"])
    session.add(entry)
    session.commit()    

    if index % 1000 == 0:
        logging.info("Imported %s entries" % index)