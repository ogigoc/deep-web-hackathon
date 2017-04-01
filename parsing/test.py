import requests
import sys
from .parser import parse_html

def parse_test(url):
    proxies = {
        'http': 'http://10.120.194.45:8123'
    }

    r = requests.get(url, proxies=proxies)
    if r.status_code != 200:
        print("Error, status code is {0}".format(r.status_code))
        return

    print("Result:")
    print(parse_html(r.text))

if len(sys.argv) < 2:
    print("Usage: {0} url".format(sys.argv[0]))
else:
    parse_test(sys.argv[1])
