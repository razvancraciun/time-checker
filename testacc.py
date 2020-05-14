from ml.preprocess_acc import COMBS
from ml.bayes import BayesClassifier, load_pickle
import os
from nltk.tokenize import RegexpTokenizer
from regex.redefs import timex_matched
from tqdm import tqdm


TEST_PATH = os.path.dirname(os.path.realpath(__file__)) + '/ml/data/test/'
RAW_PATH =  os.path.dirname(os.path.realpath(__file__)) + '/ml/data/raw/'

tokenizer = RegexpTokenizer(r'\w+')

total = 0
found = 0
for comb in tqdm(COMBS):
    bayes = BayesClassifier(time_set=load_pickle(TEST_PATH + f'times{comb}.pkl'), other_set=load_pickle(TEST_PATH + f'other{comb}.pkl'))
    with open(RAW_PATH + f'{comb[0]}times_art{comb[1:]}.txt') as f:
        text = f.read()
        total += len(text)
        result = bayes.run_on_text(text)
        for b, el in result:
            if b:
                found += sum([len(expr) for expr in timex_matched(el)])
print(found / total)
# 0.3748708186021213