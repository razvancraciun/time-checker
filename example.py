from ml.bayes import BayesClassifier
from ml.preprocess import load_data
from os import path
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')

RAW_PATH = path.dirname(path.realpath(__file__)) + '/ml/data/raw/'

print('Reading file...')
text = ''
text = load_data('time', RAW_PATH)

print(text)

print('Creating classifier...')
bc = BayesClassifier()

print('Running...')
result = bc.run_on_text(' '.join(text))

found = 0
total = 0
for (is_time, expr) in result:
    words = tokenizer.tokenize(expr)
    if (is_time):
        found += len(words)
    total += len(words)

print(result)

print(found, total, found/total)

print('---------------------------')