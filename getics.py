#by田康康
import datetime
import json
from datetime import date
import datetime

import requests

n = 1
date = datetime.datetime(2019, 9, 8)  # + datetime.timedelta(days=1)


# print(date)
# date = date(2019, 9, 8).time.__format__('%Y%m%d')

class JWXT:
	def __init__(self, acount, pwd):
		self.url = 'http://jwxt.upc.edu.cn/app.do?'
		self.header = {
			'User-Agent': 'Mozilla/5.0 (Linux; U; Mobile; Android 6.0.1;C107-9 Build/FRF91 )',
			'Referer': 'http://www.baidu.com',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'zh-CN,zh-TW;q=0.8,zh;q=0.6,en;q=0.4,ja;q=0.2',
			'cache-control': 'max-age=0'
		}
		self.number = acount
		self.pwd = pwd
		self.ss = self.login()

	def login(self):
		# http: // jwxt.xxxx.edu.cn / app.do?method = authUser & xh = {$学号} & pwd = {$密码}
		# cong = requests.get(url).content
		# print(cong)
		params = {
			"method": "authUser",
			"xh": self.number,
			"pwd": self.pwd
		}
		session = requests.session()
		req = session.get(self.url, params = params, timeout = 5, headers = self.header)
		s = json.loads(req.text)
		print(s['msg'])
		self.header['token'] = s['token']
		return session

	def getKbcxAzc(self, zc):
		# s = json.loads(getCurrentTime())
		params = {
			"method": "getKbcxAzc",
			# "xnxqid": s['xnxqh'], 选择学期，默认为当前学期
			"zc": zc,
			"xh": self.number
		}
		req = self.ss.get(self.url, params = params, headers = self.header)
		#print(req.text)
		return req.text

	def timeTrans(self, time):
		index = int((int(time[2]) - 1) / 2)
		icstime = [['080000', '095000'], ['101000', '120000'], ['140000', '155000'], ['161000', '180000'],
		           ['190000', '205000']]
		return icstime[index]

	def create_ics(self, f):
		global date
		for week in range(1, 20):
			courses = json.loads(self.getKbcxAzc(week))
			for index, course in enumerate(courses):
				if course is None:
					break
				day = (date + datetime.timedelta(days = int(course['kcsj'][0]))).strftime('%Y%m%d')
				hour = self.timeTrans(course['kcsj'])
				message = '''BEGIN:VEVENT
SUMMARY:%s
DTSTART;TZID="UTC+08:00";VALUE=DATE-TIME:%sT%s
DTEND;TZID="UTC+08:00";VALUE=DATE-TIME:%sT%s
LOCATION:%s--%s
END:VEVENT\n''' % (
					str(index + 1) + course['kcmc'], day, hour[0], day, hour[1], course['jsmc'], course['jsxm'])
				f.write(message)
			date += datetime.timedelta(days = 7)
			print(date)


number = input('请输入学号')
pwd = input('请输入密码')
print(date)
jw = JWXT(number, pwd)
f = open('kb1.ics', 'w', encoding = 'utf-8')
f.write(u"BEGIN:VCALENDAR\nVERSION:2.0\n")
jw.create_ics(f)
f.write(u"END:VCALENDAR")
f.close()
