import requests
import datetime
import time
from bs4 import BeautifulSoup

def scrap(html_doc):
	available = []
	soup = BeautifulSoup(html_doc, 'html.parser')
	table = soup.findAll("table", {"class" : "itReservationTable" })[0]
	for item in table.findAll('tr'):
		if 'HARINA' in item.text:
			if 'Pesan' in item.text:
				available.append(item.text)
	return available

def job(_departure_date):
	_tmp = datetime.datetime.strptime(_departure_date, "%d-%m-%Y")
	_date = _tmp.strftime('%d-%B-%Y')
	_date_int = _tmp.strftime("%Y%m%d")
	url = 'https://kai.id/'
	s = requests.Session()
	r = s.get(url)
	data = {
		'csrf_kai_id_cookies': r.cookies['csrf_cookie_kai_id'],
		'origination': 'BD',
		'destination': 'SBI',
		'departure_dateh': _date,
		'tanggal': '{}#{}'.format(_date_int, _date),
		'adult': 1,
		'infant': 0,
	}
	url = 'https://kai.id/train_schedule'
	result = s.post(url=url, data=data)
	body = scrap(result.content)
	if body:
		for x in body:
			print x

if __name__ == '__main__':
	_important_dates = ['29-03-2018','31-05-2018','09-06-2018','11-06-2018']
	_important_dates = ['29-03-2018','31-05-2018']
	for _x in _important_dates:
		job(_x)
		time.sleep(1)
