import webbrowser
from bs4 import BeautifulSoup as bs
import urllib.request
import json

with urllib.request.urlopen('http://www.bbk.ac.uk/student-services/careers-service/birkbeck-careers-fair') as f:
    data = f.read().decode('utf-8')
soup = bs(data, 'html.parser')
companies = soup.find_all(class_="content-pull-down")[1].find_all("strong")
companyList = {}
for company in companies:
    companyList[company.text] = {"rating": 0}

for i in companyList:
    companyList[i]["search_name"] = i.replace(' ', '+')
	
# Need to update a few companies so they get searched on Glassdoor better. Macmillan -> Macmillan Cancer Research
companyList["MacMillan"]["search_name"] = "MacMillan+Cancer+Research"
companyList

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,} 

for companyName, value in companyList.items():
    search_name = value["search_name"]
    get_request = "https://www.glassdoor.co.uk/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword={}&sc.keyword={}&locT=N&locId=2&jobType=".format(search_name, search_name)
#     print(get_request)
    send = urllib.request.Request(get_request, headers=headers)
    try:
        with urllib.request.urlopen(send) as file:
            data = file.read().decode('utf-8')
        soup = bs(data, 'html.parser')
        try:
            rating = soup.find('span', class_="compactStars").text
            print(rating)
            if float(rating) > 4:
                webbrowser.open_new_tab(get_request)
            companyList[companyName]["rating"] = rating
        except:
            print("Glassdoor failure for (couldn't find a company): \n", get_request)
    except:
        print("Urlopen failure for: \n", get_request)
    
# Select companies with rating > 4 and print.

for companyName, value in companyList.items():
    if float(value["rating"]) > 4:
        print(companyName)
