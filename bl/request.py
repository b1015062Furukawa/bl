import requests, urllib

def _to_urlencode(string):
    return urllib.parse.quote(string, encoding='Shift-JIS')

def _build_search02php_url(stopname_f, stopname_t):
    stopname_f = _to_urlencode(stopname_f)
    stopname_t = _to_urlencode(stopname_t)
    url = "".join(["http://www.hakobus.jp/search02.php?stopname_f=", stopname_f, "&stopname_t=", stopname_t ])
    return url

def _build_result_url(stopid_f, stopid_t):
    url = "http://www.hakobus.jp/result.php?in=" + str(stopid_f) + "&out=" + str(stopid_t)
    return url

def search02_html(stopname_f, stopname_t):

    # for escape traffic
    txt = ""
    with open('main.html', 'r', encoding='shift_jis') as fp:
        txt = fp.read()
    return txt

    res = None
    try:
        url = _build_search02php_url(stopname_f, stopname_t)
        res = requests.get(url)
    except requests.ConnectionError as e:
        print(e.strerror)
    res.encoding = res.apparent_encoding
    return res.text

def result_html(stopid_f, stopid_t):

    # for escape traffic
    txt = ""
    with open('result.html', 'r', encoding='shift_jis') as fp:
        txt = fp.read()
    return txt

    res = None
    try:
        url = _build_result_url(stopid_f, stopid_t)
        res = requests.get(url)
    except requests.ConnectionError as e:
        print(e.strerror)
    res.encoding = res.apparent_encoding

    return res.text



if __name__ == "__main__":
    result_html(155, 165)
