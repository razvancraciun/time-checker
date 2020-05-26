import os
import re
from .custom_tokenize import custom_tokenize
# from nltk.tokenize import RegexpTokenizer
from pickle import load
from .preprocess import stem

RAW_PATH = os.path.dirname(os.path.realpath(__file__)) + '/data/raw/'
PREPROCESSED_PATH = os.path.dirname(os.path.realpath(__file__)) + '/data/preprocessed/'

def load_pickle(path):
    with open(path, 'rb') as f:
        return load(f)
        

class BayesClassifier:
    def __init__(self, time_set=load_pickle(PREPROCESSED_PATH + 'times.pkl'), other_set=load_pickle(PREPROCESSED_PATH + 'other.pkl')):
        self.time_set = time_set
        self.other_set = other_set
        self.time_count = sum(self.time_set.values())
        self.other_count = sum(self.other_set.values())
        self.p_time = self.time_count / (self.time_count + self.other_count)
        self.p_other = self.other_count / (self.time_count + self.other_count)


    def run_on_text(self, text):
        result = []
        tokens = list(custom_tokenize(text))
        for (is_words, expr) in tokens:
            if is_words:
                tokens = re.split(r'\s+', expr)
                is_temp_exprs = [self.classify(word) for word in stem(tokens)]
                for ii in range(len(tokens)):
                    result += [(is_temp_exprs[ii], tokens[ii])]
            else:
                if len(result) > 0:
                    result[-1] = (result[-1][0], result[-1][1] + expr)

        final = [result[0]]
        for ii in range(1, len(result)):
            if final[-1][0] != result[ii][0]:
                final += [result[ii]]
            else:
                space = '' if final[-1][1].endswith('-') or final[-1][1].endswith(' ') else ' '
                final[-1] = (final[-1][0], final[-1][1] + space + result[ii][1])

        return final

    ''' True if word is part of timex, False otherwids '''
    def classify(self, word):
        try:
            int(word)
            return True
        except:
            pass
        upscale = 1e5
        z = 2

        time_count_word = 0
        try:
            time_count_word = self.time_set[word]
        except:
            pass

        other_count_word = 0
        try:
            other_count_word = self.other_set[word]
        except:
            pass

        p_word_wr_time = (time_count_word + z) * upscale / (self.time_count + 2 * z)
        p_time_wr_word = p_word_wr_time * (self.p_time * upscale)

        p_word_wr_other = (other_count_word + z) * upscale / (self.other_count + 2 * z)
        p_other_wr_word = p_word_wr_other * (self.p_other * upscale)

        return p_time_wr_word * 5 >= p_other_wr_word