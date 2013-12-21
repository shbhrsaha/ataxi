#!/usr/bin/env python

"""
    Downloads phonebook data to many files in the OUTPUT_FOLDER

    Surnames from http://names.mongabay.com/data/1000.html
    565 towns from http://en.wikipedia.org/wiki/List_of_municipalities_in_New_Jersey
"""

import sys
import Queue
import threading
from config import *
import pandas as pd
from pattern.web import plaintext, download, DOM

TOWN_FILE = "towns.txt"
NAME_FILE = "names.txt"
OUTPUT_FOLDER = "files_phonebook/"

towns = [x.replace("\n","") for x in open(TOWN_FILE,"r").readlines()]
surnames = [x.replace("\n","") for x in open(NAME_FILE,"r").readlines()]

queue = Queue.Queue(maxsize=4)


class Worker(threading.Thread):
    """
        Workers are threads that constantly process jobs
        from the priority queue
    """
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        logging.info("%s : Initialized" % self.getName())
  
    def run(self):
        while True:
            try:
                logging.info("%s : Waiting for surname"  % self.getName())
                surname = self.queue.get()

                row_data = []

                for j, town in enumerate(towns):
                    logging.info("%s : %s \t #%s \t %s"  % (self.getName(), surname, j, town))
                    
                    url = "http://yellowbook.intelius.com/results.php?ReportType=34&refer=2464&adword=RP&qar=off&qc=%s&qdma=off&qi=0&qk=6&qn=%s&qs=NJ" % (town, surname)

                    try:
                        html = unicode(download(url), "latin-1").encode('ascii', 'replace')
                    except KeyboardInterrupt:
                        sys.exit()
                    except:
                        logging.info("Failed.")
                        continue

                    dom = DOM(html)

                    for result in dom('div.cobrand_wp_multiresult_record'):
                        name = plaintext(result('div.cobrand_wp_multiresult_record_name:first-child')[0].content)
                        addr = plaintext(result('div.cobrand_wp_multiresult_record_address')[0].content).replace("\n"," ")
                        phone = plaintext(result('div.cobrand_wp_multiresult_record_phone')[0].content)

                        row_data.append({"name" : name, "addr" : addr, "phone" : phone})

                df = pd.DataFrame(row_data)
                df.to_csv("%s%s.csv" % (OUTPUT_FOLDER,surname), index = False)
                
                logging.info("%s : Processing surname %s complete"  % (self.getName(), surname))
            except:
                pass

if __name__ == "__main__":
    """
        Manage all the threads and 
        add tasks to the queue, as necessary
    """
    for i in range(3):
        t = Worker(queue)
        t.setDaemon(True)
        t.start()

    try:
        skip = int(sys.argv[1])
    except:
        skip = 0

    for i, surname in enumerate(surnames):

        if skip > 0:
            skip -= 1
            continue

        queue.put(surname, block=True)