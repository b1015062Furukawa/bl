import sys
import request
import re
import datetime
from bs4 import BeautifulSoup

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

# I can't find good name...
def convert_2_to_time(string):
    hour_minute = string.split(':')
    return datetime.time(hour=int(hour_minute[0]), minute=int(hour_minute[1]))

def is_low_floor(string):
    if 'ノンステップ' in string:
        return True
    return False

# I can't find good name...
def convert_8_to_time(string):
    if 'まもなく' in string:
        return datetime.date()

    tmp = re.sub("\D", "", string)
    if tmp == "":
        return None
    else:
        return datetime.time(minute=int(tmp))

def get_access_information(stopid_f, stopid_t):
    # 運行情報
    """与えられた駅IDからバスの停車予定時刻を得る

    結果はバスロケーションのサイトの接近情報ページに依存
    Args:
        stopid_f: 乗車駅名
        stopid_t: 降車駅名

    Returns:
        残り待ち時間でソートされた辞書の配列を返します
        [
            {"time": "<datetime.time Object>",
            "bus_type": "105系統（未来大経由）etc.",
            "destination": "赤川 etc.",
            "low_floor": False,
            "real_left_time": "<datetime.time Object>" # if まもなく it will be datetime.time(0)
            },
            {"time": "<datetime.time Object>",
            "bus_type": "105系統（未来大経由）etc.",
            "destination": "赤川 etc.",
            "low_floor": False,
            "real_left_time": "<datetime.time Object>"
            },
            ...
        ]
    """
    ret = []
    html = request.result_html(stopid_f=stopid_f, stopid_t=stopid_t)
    soup = BeautifulSoup(html, 'html.parser')

    the_table = soup.find('table', width="800", border="0")
    first_skipped = False
    for tr in the_table.find_all('tr'):

        if not first_skipped:
            first_skipped = True
            continue

        td_cnt = 0
        the_dict = {}
        for td in tr.find_all('td'):
            td_cnt += 1
            td_content = td.text.strip()

            if td_cnt == 2:
                the_dict["time"] = convert_2_to_time(td_content)
            if td_cnt == 3:
                the_dict["bus_type"] = td_content
            if td_cnt == 5:
                the_dict["description"] = td_content
            if td_cnt == 7:
                the_dict["low_floor"] = is_low_floor(td_content)
            if td_cnt == 8:
                the_dict["real_left_time"] = convert_8_to_time(td_content)
        ret.append(the_dict)

    return ret

def get_suggested_station_dict(stopname):
    """与えられた駅名から予想される駅の一覧を返す。

    結果はバスロケーションのサイトの停留所検索のページに依存
    Args:
        stopname: 乗車駅名

    Returns:
    [
        {"stopname": "stopname0", "id": "00"},
        {"stopname": "stopname1", "id": "01"},
        ...
    ]
    """

    html = request.search02_html(stopname, "dummy")
    soup = BeautifulSoup(html, 'html.parser')
    ret = []
    for in_select in soup.find_all('select', id='in'):
        for option in in_select.find_all('option'):
            a_dict = {}
            a_dict["stopname"] = option.text
            a_dict["id"] = option.get('value', 0)
            ret.append(a_dict)

    return ret

def get_matched_station_dict(stopname_f, stopname_t):
    """与えられた駅名から予想される駅の一覧を返す。

    結果はバスロケーションのサイトの停留所検索のページに依存
    Args:
        stopname_f: 乗車駅名
        stopname_t: 降車駅名

    Returns:
        {
            "stopname_f":
                [
                    {"stopname": "stopname0", "id": "00"},
                    {"stopname": "stopname1", "id": "01"},
                    ...
                ],
            "stopname_t":
                [
                    {"stopname": "stopname0", "id": "00"},
                    {"stopname": "stopname1", "id": "01"},
                    ...
                ]
        }
    """

    html = request.search02_html(stopname_f, stopname_t)
    soup = BeautifulSoup(html, 'html.parser')
    ret = {
        stopname_f: [],
        stopname_t: []
    }
    for in_select in soup.find_all('select', id='in'):
        for option in in_select.find_all('option'):
            stopname = option.text
            stopid = option.get('value', 0)
            ret[stopname_f].append({"stopname": stopname, "id": stopid})

    for out_select in soup.find_all('select', id='out'):
        for option in out_select.find_all('option'):
            stopname = option.text
            stopid = option.get('value', 0)
            ret[stopname_t].append({"stopname": stopname, "id": stopid})

    return ret

if __name__ == "__main__":
    stopname_f = "亀田"
    stopname_t = "未来"
    ret = get_suggested_station_dict('亀田')
    print(ret)
