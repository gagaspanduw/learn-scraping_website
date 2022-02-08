from xml.etree.ElementTree import tostring
import requests
from bs4 import BeautifulSoup
import csv
 
key = input('please enter the term :')
location = input('please enter the location too :')
rangedata = int(input('please input range page to collect:'))
url = 'https://www.yell.com/ucs/UcsSearchAction.do?scrambleSeed=1673388186&keywords={}&location={}&pageNum='.format(key, location)
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}

 
datas = []
count_page = 0
for page in range(0, rangedata):
    count_page+=1
    print('scraping page :',count_page)
    req = requests.get(url+str(page), headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    items = soup.findAll('div', 'row businessCapsule--mainRow')
    for it in items:
        name = it.find('h2', 'businessCapsule--name text-h2').text
        try : address = ''.join(it.find('span', {'itemprop':'address'}).text.strip().split('\n'))
        except : address = ''
        try : web = it.find('a', {'rel':'nofollow noopener'})['href'].replace('http://', '').replace('www.', '').replace('https://', '').split('/')[0]
        except : web = ''
        try : telp = it.find('span', 'business--telephoneNumber').text
        except: telp= ''
        image = it.find('div', 'col-sm-4 col-md-4 col-lg-5 businessCapsule--leftSide').find('img')['data-original']
        if 'http' not in image: image = 'https://www.yell.com{}'.format(image)
        datas.append([name, address, web, telp, image])
 
kepala = ['Name', 'Address', 'Website', 'Phone Number', 'Image URL']
writer = csv.writer(open('result/{}_{}.csv'.format(key, location), 'w', newline=''))
writer.writerow(kepala)
for d in datas: writer.writerow(d)