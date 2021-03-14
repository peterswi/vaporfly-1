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
                print('429 encountered')
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

scrape_activities(['inputCsv/input13.csv','outputActivityCsv/output13.csv'])
scrape_activities(['inputCsv/input14.csv','outputActivityCsv/output14.csv'])
scrape_activities(['inputCsv/input15.csv','outputActivityCsv/output15.csv'])
scrape_activities(['inputCsv/input16.csv','outputActivityCsv/output16.csv'])



#down here, could just line up like 10 program calls. or could let maxwell's computer try PARALLEL processing

