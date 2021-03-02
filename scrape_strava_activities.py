from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import urllib3
import mechanize
import http.cookiejar

import time

tic=time.perf_counter()
#GOING TO NEED TO BE LOGGED IN FOR THIS ONE-- NEED TO CHECK ON THAT.
# Check this link for log-in method: 
""" MECHANIZE ATTEMPT:
cj = http.cookiejar.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.open("https://strava.com/activities/318124113/overview")

br.select_form(nr=0)
br.form['email'] = 'wpeters1998@gmail.com'
br.form['password'] = 'fib1123581321'
br.submit()

print(br.response().read())
"""

session = requests.Session()
payload = {'email':'wpeters1998@gmail.com', 
          'password':'fib1123581321'
         }

s = session.post("https://www.strava.com/session", data=payload)
#THIS IS NOT POSTING CORRECTLY
s = session.get("https://www.strava.com/settings/profile")
soup = BeautifulSoup(s.text, 'html.parser')
print(soup.prettify)
#loading data into dataframe
data = pd.read_csv("strava_results_test.csv") #change to wmm_results.csv 

#getting activities in a list
activities= data['data-activity_id'].to_list()


url = "strava.com/activities/{}"


for activity in activities:
    #get our URL
    activity_url=url.format(activity)+"/overview"
    
    html_content = session.get(activity_url).text

    soup = BeautifulSoup(html_content, "html.parser")

    gear=soup.find_all("span",{"class":"gear-name"})
    print(gear)










toc =time.perf_counter()
duration = toc - tic
print(f"Completed Execution in {duration:0.2f} seconds")