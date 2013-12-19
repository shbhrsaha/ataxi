
aTaxi Project
=============

The goal of this project is the model the behavior of the NJ transportation system when an autonomous taxi network is implemented.

Developed in [Alain Kornhauser's ORF 467 Transportation Class Fall 2013](http://www.princeton.edu/~alaink/).

System Requirements
-------------------
- A completed config.json file in the home directory
- A database named 'transportation'
- Run config.py to populate the database with tables 
- Python 2.7 and other libraries, available from PyPi

Source File Descriptions
------------------------
- config.py -- Usually imported in every script. Loads the config file and connects to the database.
- phonebook_download.py -- Downloads name data from the phonebook, going down the names file and repeating for each town.
- phonebook_import.py -- Imports the downloaded name data to the database
