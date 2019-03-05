import requests


def wkd2d(week_list, index):
    return "".join(week_list[int(index)%7].split('-'))


def lessons2time(lessons):
    index = int((int(lessons[1]) - 1) / 2)
    hour = [['080000', '095000'], ['101000', '120000'], ['140000', '155000'], ['161000', '180000'],
              ['190000', '215000']]
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
    'year': '2018-2019',
    'term': '2',
    'week': '1'
}
session = requests.session()
r=session.post(url=login_url, data=login_data)

f = open('kb.ics', 'w', encoding='utf-8')
f.write(u"BEGIN:VCALENDAR\nVERSION:2.0\n")
for week in range(1, 19):
    course_data['week'] = week
    response = session.post(url=course_url, data=course_data)
    course_list = response.json()['d']['classes']
    date_list = response.json()['d']['weekdays']
    for course in course_list:
        for item in course_list[course]:
            if not isinstance(course_list[course][item],list):
                hour = lessons2time(course_list[course][item]['lessons'])
                day = wkd2d(date_list, course_list[course][item]['weekday'])
                message = u'''BEGIN:VEVENT
SUMMARY:%s
DTSTART;TZID="UTC+08:00";VALUE=DATE-TIME:%sT%s
DTEND;TZID="UTC+08:00";VALUE=DATE-TIME:%sT%s
LOCATION:%s--%s
END:VEVENT\n''' % (course_list[course][item]['course_name'], day, hour[0], day, hour[1], course_list[course][item]['location'], course_list[course][item]['teacher'])
                f.write(message)
f.write(u"END:VCALENDAR")
f.close()
