from bs4 import BeautifulSoup
import requests

url="https://www.strava.com/running_races/2"

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "html5lib")
#print(soup.prettify()) # print the parsed data of html
print(soup.title)

results_table=soup.find("table",attrs={"id":"results_table"})
print("table:",results_table)
results_table_data=results_table.tbody.find_all("tr")

headings = []
for td in results_table_data[0].find_all("th"):
    # remove any newlines and extra spaces from left and right
    headings.append(td.b.text.replace('\n', ' ').strip())

print(headings)