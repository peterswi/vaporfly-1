from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import urllib3
import http.cookiejar
import time
import sys
import mechanicalsoup
from passwords import user_pass

#setup counter-- counter%4==1 goes to first, 2 to second, 3 to third, 4th to rest

#GOING TO NEED TO BE LOGGED IN FOR THIS SCRAPE
def scrape_activities(inputList):
    tic=time.perf_counter()
    # TRY THIS USING MULTIPLE ACCOUNTS / BROWSERS?
    


    inputCsv=inputList[0]
    outCsv=inputList[1]

    user=user_pass[3][0]
    password=user_pass[3][1]
    print('Users and Pass:')
    print(user,password)
    #MECHANICAL SOUP-- 
    #could do for loop and loop through 
    browser = mechanicalsoup.Browser(soup_config={'features': 'lxml'}, user_agent='MyBot/0.1: mysite.example.com/bot_info')
    login_page = browser.get("https://strava.com/login")
    login_page.raise_for_status()
    login_form = mechanicalsoup.Form(login_page.soup.select_one('#login_form'))
    login_form.input({"email":user, "password": password})
    page2 = browser.submit(login_form, login_page.url)
    print(page2)
    #REQUEST LIMIT IS 1000/day, 100/15min
    # RANDOM SAMPLING?


    print('"""""')
    #loading data into dataframe-- NOW USING OUR SAMPLED DATASET
    data = pd.read_csv(inputCsv) 

    #getting activities in a list
    activities= data['data-activity_id'].to_list()
    

    url = "https://strava.com/activities/{}"


    with open(outCsv, 'w',newline='') as results_file:
        strava_write=csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
        firstrow=['activity_id','shoes','device','suffer']
        strava_write.writerow(firstrow)

        count =0
        userCount=0
        for activity in activities[:]:
            
            row=[]
            row.append(activity)
            #get our URL
            activity_url=url.format(activity)+"/overview"

            nav_page=browser.get(activity_url)

            
            if (nav_page.status_code ==200): 
                html_content = nav_page.text

                soup = BeautifulSoup(html_content, "html.parser")
                #GEt Shoes
                gear=soup.find_all("span",{"class":"gear-name"})
                if(len(gear)>0):
                    gear_entry=gear[0].text.strip('\n').strip().encode('utf-8')
                else:
                    gear_entry=b'\xe2\x80\x94'
                
                row.append(gear_entry)
                #Get Device
                gear2=soup.find("div",{"class":"device spans8"})
                if(gear2):
                    device_entry=gear2.text.strip('\n').strip().encode('utf-8')
                else:
                    device_entry=b'\xe2\x80\x94'
                row.append(device_entry)

                #Get Suffer
                suffer=soup.find("li",{"class":"suffer-score"})
                
                if(suffer):
                    suffer=suffer.find('strong')
                    suffer_entry=suffer.text.strip('\n').strip().encode('utf-8')
                else:
                    suffer_entry=b'\xe2\x80\x94'
                row.append(suffer_entry)

                #write our row
                strava_write.writerow(row)
                if (count%100==1):
                    print('count: ',count)
                    print('gear: ',gear_entry)
                    print('device: ',device_entry)
                    print('suffer score: ',suffer_entry)
            # what if we got rid of this sleep call?... just let it run till a 429. making this sleep after count=1000 to simulate
                if ((count%2000==0)and(count>0)):
                    print('""""""')
                    print('count: ',count)
                    print('sleeping for 15 min to avoid requests problem')
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    print(current_time)
                    time.sleep(900)
                    print('awake!')
                    print('"""""')
    
                    
            else: 
                #iterating through all 3 accounts
                
                userCount=userCount+1
                if (userCount%3==1):
                    user=user_pass[1][0]
                    password=user_pass[1][1]
                    print('Users and Pass:')
                    print(user,password)
                    #MECHANICAL SOUP-- 
                    #could do for loop and loop through 
                    browser = mechanicalsoup.Browser(soup_config={'features': 'lxml'}, user_agent='MyBot/0.1: mysite.example.com/bot_info')
                    login_page = browser.get("https://strava.com/login")
                    login_page.raise_for_status()
                    login_form = mechanicalsoup.Form(login_page.soup.select_one('#login_form'))
                    login_form.input({"email":user, "password": password})
                    page2 = browser.submit(login_form, login_page.url)
                    print(page2)

                    #Send browser to page again
                    nav_page=browser.get(activity_url)
                    print('Awake after error, new response:',nav_page.status_code)
                    print('""""""')
                    html_content = nav_page.text

                elif (userCount%3==2):
                    user=user_pass[2][0]
                    password=user_pass[2][1]
                    print('Users and Pass:')
                    print(user,password)
                    #MECHANICAL SOUP-- 
                    #could do for loop and loop through 
                    browser = mechanicalsoup.Browser(soup_config={'features': 'lxml'}, user_agent='MyBot/0.1: mysite.example.com/bot_info')
                    login_page = browser.get("https://strava.com/login")
                    login_page.raise_for_status()
                    login_form = mechanicalsoup.Form(login_page.soup.select_one('#login_form'))
                    login_form.input({"email":user, "password": password})
                    page2 = browser.submit(login_form, login_page.url)
                    print(page2)

                    #Send browser to page again
                    nav_page=browser.get(activity_url)
                    print('Awake after error, new response:',nav_page.status_code)
                    print('""""""')
                    html_content = nav_page.text

                else:
                    print('""""""')
                    print('Error Code ',nav_page.status_code,'. Sleeping for 60 minutes, then trying again.')
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    print(current_time)
                    time.sleep(3600)
                
                    user=user_pass[3][0]
                    password=user_pass[3][1]
                    print('Users and Pass:')
                    print(user,password)
                    #MECHANICAL SOUP-- 
                    #could do for loop and loop through 
                    browser = mechanicalsoup.Browser(soup_config={'features': 'lxml'}, user_agent='MyBot/0.1: mysite.example.com/bot_info')
                    login_page = browser.get("https://strava.com/login")
                    login_page.raise_for_status()
                    login_form = mechanicalsoup.Form(login_page.soup.select_one('#login_form'))
                    login_form.input({"email":user, "password": password})
                    page2 = browser.submit(login_form, login_page.url)
                    print(page2)

                    #Send browser to page again
                    nav_page=browser.get(activity_url)
                    print('Awake after error, new response:',nav_page.status_code)
                    print('""""""')
                    html_content = nav_page.text
                    
                soup = BeautifulSoup(html_content, "html.parser")
                #GEt Shoes
                gear=soup.find_all("span",{"class":"gear-name"})
                if(len(gear)>0):
                    gear_entry=gear[0].text.strip('\n').strip().encode('utf-8')
                else:
                    gear_entry=b'\xe2\x80\x94'
                
                row.append(gear_entry)
                #Get Device
                gear2=soup.find("div",{"class":"device spans8"})
                if(gear2):
                    device_entry=gear2.text.strip('\n').strip().encode('utf-8')
                else:
                    device_entry=b'\xe2\x80\x94'
                row.append(device_entry)

                #Get Suffer
                suffer=soup.find("li",{"class":"suffer-score"})
                
                if(suffer):
                    suffer=suffer.find('strong')
                    suffer_entry=suffer.text.strip('\n').strip().encode('utf-8')
                else:
                    suffer_entry=b'\xe2\x80\x94'
                row.append(suffer_entry)

                #write our row
                strava_write.writerow(row)
                if (count%100==1):
                    print('count: ',count)
                    print('gear: ',gear_entry)
                    print('device: ',device_entry)
                    print('suffer score: ',suffer_entry)
            
            if (count%25==1):
                print('count: ',count)
                time.sleep(2)
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                print(current_time)
            count=count+1


    toc =time.perf_counter()
    duration = toc - tic
    print(f"Completed Execution in {duration:0.2f} seconds")

# PROGRAM CALLS UP NEXT:

scrape_activities([user_pass[2][0],user_pass[2][1],'inputCsv/input8.csv','outputActivityCsv/output8.csv'])
scrape_activities([user_pass[3][0],user_pass[3][1],'inputCsv/input9.csv','outputActivityCsv/output9.csv'])
scrape_activities([user_pass[1][0],user_pass[1][1],'inputCsv/input10.csv','outputActivityCsv/output10.csv'])

#scrape_activities(user_pass[3][0],user_pass[3][1],'inputCsv/input4.csv','outputActivityCsv/output4.csv')

#down here, could just line up like 10 program calls. or could let maxwell's computer try PARALLEL processing

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

"""
#mechanical browser
# THIS IS A STATEFUL BROWSER-- seems to be time consuming
browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features': 'lxml'},
    raise_on_404=True,
    user_agent='MyBot/0.1: mysite.example.com/bot_info',
)
browser.open("https://www.strava.com/login")
print(browser.url)

browser.select_form('form[action="/session"]')


#fill Log in form
browser["email"]=user
browser["password"]=password
browser["remember_me"]="on"
print("New Form")
browser.form.print_summary()

#submit form
response=browser.submit_selected()
page = browser.page
print(page.title.text)

"""