from os import listdir, fsencode, fsdecode, path
from .stemming.run_stemmer import run_stemmer
from nltk.tokenize import RegexpTokenizer
from collections import Counter
import pickle

RAW_PATH = path.dirname(path.realpath(__file__)) + '/data/raw/'
PREPROCESSED_PATH = path.dirname(path.realpath(__file__)) + '/data/test/'
COMBS = ['c' + str(i) for i in range(1,41)] + ['t' + str(i) for i in range(1,41)]

def load_data(containing, butnot, dirpath=RAW_PATH):
    owner = butnot[0]
    nr = butnot[1:]
    words = []
    for file in listdir(fsencode(dirpath)):
        fnr = ''.join([i for i in fsdecode(file) if i.isdigit()])
        if containing in fsdecode(file) and (fsdecode(file)[0] != owner or nr != fnr):
            words += load_set(RAW_PATH + fsdecode(file))
    result = stem(words)
    return result

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

def filter_keys(dictt):
    pops = []
    for key in dictt:
        if any(char.isdigit() for char in key):
            pops.append(key)

    for key in pops:
        dictt.pop(key)

if __name__ == "__main__":
    
    
    for comb in COMBS:
        print(comb)
        times = load_data('times', butnot=comb)
        times_dict = Counter(times)
        times_dict = dict(times_dict)
        filter_keys(times_dict)

        with open(PREPROCESSED_PATH + f'times{comb}.pkl', 'wb') as f:
            pickle.dump(times_dict, f, pickle.HIGHEST_PROTOCOL)


        other = load_data('other', butnot=comb)
        other_dict = Counter(other)
        other_dict = dict(other_dict)
        filter_keys(other_dict)


        with open(PREPROCESSED_PATH + f'other{comb}.pkl', 'wb') as f:
            pickle.dump(other_dict, f, pickle.HIGHEST_PROTOCOL)

