from bs4 import BeautifulSoup
import requests
import time

# to get user input before running the script
print('Put some skill that you are not familiar with')
unfamiliar_skill = input('>')
print(f'Filtering out {unfamiliar_skill}')

def find_jobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')
    with open(f'result/result.txt', 'w') as f:
        for job in jobs:
            published_date = job.find('span', class_ = 'sim-posted').span.text
            # to filter the job with word few
            if 'few' in published_date:
                company_name = job.find('h3', class_ = 'joblist-comp-name').text.replace(' ', '')
                skills = job.find('span', class_ = 'srp-skills').text.replace(' ', '')
                more_info = job.header.h2.a['href']
                if unfamiliar_skill not in skills:
                    # to create file
                    # \n for jump to next line or like <\br> in html
                    # f.write to write text into a file
                    f.write(f"Company Name: {company_name.strip()} \n")
                    f.write(f"Required Skills: {skills.strip()} \n")
                    f.write(f'More Info: {more_info} \n')
                    f.write('')
    print(f'File saved')

    # create one file for every single jobs
    # for index, job in enumerate(jobs):
    #     published_date = job.find('span', class_ = 'sim-posted').span.text
    #     # to filter the job with word few
    #     if 'few' in published_date:
    #         company_name = job.find('h3', class_ = 'joblist-comp-name').text.replace(' ', '')
    #         skills = job.find('span', class_ = 'srp-skills').text.replace(' ', '')
    #         more_info = job.header.h2.a['href']
    #         if unfamiliar_skill not in skills:
    #             # to create file
    #             with open(f'result/{index}.txt', 'w') as f:
    #                 # \n for jump to next line or like <\br> in html
    #                 # f.write to write text into a file
    #                 f.write(f"Company Name: {company_name.strip()} \n")
    #                 f.write(f"Required Skills: {skills.strip()} \n")
    #                 f.write(f'More Info: {more_info}')
    #                 f.write('')
    #             print(f'File saved {index}')

# to run scraping every 10 minutes
if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 1
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
