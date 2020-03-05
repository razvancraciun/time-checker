import os
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup
import html
from copy import deepcopy

CORPUS_PATH = os.path.dirname(os.path.realpath(__file__)) + '/data/corpus/'
DATA_PATH = os.path.dirname(os.path.realpath(__file__)) + '/data/'


TAGS = ['TIMEX', 'TIMEX3']

def extract_data():
    """ Returns a tuple of type (list of time related words, list words unrelated to time expressions) """
    timexs = []
    notimexs = []
    for file in os.listdir(os.fsencode(CORPUS_PATH)):
        if os.fsdecode(file).endswith('.xml'):
            (file_timexs, file_notimexs) = words_from_file(os.path.join(CORPUS_PATH, os.fsdecode(file)))
            timexs += file_timexs
            notimexs += file_notimexs
    return (timexs, notimexs)


def words_from_file(filepath):
    with open(filepath, 'r') as file:
        text = file.read()
        text = html.unescape(text)
        tree = et.fromstring(text)
        timexs = []
        notimexs = []
        textNode = tree.findall(f'.//TEXT')[0]
        for tag in TAGS:
            timexs += tree.findall(f'.//{tag}')
        
        timexs = list(map(lambda ex: deepcopy(ex), timexs))

        for tag in TAGS:
            parents = tree.findall(f'.//{tag}/..')
            for parent in parents:
                for timex in timexs:
                    try:
                        parent.remove(timex)
                    except:
                        pass              
        timexs = [timex for timex in timexs if timex]
        notimexs = [notimex for notimex in notimexs if notimex]  
        return (timexs, notimexs)

def corpus_to_class_files():
    (timexs, notimexs) = extract_data()
    print(len(timexs))
    timex_text = [''.join(timex.itertext()) for timex in timexs]
    timex_text = [text for text in timex_text if text != '']
    timex_text = '\n'.join(timex_text)


    with open(DATA_PATH + 'TIMEXS_RAW.txt', 'w') as f:
        f.write(timex_text)


corpus_to_class_files()





### EXAMPLE USAGE

# timexs = extract_timex()
# for time in timexs:
#     print(time.text)