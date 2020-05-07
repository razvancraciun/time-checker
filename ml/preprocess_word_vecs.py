import io
from os import path
import pickle
import string
import numpy as np

WORD_VEC_PATH = path.dirname(path.realpath(__file__)) + '/data/model/cc.ro.300.vec'
PREPROCESSED_PATH = path.dirname(path.realpath(__file__)) + '/data/preprocessed/'

def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    i = 0
    for line in fin:
        i += 1
        tokens = line.rstrip().split(' ')
        if any( [( c in string.punctuation or c.isnumeric() or c.isupper() ) for c in tokens[0] ] ):
            continue
        data[tokens[0]] = np.asarray(list(map(float, tokens[1:])))
    return data

data = load_vectors(WORD_VEC_PATH)
print(len(data))

print('Writing...')
with open(PREPROCESSED_PATH + 'vec.pkl', 'wb') as f:
    pickle.dump(data, f)