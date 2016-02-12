import requests, sys, re, argparse
from station_dict import get_station_dict
from bs4 import BeautifulSoup as bs
from option import Option

def parse_args():
    parser = argparse.ArgumentParser()
    f_help =    """
                set entraining point. default: fun
                """
    parser.add_argument("-f", help=f_help, default="fun")

    t_help =    """
                set destination point. default: tomioka
                """
    parser.add_argument("-t", help=t_help, default="tomioka")
    parser.add_argument("--list", help="list up station names", action="store_true")

    args = parser.parse_args()
    return args

def convert_name_to_number(name):
    station_dict = get_station_dict()

    ret = ""
    try:
        ret = station_dict.get(name)
    except:
        print(name + " is not existed in dict", file=sys.stderr)
        sys.exit(1)

    return ret

def get_option():
    args = parse_args()
    option = Option()
    option.f = convert_name_to_number(args.f)
    option.t = convert_name_to_number(args.t)

    # not implemented
    if args.list:
        option.list = args.list
    option.a = False


    return option

def getsrc(option):
    r = requests.get("http://www.hakobus.jp/result.php?in={0}&out={1}".format(option.f, option.t))
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

def main():
    option = get_option()

    if option.list:
        dct = get_station_dict()
        for key in dct.keys():
            print(key)
        sys.exit(0)

    try:
        src = getsrc(option)
    except ConnectionError:
        print("Connection Error!", file=sys.stderr)
    except Exception as e:
        print(type(e), " exception had raised.", file=sys.stderr)

    left_minutes = get_next_bus_time(src)
    for minute in left_minutes:
        print(minute)

if __name__ == "__main__":
    main()
