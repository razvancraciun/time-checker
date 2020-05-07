from ml.bayes import BayesClassifier


print('Reading file...')
text = ''
with open('example.txt', 'r') as f:
    text = f.read()

print('Creating classifier...')
bc = BayesClassifier()

print('Running...')
result = bc.run_on_text(text)
print(result)

print('---------------------------')