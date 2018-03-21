from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv
import requests
from bs4 import BeautifulSoup
import datetime
import os

def parse(html):
        header = ['Date', 'Notifier', 'H', 'M', 'R', 'L', 'Star', 'Domain', 'OS', 'View']
        data = {}
        for _ in header:
                data[_] = []

        html_doc = open(html).read().rstrip()
        available = []
        soup = BeautifulSoup(html_doc, 'html.parser')
        table = soup.findAll("table", {"id" : "ldeface" })[0]
        for item in table.findAll('tr'):
                i = 0
                for _,x in enumerate(item.findAll('td')):
                        try:
                                print header[i], x.getText()
                                data[header[i]].append(str(x.getText().rstrip()))
                        except:
                                pass
                        i += 1
        clean = {}
        for _ in header:
                clean[_] = data[_][1:26]
        unique = datetime.datetime.now().strftime('%d%m%Y')
        with open('csv/zone-h-data-collected-at-{}.csv'.format(unique), 'a') as csvfile:
                author = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for i in xrange(25):
                        row = [clean[_][i] for _ in header]
                        author.writerow(row)

os.system('rm csv/* && rm /tmp/*.html')

driver = webdriver.Firefox()
driver.set_window_size(768, 512)
driver.get("http://www.zone-h.org/archive")

while 'captcha' in driver.page_source:
    elem = driver.find_element_by_name("captcha")
    elem.clear()
    challenge = raw_input('> ')
    elem.send_keys(challenge)
    elem.send_keys(Keys.RETURN)
    sleep(5)

elements = driver.find_elements_by_xpath("//a[@href]")
for elem in elements:
    if '/archive/filter=1' in elem.get_attribute("href"):
        elem.click()
        sleep(5)
        break

elem = driver.find_element_by_class_name("domaininput")
elem.clear()
challenge = 'id'
elem.send_keys(challenge)
elem.send_keys(Keys.RETURN)
sleep(5)

while 'captcha' in driver.page_source:
    elem = driver.find_element_by_name("archivecaptcha")
    elem.clear()
    challenge = raw_input('> ')
    elem.send_keys(challenge)
    elem.send_keys(Keys.RETURN)
    sleep(5)

i = 1
unique = '{}-{}'.format(i,datetime.datetime.now().strftime('%d%m%Y'))
filename = '/tmp/zone-h-archive-page-{}.html'.format(unique)
with open(filename, 'w') as f:
    f.write(driver.page_source)
parse(filename)

for i in xrange(2, 50+1, 1):
    sleep(5)
    elements = driver.find_elements_by_xpath("//a[@href]")
    for elem in elements:
        try:
            if '/page={}'.format(i) in elem.get_attribute("href"):
                elem.click()
                sleep(5)
                unique = '{}-{}'.format(i,datetime.datetime.now().strftime('%d%m%Y'))
                filename = '/tmp/zone-h-archive-page-{}.html'.format(unique)
                with open(filename, 'w') as f:
                    f.write(driver.page_source)
                parse(filename)
                break
        except:
            print '[!] ERROR: Ctrl+Z'
            break
            # driver.refresh()
            # elem.send_keys(Keys.RETURN)

sleep(5)
driver.close()