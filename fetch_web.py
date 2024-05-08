import requests
from bs4 import BeautifulSoup
import sys

def fetch_from_web(url, fname):

    html_raw = requests.get(url).content

    soup = BeautifulSoup(html_raw, 'html.parser')
    text = soup.find_all(text=True)

    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'style'
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    f = open(fname, "w")

    for char in output:
        try:
            f.write(char)
        except:
            continue

    f.close()

    return output