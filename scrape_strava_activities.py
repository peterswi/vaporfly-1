from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import urllib3
import mechanize
import http.cookiejar
import time
from fake_useragent import UserAgent
import mechanicalsoup

#GOING TO NEED TO BE LOGGED IN FOR THIS SCRAPE

tic=time.perf_counter()
user='wpeters1998@gmail.com'
password='fib1123581321'

#MECHANICAL SOUP
#Try this url: https://mechanicalsoup.readthedocs.io/en/stable/tutorial.html
browser = mechanicalsoup.StatefulBrowser()
browser.open("https://www.strava.com/login")
print(browser.url)

browser.select_form('form[action="/session"]')
browser.form.print_summary()

#fill Log in form
browser["email"]=user
browser["password"]=password
browser["remember_me"]="on"
print("New Form")
browser.form.print_summary()

#submit form
response=browser.submit_selected()
page2=browser.open("https://www.strava.com/settings/profile")


soup = BeautifulSoup(page2.text, 'html.parser')
head=soup.find("div",{'id':'my-profile'})
print('profile:',head.find("h1"))


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
        
        html_content = session.get(activity_url).text

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


toc =time.perf_counter()
duration = toc - tic
print(f"Completed Execution in {duration:0.2f} seconds")




"""


## MECHANIZE ATTEMPT-- now works for a limited number of requests:

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
for f in br.forms():
    print(f)


br.select_form(nr=0)
br.form['email'] = 'wpeters1998@gmail.com'
br.form['password'] = 'fib1123581321'
br.submit()

"""


"""
# ROBO BROWSER ATTEMPT:
from robobrowser import RoboBrowser

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
"""


"""
import lxml.html
def strava_login(service, username, password):
    # GET parameters - URL we'd like to log into.
    params = {'service': service}
    LOGIN_URL = 'https://strava.com/login'

    # Start session and get login form.
    session = requests.session()
    login = session.get(LOGIN_URL, params=params)

    # Get the hidden elements and put them in our form.
    login_html = lxml.html.fromstring(login.text)
    hidden_elements = login_html.xpath('//form//input[@type="hidden"]')
    print(hidden_elements)
    form = {x.attrib['name']: x.attrib['value'] for x in hidden_elements}

    # "Fill out" the form.
    form['username'] = username
    form['password'] = password

    # Finally, login and return the session.
    session.post(LOGIN_URL, data=form, params=params)
    return session
testSesh=strava_login("https://www.strava.com/settings/profile",user, password)
soup = BeautifulSoup(testSesh.text, 'html.parser')
head=soup.find("div",{'id':'my-profile'})
print('profile:',head)
"""

"""
#REQUESTS METHOD
ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}

session = requests.Session()
session.headers=header
payload = {'action':'/session'}
sec = session.get("https://www.strava.com/login")
signin = BeautifulSoup(sec._content, 'html.parser')
token=signin.find('input', {'name':'authenticity_token'})['value']


#at this point need to figure out WHAT to put in this payload
payload['authenticity_token'] = token
# payload["#__VIEWSTATE"]=viewstate
# payload["#__VIEWSTATEGENERATOR"]=viewstategenerator
payload['email']=user
payload['password']=password
print('payload:',payload)
s = session.post("https://www.strava.com/login", data=payload, verify=False)
p= session.get("https://www.strava.com/settings/profile")
#THIS IS NOT POSTING CORRECTLY

"""