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
        for tag in TAGS:
            timexs += tree.findall(f'.//{tag}')
        
        timexs = list(map(lambda ex: deepcopy(ex), timexs))
        timex_text = [' '.join(timex.itertext()) for timex in timexs]
        time_words = []
        for text in timex_text:
            for word in text.split():
                time_words.append(word)

        return (time_words, notimexs)

def corpus_to_class_files():
    (time_words, other_words) = extract_data()
    print(time_words)
    print(len(time_words))


corpus_to_class_files()





### EXAMPLE USAGE

# timexs = extract_timex()
# for time in timexs:
#     print(time.text)