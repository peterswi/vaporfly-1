from bs4 import BeautifulSoup
import requests
import csv

url="https://www.strava.com/running_races/2"

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "html.parser")
#print(soup.prettify()) # print the parsed data of html
print("Page Title: ",soup.title)

results_section=soup.find(id="results-table-container")
#print(results_section.prettify())
result_table=results_section.find_all('tr')

"""
for i in range(len(result_table)):
    print("result",i,": ",result_table[i].prettify())
"""


#Write data to CSV
with open("strava_results_test.csv", 'w',newline='') as results_file:
    strava_write=csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    headers= result_table[0].find_all('th')
    firstRow=[]
    for header in headers:
        firstRow.append(header.text)
    strava_write.writerow(firstRow)
    for i in (range(len(result_table))[1:]):
        data=result_table[i].find_all('td')
        row=[]
        for item in data:
            row.append(item.text.strip('\n').strip())
        row.append(result_table[i].attrs['data-activity_id'])
        strava_write.writerow(row)

"""
headings = []
for td in results_table_data[0].find_all("th"):
    # remove any newlines and extra spaces from left and right
    headings.append(td.b.text.replace('\n', ' ').strip())

print(headings)
"""