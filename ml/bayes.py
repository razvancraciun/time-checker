import os
import time
from .stemming.run_stemmer import run_stemmer
from nltk.tokenize import RegexpTokenizer


RAW_PATH = os.path.dirname(os.path.realpath(__file__)) + '/data/raw/'


def load_data(containing, dirpath=RAW_PATH):
    words = []
    for file in os.listdir(os.fsencode(dirpath)):
        if containing in os.fsdecode(file):
            words += load_set(RAW_PATH + os.fsdecode(file))
    return run_stemmer(words)

def load_set(filepath):
    with open(filepath) as f:
        text = f.read()
        tokenizer = RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(text.lower())
        return words
    return None

class BayesClassifier:
    def __init__(self, time_set=load_data(containing='times'), other_set=load_data(containing='other')):
        self.time_set = time_set
        self.other_set = other_set
        self.time_count = len(time_set)
        self.other_count = len(other_set)
        self.p_time = self.time_count / (self.time_count + self.other_count)
        self.p_other = self.other_count / (self.time_count + self.other_count)

    ''' Text should be a list of words (eg. ['după', 'câteva', 'luni']) without any spaces or punctuation. Use misc_utils.preprocess to preprocess the text'''
    def run(self, text):
        start = time.time()
        result = []
        last_word_index = None
        stemmed_text = run_stemmer(text)
        for index in range(len(text)):
            word = text[index]
            if self.classify(stemmed_text[index]):
                if last_word_index == None or index != last_word_index + 1:
                    result.append(word)
                    last_word_index = index
                else:
                    result[-1] += ' ' + word
                    last_word_index = index
        print(f'Origin: {len(text)} words. Result: {len(result)} words')
        print(f'Duration {round(time.time() - start, 3)} seconds')
        return result
    

    ''' True if word is part of timex, False otherwids '''
    def classify(self, word):
        try:
            int(word)
            return True
        except:
            pass
        upscale = 1e5
        z = 2
        p_word_wr_time = (self.time_set.count(word) + z) * upscale / (self.time_count + 2 * z)
        p_time_wr_word = p_word_wr_time * (self.p_time * upscale)

        p_word_wr_other = (self.other_set.count(word) + z) * upscale / (self.other_count + 2 * z)
        p_other_wr_word = p_word_wr_other * (self.p_other * upscale)

        return p_time_wr_word >= p_other_wr_word

    ''' Text should be a list of words (eg. ['după', 'câteva', 'luni']) without any spaces or punctuation. Use misc_utils.preprocess to preprocess the text'''
    def run_biased(self, text):
        start = time.time()
        result = []
        last_word_index = None
        for index in range(len(text)):
            word = text[index]
            if self.classify_biased(word):
                if last_word_index == None or index != last_word_index + 1:
                    result.append(word)
                    last_word_index = index
                else:
                    result[-1] += ' ' + word
                    last_word_index = index
        print(f'Origin: {len(text)} words. Result: {len(result)} words')
        print(f'Duration {round(time.time() - start, 3)} seconds')
        return result
    

    ''' True if word is part of timex, False otherwids '''
    def classify_biased(self, word):
        try:
            int(word)
            return True
        except:
            pass
        upscale = 1e5

        p_word_wr_time = self.time_set.count(word) * upscale / self.time_count
        p_time_wr_word = p_word_wr_time * (self.p_time * upscale)

        p_word_wr_other = self.other_set.count(word) * upscale / self.other_count
        p_other_wr_word = p_word_wr_other * (self.p_other * upscale)

        return p_time_wr_word >= p_other_wr_word