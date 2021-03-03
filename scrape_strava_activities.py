from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import urllib3
import mechanize
import http.cookiejar
from robobrowser import RoboBrowser
import time


werkzeug.cached_property = werkzeug.utils.cached_property

tic=time.perf_counter()

#new attempt: RoboBrowser-- init and go to login
browser = RoboBrowser(history=True)
browser.open('https://strava.com/login')

#get login form
login=browser.get_form()

#login credentials & submit forms
login["email"]='wpeters1998@gmail.com'
login['password']='fib1123581321'

browser.submit_form(login) #, NEED SOMETHING ELSE HERE?)
browser.open('https.strava.com/activities/497490342') #--> test 

#Now it works like beautiful soup?
gear=browser.find_all("span",{"class":"gear-name"})
gear_entry=gear[0].text.strip('\n').strip().encode('utf-8')

#Now we navigate to the pages of interest

#GOING TO NEED TO BE LOGGED IN FOR THIS ONE-- NEED TO CHECK ON THAT.
# Check this link for log-in method: 
## MECHANIZE ATTEMPT-- now works for a limited number of requests:
"""
cj = http.cookiejar.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Chrome')]

# The site we will navigate into, handling it's session
br.open('https://strava.com/login')

# View available forms

for f in br.forms():
    print(f)


br.select_form(nr=0)
br.form['email'] = 'wpeters1998@gmail.com'
br.form['password'] = 'fib1123581321'
br.submit()

#loading data into dataframe
data = pd.read_csv("strava_results_test.csv") #change to wmm_results.csv 

#getting activities in a list
activities= data['data-activity_id'].to_list()


url = "https://strava.com/activities/{}"

with open("activity_data.csv", 'w',newline='') as results_file:
    strava_write=csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
    firstrow=['activity_id','gear']
    strava_write.writerow(firstrow)

    count =0
    for activity in activities:
        
        row=[]
        row.append(activity)
        #get our URL
        activity_url=url.format(activity)+"/overview"
        
        html_content = br.open(activity_url).read()

        #if html_content.status_code == 429:
        #    time.sleep(int(html_content.headers["Retry-After"]))
        
        soup = BeautifulSoup(html_content, "html.parser")

        gear=soup.find_all("span",{"class":"gear-name"})
        if(len(gear)>0):
            gear_entry=gear[0].text.strip('\n').strip().encode('utf-8')
        else:
            gear_entry=b'\xe2\x80\x94'
        
        row.append(gear_entry)
        
        strava_write.writerow(row)

        if (count%100==0):
            print('count: ',count)
            print('gear: ',gear_entry)
        count=count+1

"""
toc =time.perf_counter()
duration = toc - tic
print(f"Completed Execution in {duration:0.2f} seconds")


#REQUESTS METHOD
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
"""