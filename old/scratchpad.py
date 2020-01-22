import pyperclip as clip
import datetime as dt

def func(param: dt.datetime.second,start):
    if param - start > 0.5:
        return True

while True:
    start = dt.datetime.now()
    if func(dt.datetime.now().second,start.second):
        print('yes')