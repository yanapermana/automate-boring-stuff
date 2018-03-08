import requests
import datetime
import time
import smtplib
import schedule
from bs4 import BeautifulSoup

def send_email(body):
        gmail_user = 'xyz@gmail.com'
        gmail_pwd = 'xyz'
        FROM = 'xyz@gmail.com'
        recipient = 'pqr@gmail.com'
        TO = recipient if type(recipient) is list else [recipient]
        SUBJECT = 'KAI - Train Schedule'
        TEXT = body
        # Prepare actual message
        msg = "\r\n".join([
"From: %s" % (FROM),
"To: %s" % (TO),
"Subject: %s" % (SUBJECT),
"",
"%s" % (TEXT)
])
        try:
                server = smtplib.SMTP("smtp.gmail.com:587")
                server.set_debuglevel(1)
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, msg)
                server.close()
                print 'Successfully sent the mail'
        except:
                print "Failed to send mail"

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
		send_email(body)

def check():
	_important_dates = ['29-03-2018','31-05-2018','09-06-2018','11-06-2018']
	_important_dates = ['29-03-2018','31-05-2018']
	for _x in _important_dates:
		job(_x)
		time.sleep(1)

if __name__ == '__main__':
	check()
        schedule.every(3).hours.do(check)
        while True:
                schedule.run_pending()
                time.sleep(1)
