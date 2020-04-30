import os
from nltk.tokenize import RegexpTokenizer
from pickle import load
from .preprocess import stem

RAW_PATH = os.path.dirname(os.path.realpath(__file__)) + '/data/raw/'
PREPROCESSED_PATH = os.path.dirname(os.path.realpath(__file__)) + '/data/preprocessed/'

def load_pickle(path):
    with open(path, 'rb') as f:
        return load(f)
        

class BayesClassifier:
    def __init__(self, begin_set=load_pickle(PREPROCESSED_PATH + 'begin.pkl'), inside_set=load_pickle(PREPROCESSED_PATH + 'inside.pkl'), outside_set=load_pickle(PREPROCESSED_PATH + 'other.pkl')):
        self.begin_set = begin_set
        self.inside_set = inside_set
        self.outside_set = outside_set

        self.begin_count = sum(self.begin_set.values())
        self.inside_count = sum(self.inside_set.values())
        self.outside_count = sum(self.outside_set.values())
        self.all_count = self.begin_count + self.inside_count + self.outside_count

        self.p_begin = self.begin_count / self.all_count
        self.p_inside = self.inside_count / self.all_count
        self.p_outside = self.outside_count / self.all_count

    def run_on_text(self, text):
        tokenizer = RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(text.lower())
        return self.run(words)

    ''' Text should be a list of words (eg. ['după', 'câteva', 'luni']) without any spaces or punctuation. Use misc_utils.preprocess to preprocess the text'''
    def run(self, words):
        if len(words) == 0:
            return []

        stemmed_words = stem(words)
        bool_mask = [self.classify(word) for word in (stemmed_words)]
        
        result = []
        partial = ''
        last_bool = bool_mask[0]
        for i, el in enumerate(bool_mask):
            if el == last_bool:
                partial += ' ' + words[i]
            else:
                result.append( (last_bool, partial) ) 
                last_bool = el
                partial = words[i] 

        result.append( (last_bool, partial) )
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

        begin_count_word = 0
        try:
            begin_count_word = self.begin_set[word]
        except:
            pass

        inside_count_word = 0
        try:
            inside_count_word = self.inside_set[word]
        except:
            pass

        outside_count_word = 0
        try:
            outside_count_word = self.outside_set[word]
        except:
            pass

        p_word_wr_begin = (begin_count_word + z) * upscale / (self.begin_count + 2 * z)
        p_begin_wr_word = p_word_wr_begin * (self.p_begin * upscale)

        p_word_wr_inside = (inside_count_word + z) * upscale / (self.inside_count + 2 * z)
        p_inside_wr_word = p_word_wr_inside * (self.p_inside * upscale)

        p_word_wr_outside = (outside_count_word + z) * upscale / (self.outside_count + 2 * z)
        p_outside_wr_word = p_word_wr_outside * (self.p_outside * upscale)

        return p_inside_wr_word >= p_outside_wr_word or p_begin_wr_word >= p_outside_wr_word