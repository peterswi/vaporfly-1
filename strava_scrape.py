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

# generic strava browse url and makelinks url ?? 
#Unclear purpose of makelinks rn
browse_url = "https://www.strava.com/running_races"
makelinks_url = "https://www.strava.com/running_races/makelinks.cfm"

post_data = {
    "RaceRange" : "",
    "MIDD" : "",
    "SubmitButton" : "View"
}
headers = {
    "Referer" : "",
    "User-Agent" : ("Mozilla/5.0 (Windows NT 6.1; WOW64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/34.0.1847.116 Safari/537.36")
}

