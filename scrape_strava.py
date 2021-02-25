from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#BOSTON MARATHON 2014-- Sample Data
url="https://www.strava.com/running_races/2018-boston-marathon"

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

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "html.parser")
#print(soup.prettify()) # print the parsed data of html
print("Page Title: ",soup.title)

results_section=soup.find(id="results-table-container")
#print(results_section.prettify())
result_table=results_section.find_all('tr')

#Write data to CSV
with open("strava_results_test.csv", 'w',newline='') as results_file:
    strava_write=csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    headers= result_table[0].find_all('th')
    firstRow=[]
    print('here')
    for header in headers:
        firstRow.append(header.text)
    firstRow.append('data-activity_id')
    strava_write.writerow(firstRow)
    for i in (range(len(result_table))[1:]):
        data=result_table[i].find_all('td')
        row=[]
        for item in data:
            entry=item.text.strip('\n').strip()
            row.append(entry.encode('utf-8'))
        row.append(result_table[i].attrs['data-activity_id'])
        print(row)
        strava_write.writerow(row)

#MIGHT NOT NEED SELENIUM,READ:
"""
url takes the form : https://www.strava.com/running-races/2019-boston-marathon?gender=ALL&page=100
can just iterate over a certain number of pages for all marathons of interest by changing page variable
"""