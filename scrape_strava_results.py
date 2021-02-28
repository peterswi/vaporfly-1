# THIS FILE SCRAPES STRAVA RACE RESULTS PAGES FROM THE 6 WMM BETWEEN
# 2014-2019 WHERE AVAILABLE. STEP ONE IN RECREATING NYT VAPORFLY STUDY.

from bs4 import BeautifulSoup
import requests
import csv

import time

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys


"""
    NOW: we are scraping one page successfully, now we want to be able to scrape multiple pages
    of results within that page, and also keep it specific to men vs women.

    Suggested way would be to use Selenium & BeautifulSoup together?

    SEE THIS TUTORIAL: https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25
"""
##SELENIUM ATTEMPT
"""
options = webdriver.ChromeOptions()
#options.add_argument('--ignore-certificate-errors')
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options) #not sure if there should be an executable path here?
driver.get(url)

gender_switches=driver.find_element_by_class_name("switches")
next_results=driver.find_element_by_class_name("next_page")
print(next_results)
driver.execute_script("arguments[0].click();",next_results)
for x in range(len(next_results)):
  if next_results[x].is_displayed():
      driver.execute_script("arguments[0].click();", next_results[x])
      print('hello')
      time.sleep(1)


page_source = driver.page_source
print('done')
driver.quit()

"""
"""
SUCCESFUL BEAUTIFUL SOUP SCRAPE OF STATIC PAGE:
"""
## MISSING MARATHONS: 2016 Berlin, 2016 NYC, 2014 tokyo, 2019 tokyo, 2017 London
races=['2014-Boston-Marathon','2015-Boston-Marathon','2016-Boston-Marathon','2017-Boston-Marathon','2018-Boston-Marathon','2019-Boston-Marathon','2014-Berlin-Marathon','2015-Berlin-Marathon','2017-BMW-Berlin-Marathon','2018-BMW-Berlin-Marathon','2019-BMW-Berlin-Marathon','2014-New-York-City-Marathon','2015-New-York-City-Marathon','2017-TCS-New-York-City-Marathon','2018-TCS-New-York-City-Marathon','2019-TCS-New-York-City-Marathon','2014-Chicago-Marathon','2015-Chicago-Marathon','2016-Chicago-Marathon','2017-Chicago-Marathon','2018-Chicago-Marathon','2019-Chicago-Marathon','2015-Tokyo-Marathon','2016-Tokyo-Marathon','2017-Tokyo-Marathon','2018-Tokyo-Marathon','2015-London-Marathon','2016-London-Marathon','2018-Virgin-Money-London-Marathon','2019-Virgin-Money-London-Marathon']
races2=['2014-Boston-Marathon','2015-Boston-Marathon','2016-Boston-Marathon']

#added a timer
tic=time.perf_counter()

url="https://www.strava.com/running_races/{}"
#Write data to CSV
with open("wmm_results.csv", 'w',newline='') as results_file:
    #init our csv
    strava_write=csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    firstRow=['Rank', 'Name', 'Gender', 'Age', 'Finish', 'Pace', 'Strava Activity', 'data-activity_id', 'athlete_id','race_name']
    strava_write.writerow(firstRow)

    
    #iterate through rest of results pages
    #NOW--> create list of races to iterate through
    #iterate starting on second page
    for race_name in races:
        race_url=url.format(race_name)
        print(race_url)
        #first want to figure out how many pages there are
        url_iter = race_url + '/results?gender=ALL&page={}'.format(1)
        print(url_iter)
        # Make a GET request to fetch the raw HTML content
        html_content = requests.get(url_iter).text

        # Parse the html content
        soup = BeautifulSoup(html_content, "html.parser")

        results_section=soup.find(id="results-table")

        result_table=results_section.find_all('tr')
        
        headers= result_table[0].find_all('th')
        pages=soup.find_all("div",{"class":"pages"})
        numResults=pages[0].text.strip()
        index=numResults.find('f',0,len(numResults))
        numPages=int(numResults[index+2:])//20
        if numPages>101:
            numPages=101
        print("number of results pages to be scraped:",numPages-1)
        for i in (range(len(result_table))[1:]):
                    data=result_table[i].find_all('td')
                    row=[]
                    for item in data:
                        entry=item.text.strip('\n').strip()
                        row.append(entry.encode('utf-8'))
                    links=result_table[i].find_all('a', href=True)  
                    row.append(result_table[i].attrs['data-activity_id'])
                    row.append(links[0]['href'][10:])
                    row.append(race_name)
                    strava_write.writerow(row)
        
        #starting at page 2 and iterating through all results
        for page in range(2,numPages):
            url_iter = race_url + '/results?gender=ALL&page={}'.format(page)
            if (page%25==0):
                print(url_iter)
            # Make a GET request to fetch the raw HTML content
            html_content = requests.get(url_iter).text

            # Parse the html content
            soup = BeautifulSoup(html_content, "html.parser")

            results_section=soup.find(id="results-table")

            result_table=results_section.find_all('tr')
            
            headers= result_table[0].find_all('th')

            #SHOULD I ITERATE SEPARATELY OVER MEN AND WOMEN?

            for i in (range(len(result_table))[1:]):
                data=result_table[i].find_all('td')
                row=[]
                for item in data:
                    entry=item.text.strip('\n').strip()
                    row.append(entry.encode('utf-8'))
                links=result_table[i].find_all('a', href=True)  
                row.append(result_table[i].attrs['data-activity_id'])
                row.append(links[0]['href'][10:])
                row.append(race_name)
                strava_write.writerow(row)

    #MIGHT NOT NEED SELENIUM,READ:
    """
    url takes the form : https://www.strava.com/running-races/2019-boston-marathon?gender=ALL&page=100
    can just iterate over a certain number of pages for all marathons of interest by changing page variable
    """
#finish timing
toc =time.perf_counter()
duration = toc - tic
print(f"Completed Execution in {duration:0.2f} seconds")
"""
When capping results @ 2000 results per race, total run time is 902 seconds (15 minutes)
"""