from ml.bayes import BayesClassifier

from nltk.tokenize import RegexpTokenizer

text = ''
with open('example.txt', 'r') as f:
    text = f.read()

tokenizer = RegexpTokenizer(r'\w+')
words = tokenizer.tokenize(text.lower())

bc = BayesClassifier()

print('Unbiased run...')
result = bc.run(words)
print(result)

print('---------------------------')