#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import requests, sys, re
from bs4 import BeautifulSoup as bs

def getsrc(_in=165, _out=155):
    r = requests.get("http://www.hakobus.jp/result.php?in={0}&out={1}".format(_in, _out))
    return r.text.encode("Shift_JIS", 'ignore').decode("utf-8", 'ignore')

def get_next_bus_time(src):
    soup = bs(src, "html.parser")
    trlist = soup.find_all('tr')
    left_minutes = []

    for tr in trlist:

        td = tr.find(attrs={"width": "160"})
        if td is None:
            continue
        row_data = td.text

        if "*" in row_data:
            left_minutes.append('*****')
            continue

        # strip strings
        tmp = re.sub("\D", "", row_data)

        if tmp == "":
            continue

        left = int(re.sub("\D", "", row_data))
        left_minutes.append(left)

    return left_minutes

if __name__ == "__main__":

    try:
        src = getsrc()
    except ConnectionError:
        print("Connection Error!", file=sys.stderr)
    except Exception as e:
        print(type(e), " exception had raised.", file=sys.stderr)

    left_minutes = get_next_bus_time(src)
    print(left_minutes)
