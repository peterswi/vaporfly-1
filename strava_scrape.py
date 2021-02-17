# GOING TO TRY TO START SCRAPING STRAVA RACE PAGES USING
# JOE GUINNESS' CODE AS A TEMPLATE

import sys
try:
    assert sys.version_info[0] == 3
except:
    print("User does not have python3")
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

