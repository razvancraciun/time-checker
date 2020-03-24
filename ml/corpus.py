import os
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup
import html
from copy import deepcopy
import string
from misc_utils import preprocess

DATA_PATH = os.path.dirname(os.path.realpath(__file__)) + '/data/'

CORPUS_PATH = DATA_PATH + 'corpus/'
RAW_PATH = DATA_PATH + 'raw/'


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
        for tag in TAGS:
            timexs += tree.findall(f'.//{tag}')
        timex_text = [' '.join(timex.itertext()) for timex in timexs]
        time_exp = []
        for text in timex_text:
            time_exp.append(text)
        
        textNode = tree.find('.//TEXT')
        for tag in TAGS:
            parents = textNode.findall(f'.//{tag}/..')
            for parent in parents:
                for timex in timexs:
                    try:
                        parent.remove(timex)
                    except:
                        pass
        
        notime_exp = []
        for text in textNode.itertext():
            notime_exp.append(text)

        return (time_exp, notime_exp)

def corpus_to_class_files():
    (time_exp, other_exp) = extract_data()
    
    time_text = '\n'.join([' '.join(preprocess(exp)) for exp in time_exp])
    other_text = '\n'.join([' '.join(preprocess(exp)) for exp in other_exp])

    time_text = '\n'.join([line for line in time_text.splitlines() if line != '\n' ])
    other_text = '\n'.join([line for line in other_text.splitlines() if line != '\n' ])

    with open(RAW_PATH + 'TIMES_RAW.txt', 'w') as f:
        f.write(time_text)
    
    with open(RAW_PATH + 'OTHER_RAW.txt', 'w') as f:
        f.write(other_text)


corpus_to_class_files()