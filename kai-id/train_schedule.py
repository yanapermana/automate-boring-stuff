import requests
import datetime
from bs4 import BeautifulSoup

def scrap(html_doc):
	available = []
	soup = BeautifulSoup(html_doc, 'html.parser')
	# print html_doc
	table = soup.findAll("table", {"class" : "itReservationTable" })[0]
	for item in table.findAll('tr'):
		if 'HARINA' in item.text:
			if 'Pesan' in item.text:
				available.append(item.text)
	return available

def job():
	_date = datetime.datetime.now().strftime('%d-%B-%Y')
	_date_int = datetime.datetime.now().strftime("%Y%m%d")
	url = 'https://kai.id/'
	s = requests.Session()
	r = s.get(url)
	# print r.cookies['csrf_cookie_kai_id']
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
	# print data, _date_int, _date
	result = s.post(url=url, data=data)
	body = scrap(result.content)
	if body:
		for x in body:
			print x

if __name__ == '__main__':
	job()
