import os
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup
import html
from copy import deepcopy
import string


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
    
    def preprocess(text):
        result = ''
        for word in text:
            modded = word.replace('_', ' ')
            modded = ''.join(list(filter(lambda x: x not in ['.', ',', '!', '?'], modded)))
            modded = modded.strip()
            modded = modded.lower()
            result += (modded + '\n') if modded != '' else ''
        return result

    time_text = preprocess(time_exp)
    other_text = preprocess(other_exp)

    with open(DATA_PATH + 'TIMES_RAW.txt', 'w') as f:
        f.write(time_text)
    
    with open(DATA_PATH + 'OTHER_RAW.txt', 'w') as f:
        f.write(other_text)


corpus_to_class_files()