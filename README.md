## Selecting companies with a Glassdoor Rating > 4.0 from all the companies attending the Birkbeck Careers Fair of 2018.
#### It's recommended you work through the jupyter-notebook file, download it and run it through. I wish GitHub had jupyter-notebook integration.
##### Fine print: Unfortunately Glassdoor searches aren't perfect. Try it!: Search for Circus Street, and the first result is "GP Open Evening"...Second place goes to Circus Street.

![Glassdoor Search](https://i.imgur.com/DbtPSra.png)


## Acquiring the company names from the Birkbeck Career's Website
```python
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
```

## Macmillan != MacMillan Cancer Research
```python
# Need to update a few companies so they get searched on Glassdoor better. Macmillan -> Macmillan Cancer Research
companyList["MacMillan"]["search_name"] = "MacMillan+Cancer+Research"
companyList
```
## This is the result of webscraping: 
    {'Alliance Visas': {'rating': ' 3.7', 'search_name': 'Alliance+Visas'},
     'ASOS': {'rating': ' 3.6', 'search_name': 'ASOS'},
     'Betway Group': {'rating': ' 3.4', 'search_name': 'Betway+Group'},
     'Binti': {'rating': 0, 'search_name': 'Binti'},
     'Bio Nano Consulting': {'rating': 0, 'search_name': 'Bio+Nano+Consulting'},
     'Capco': {'rating': ' 3.8', 'search_name': 'Capco'},
     'Centre 404': {'rating': ' 4.2', 'search_name': 'Centre+404'},
     'Circus Street': {'rating': ' 3.4', 'search_name': 'Circus+Street'},
     'City Year UK': {'rating': ' 3.5', 'search_name': 'City+Year+UK'},
     'Code First Girls': {'rating': ' 4.0', 'search_name': 'Code+First+Girls'},
     'CREST': {'rating': ' 2.9', 'search_name': 'CREST'},
     'Dozens': {'rating': ' 4.2', 'search_name': 'Dozens'},
     'Frontier': {'rating': ' 4.9', 'search_name': 'Frontier'},
     'Future Frontier': {'rating': ' 3.8', 'search_name': 'Future+Frontier'},
     'Government Social Research': {'rating': ' 4.2',
      'search_name': 'Government+Social+Research'},
     'Harvey Nichols': {'rating': ' 3.4', 'search_name': 'Harvey+Nichols'},
     'HS. Live': {'rating': ' 3.1', 'search_name': 'HS.+Live'},
     'International SOS': {'rating': ' 3.3', 'search_name': 'International+SOS'},
     'IntoUniversity': {'rating': 0, 'search_name': 'IntoUniversity'},
     'JobTeaser': {'rating': ' 4.4', 'search_name': 'JobTeaser'},
     'KPMG': {'rating': ' 3.7', 'search_name': 'KPMG'},
     'Le Cordon Bleu': {'rating': 0, 'search_name': 'Le+Cordon+Bleu'},
     'London Fire Brigade': {'rating': ' 3.0',
      'search_name': 'London+Fire+Brigade'},
     'MacMillan': {'rating': ' 5.0', 'search_name': 'MacMillan+Cancer+Research'},
     'Mayor’s Entrepreneur 2019': {'rating': 0,
      'search_name': 'Mayor’s+Entrepreneur+2019'},
     'Metro Bank': {'rating': 0, 'search_name': 'Metro+Bank'},
     'Metropolitan Police': {'rating': 0, 'search_name': 'Metropolitan+Police'},
     'Oxford Business Group Emergent Market Consultancy Company': {'rating': 0,
      'search_name': 'Oxford+Business+Group+Emergent+Market+Consultancy+Company'},
     'Role Models': {'rating': 0, 'search_name': 'Role+Models'},
     'Scarborough Teaching Alliance': {'rating': 0,
      'search_name': 'Scarborough+Teaching+Alliance'},
     'SLV Global': {'rating': 0, 'search_name': 'SLV+Global'},
     'Smaller Earth': {'rating': 0, 'search_name': 'Smaller+Earth'},
     'Sparta Global': {'rating': 0, 'search_name': 'Sparta+Global'},
     'Square One Resources': {'rating': 0, 'search_name': 'Square+One+Resources'},
     'StartSmart': {'rating': 0, 'search_name': 'StartSmart'},
     'Streetbees': {'rating': 0, 'search_name': 'Streetbees'},
     'Studio Graphene': {'rating': 0, 'search_name': 'Studio+Graphene'},
     'Teach First': {'rating': 0, 'search_name': 'Teach+First'},
     'Thames Reach': {'rating': 0, 'search_name': 'Thames+Reach'},
     'The Challenge': {'rating': 0, 'search_name': 'The+Challenge'},
     'The OR Society': {'rating': 0, 'search_name': 'The+OR+Society'},
     'Travel Teacher': {'rating': 0, 'search_name': 'Travel+Teacher'},
     'University of Law': {'rating': 0, 'search_name': 'University+of+Law'},
     'VOLO': {'rating': 0, 'search_name': 'VOLO'}}



## Now to query Glassdoor for the ratings, through simple url's. (GET requests)
```python
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
```
## These are the ratings. To be specific, this is the rating of the first company that pops up. 
     3.7
     3.6
     3.4
    Glassdoor failure for (couldn't find a company): 
     https://www.glassdoor.co.uk/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=Binti&sc.keyword=Binti&locT=N&locId=2&jobType=
    Glassdoor failure for (couldn't find a company): 
     https://www.glassdoor.co.uk/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=Bio+Nano+Consulting&sc.keyword=Bio+Nano+Consulting&locT=N&locId=2&jobType=
     3.8
     4.2
     5.0
     3.5
     4.0
     2.9
     3.2
     4.9
     3.8
     4.2
     3.4
     4.5
     3.3
    Glassdoor failure for (couldn't find a company): 
     https://www.glassdoor.co.uk/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=IntoUniversity&sc.keyword=IntoUniversity&locT=N&locId=2&jobType=
     4.4
     3.7
    Glassdoor failure for (couldn't find a company): 
     https://www.glassdoor.co.uk/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=Le+Cordon+Bleu&sc.keyword=Le+Cordon+Bleu&locT=N&locId=2&jobType=
     3.0
     3.2
    Urlopen failure for: 
     https://www.glassdoor.co.uk/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=Mayor’s+Entrepreneur+2019&sc.keyword=Mayor’s+Entrepreneur+2019&locT=N&locId=2&jobType=
     4.1
     2.9
     3.1
     4.6
    Glassdoor failure for (couldn't find a company): 
     https://www.glassdoor.co.uk/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=Scarborough+Teaching+Alliance&sc.keyword=Scarborough+Teaching+Alliance&locT=N&locId=2&jobType=
     4.7
    Glassdoor failure for (couldn't find a company): 
     https://www.glassdoor.co.uk/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=Smaller+Earth&sc.keyword=Smaller+Earth&locT=N&locId=2&jobType=
     3.1
     3.8
    Glassdoor failure for (couldn't find a company): 
     https://www.glassdoor.co.uk/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=StartSmart&sc.keyword=StartSmart&locT=N&locId=2&jobType=
     3.4
    Glassdoor failure for (couldn't find a company): 
     https://www.glassdoor.co.uk/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=Studio+Graphene&sc.keyword=Studio+Graphene&locT=N&locId=2&jobType=
     3.4
     3.8
     5.0
     3.8
     5.0
     4.0
    Glassdoor failure for (couldn't find a company): 
     https://www.glassdoor.co.uk/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=VOLO&sc.keyword=VOLO&locT=N&locId=2&jobType=
    

## To extract companies with ratings > 4.0.
```python
for companyName, value in companyList.items():
    if float(value["rating"]) > 4:
        print(companyName)
```

    Centre 404
    Circus Street
    Dozens
    Frontier
    Government Social Research
    HS. Live
    JobTeaser
    Metro Bank
    SLV Global
    The Challenge
    
    
## I did this pretty quickly, but really should have commented some parts of it, and added more pictures to this readme. But there you have it, out of all the companies attending the Birkbeck Career's Fair on the 4th of November 2018, there are 10 companies that have a glassdoor rating > 4.0.
