from ml.preprocess_acc import COMBS
from ml.bayes import BayesClassifier, load_pickle
import os
from nltk.tokenize import RegexpTokenizer
from regexs.redefs import timex_matched
from tqdm import tqdm


TEST_PATH = os.path.dirname(os.path.realpath(__file__)) + '/ml/data/test/'
RAW_PATH =  os.path.dirname(os.path.realpath(__file__)) + '/ml/data/raw/'

tokenizer = RegexpTokenizer(r'\w+')

def flatten(lst):
    flat_list = []
    for sublist in lst:
        for item in sublist:
            flat_list.append(item)
    return flat_list

print('This will take a while...')

true_positives = 0
false_positives = 0
false_negatives = 0
for comb in tqdm(COMBS):
    with open(RAW_PATH + f'{comb[0]}times_art{comb[1:]}.txt') as f:
        text = f.read()
        matched, notMatched = timex_matched(text)
        matched = [tokenizer.tokenize(el) for el in matched]
        flat_list = []
        for sublist in matched:
            for item in sublist:
                flat_list.append(item)
        matched = flat_list
        notMatched = tokenizer.tokenize(notMatched)
        true_positives += len(matched)
        false_negatives += len(notMatched)
        
    with open(RAW_PATH + f'{comb[0]}other_art{comb[1:]}.txt') as f:
            text = f.read()
            matched, notMatched = timex_matched(text)
            matched = [tokenizer.tokenize(el) for el in matched]
            flat_list = []
            for sublist in matched:
                for item in sublist:
                    flat_list.append(item)
            matched = flat_list
            false_positives += len(matched)

print(f'Stats for regex module:')
print(f'Precision: {true_positives / (true_positives + false_positives)}')
print(f'Recall: {true_positives / (true_positives + false_negatives)}')

true_positives = 0
false_positives = 0
false_negatives = 0

for comb in tqdm(COMBS):
    bayes = BayesClassifier(time_set=load_pickle(TEST_PATH + f'times{comb}.pkl'), other_set=load_pickle(TEST_PATH + f'other{comb}.pkl'))
    with open(RAW_PATH + f'{comb[0]}times_art{comb[1:]}.txt') as f:
        text = f.read()
        bayes_output = bayes.run_on_text(text)
        tp = [txt for (b, txt) in bayes_output if b]
        fn = [txt for (b, txt) in bayes_output if not b]
        tp = [tokenizer.tokenize(expr) for expr in tp]
        tp = flatten(tp)

        fn = [tokenizer.tokenize(expr) for expr in fn]
        fn = flatten(fn)
        true_positives += len(tp)
        false_negatives += len(fn)

        
    with open(RAW_PATH + f'{comb[0]}other_art{comb[1:]}.txt') as f:
            text = f.read()
            bayes_output = bayes.run_on_text(text)
            fp = [txt for (b, txt) in bayes_output if b]
           
            fp = [tokenizer.tokenize(expr) for expr in fp]
            fp = flatten(fp)

            false_positives += len(fp)


print(f'Stats for bayes module:')
print(f'Precision: {true_positives / (true_positives + false_positives)}')
print(f'Recall: {true_positives / (true_positives + false_negatives)}')



