import os
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup
import html

ROOT_DATA = os.path.dirname(os.path.realpath(__file__)) + '/data/'

TAGS = ['TIMEX', 'TIMEX3']

def extract_timex():
    timexs = []
    for file in os.listdir(os.fsencode(ROOT_DATA)):
        if os.fsdecode(file).endswith('.xml'):
            timexs += timex_element_from_file(os.path.join(ROOT_DATA, os.fsdecode(file)))
    return timexs


def timex_element_from_file(filepath):
    with open(filepath, 'r') as file:
        text = file.read()
        text = html.unescape(text)
        tree = et.fromstring(text)
        timexs = []
        for tag in TAGS:
            timexs += tree.findall(f'.//{tag}')
        return timexs


### EXAMPLE USAGE

# timexs = extract_timex()
# for time in timexs:
#     print(time.text)