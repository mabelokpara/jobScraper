from bs4 import BeautifulSoup
import requests
import csv

#variable that we will later pass into requests
#we will use the scraperapi in order to handle all of these requests
url = 'http://api.scraperapi.com?api_key=81465bfd152aec8b0e527fec640fd11f&url=https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Software%20Engineer&location=California,%20United%20States&geoId=102095887&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=0'

#variable to store the requests that we will get back from the url
response = requests.get(url)
print(response)

#creating a beautifulSoup object. this will help us get the raw data
soup = BeautifulSoup(response.content, 'html.parser')
job_title = soup.find('h3', class_='base-search-card__title').text
print(job_title)

#function to help build http query
def linkedin_scraper(webpage, page_number):
    #the next_page variable combines webpage + page_number, and then converts it into a string
    next_page = webpage + str(page_number)
    print(str(next_page))

    #passes in the next_page variable into requests
    response = requests.get(str(next_page))
    soup = BeautifulSoup(response.content, 'html.parser')
    print(response)
    print(page_number)

    if page_number < 25:
        page_number = page_number +25
        linkedin_scraper(webpage,page_number)
        linkedin_scraper('https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Software%20Engineer&location=California,%20United%20States&geoId=102095887&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=', 0)

jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')

#this loop will loop through the h3, h4, span and a elements in order to grab the data
for job in jobs:
    job_title = job.find('h3', class_='base-search-card__title').text.strip()
    job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
    job_location = job.find('span', class_='job-search-card__location').text.strip()
    job_link = job.find('a', class_='base-card__full-link')['href']

    #this will send the data that we grabbed above into a CSV file
    file = open('linkedin-jobs.csv', 'a')
    writer = csv.writer(file)
    writer.writerow(['Title', 'Company', 'Location', 'Apply'])

    #appends the data that was received into a new row in THE CSV file
    writer.writerow([
    job_title.encode('utf-8'),
    job_company.encode('utf-8'),
    job_location.encode('utf-8'),
    job_link.encode('utf-8')
    ])

else:
    file.close()
    print('File closed')