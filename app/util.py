import datetime
from flask import request

def get_month (year: int, weekday: int):
    start = datetime.datetime (year=year, month=1, day=1)
    '''
    Weekday correction:
    source: https://www.calendar-week.org/
    "In Europe, the first calendar week of the year is the week that
    contains four days of the new year."
    '''
    if start.weekday () >= 4:
        start += datetime.timedelta (days=7-start.weekday ())
    else:
        start -= datetime.timedelta (days=start.weekday ())
    start += datetime.timedelta (days=7*(weekday-1))
    return [start + datetime.timedelta(days=i) for i in range (0, 7)]

def get_month_days(
    weeknum=datetime.date(
        datetime.date.today().year,
        datetime.date.today().month,
        datetime.date.today().day).isocalendar()[1]):
    days = list()
    for i in range(weeknum,weeknum+5):
        days.append(list(map (lambda x: str (x.date()), get_month (2022, i))))

    return days


def isLogin():
    LogedIn = False
    userID = request.cookies.get("userID")
    if userID != None :
        LogedIn = True
    
    return LogedIn
# print(datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day).isocalendar())
# print(list(map (lambda x: str (x.date()), get_month (2022, 10))))
# print(get_month_days())