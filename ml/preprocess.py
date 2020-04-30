from os import listdir, fsencode, fsdecode, path
from .stemming.run_stemmer import run_stemmer
from nltk.tokenize import RegexpTokenizer
from collections import Counter
import pickle

RAW_PATH = path.dirname(path.realpath(__file__)) + '/data/raw/'
PREPROCESSED_PATH = path.dirname(path.realpath(__file__)) + '/data/preprocessed/'

def load_data(containing, dirpath=RAW_PATH):
    if containing == 'times':
        begin, inside = [], []
        for file in listdir(fsencode(dirpath)):
            if containing in fsdecode(file):
                file_begin, file_inside = load_times_set(RAW_PATH + fsdecode(file))
                begin += file_begin
                inside += file_inside
        return stem(begin), stem(inside)

    words = []
    for file in listdir(fsencode(dirpath)):
        if containing in fsdecode(file):
            words += load_set(RAW_PATH + fsdecode(file))
    return stem(words)

def stem(words):
    step = 300
    words = [ words[i*step:min(i*step+step, len(words))] for i in range(len(words) // step + 1)]
    stemmed_chunks = [run_stemmer(chunk) for chunk in words]
    result = []
    for chunk in stemmed_chunks:
        result += chunk
    return result

def load_set(filepath):
    with open(filepath) as f:
        text = f.read()
        tokenizer = RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(text.lower())
        return words
    return None

def load_times_set(filepath):
    with open(filepath) as f:
        lines = f.readlines()
        tokenizer = RegexpTokenizer(r'\w+')
        words = list(map(lambda x: tokenizer.tokenize(x.lower()), lines))
        begin = [line[0] for line in words]
        inside = []
        for line in words:
            for word in line[1:]:
                inside.append(word)
    return begin, inside

def filter_keys(dictt):
    pops = []
    for key in dictt:
        if any(char.isdigit() for char in key):
            pops.append(key)

    for key in pops:
        dictt.pop(key)

if __name__ == "__main__":
    
    print('Loading times...')
    begin, inside = load_data('times')
    begin_dict = Counter(begin)
    begin_dict = dict(begin_dict)
    filter_keys(begin_dict)

    inside_dict = Counter(inside)
    inside_dict = dict(inside_dict)
    filter_keys(inside_dict)

    print('Writing begin...')
    with open(PREPROCESSED_PATH + 'begin.pkl', 'wb') as f:
        pickle.dump(begin_dict, f, pickle.HIGHEST_PROTOCOL)

    print('Writing insides...')
    with open(PREPROCESSED_PATH + 'inside.pkl', 'wb') as f:
        pickle.dump(inside_dict, f, pickle.HIGHEST_PROTOCOL)


    print('Loading other...')
    other = load_data('other')
    other_dict = Counter(other)
    other_dict = dict(other_dict)
    filter_keys(other_dict)
    
    print('Writing other...')
    with open(PREPROCESSED_PATH + 'other.pkl', 'wb') as f:
        pickle.dump(other_dict, f, pickle.HIGHEST_PROTOCOL)
    print('Done')
