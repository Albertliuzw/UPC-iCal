#by 张世琛
import requests


def wkd2d(week_list, index):
    return "".join(week_list[int(index)%7].split('-'))


def lessons2time(lessons):
    index = int((int(lessons[1]) - 1) / 2)
    hour = [['080000', '095000'], ['101000', '120000'], ['140000', '155000'], ['161000', '180000'],
              ['190000', '205000']]
    return hour[index]


login_url = 'https://app.upc.edu.cn/uc/wap/login/check'
username = input("学号:")
passwd = input("数字石大密码:")
login_data = {
    'username': username,
    'password': passwd,
}
course_url = "https://app.upc.edu.cn/timetable/wap/default/get-data"
course_data = {
    'year': '2019-2020',
    'term': '1',
    'week': '1'
}
session = requests.session()
r=session.post(url=login_url, data=login_data)

f = open('kb1.ics', 'w', encoding='utf-8')
f.write(u"BEGIN:VCALENDAR\nVERSION:2.0\n")
for week in range(1, 19):
    course_data['week'] = week
    response = session.post(url=course_url, data=course_data)
    course_list = response.json()['d']['classes']
    date_list = response.json()['d']['weekdays']
    for course in course_list:
        hour = lessons2time(course['lessons'])
        day = wkd2d(date_list,course['weekday'])
        message = u'''BEGIN:VEVENT
SUMMARY:%s
DTSTART;TZID="UTC+08:00";VALUE=DATE-TIME:%sT%s
DTEND;TZID="UTC+08:00";VALUE=DATE-TIME:%sT%s
LOCATION:%s--%s
END:VEVENT\n''' % (course['course_name'], day, hour[0], day, hour[1],course['location'],course['teacher'])
        f.write(message)
f.write(u"END:VCALENDAR")
f.close()
