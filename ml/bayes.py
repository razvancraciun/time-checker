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
                tokens = re.split('\s+', expr)
                is_temporal_expr = self.classify(stem(tokens)[0])
                result += [(is_temporal_expr, ' '.join(tokens))]
            else:
                result += [(False, expr)]
        return result


    # def run_on_text(self, text):
    #     result = []
    #     tokens = list(custom_tokenize(text))
    #     for (is_word, token) in tokens:
    #         if is_word:
    #             is_temporal_expr = self.classify(stem([token])[0])
    #             result += [(is_temporal_expr, token)]
    #         else:
    #             result += [(False, token)]
    #     return result


    # def run_on_text(self, text):
    #     tokenizer = RegexpTokenizer(r'\w+')
    #     words = tokenizer.tokenize(text.lower())
    #     return self.run(words)

    # ''' Text should be a list of words (eg. ['după', 'câteva', 'luni']) without any spaces or punctuation. Use misc_utils.preprocess to preprocess the text'''
    # def run(self, words):
    #     if len(words) == 0:
    #         return []

    #     stemmed_words = stem(words)
    #     bool_mask = [self.classify(word) for word in (stemmed_words)]
        
    # 	# self.classify(stem([word])[0])

    #     result = []
    #     partial = ''
    #     last_bool = bool_mask[0]
    #     for i, el in enumerate(bool_mask):
    #         if el == last_bool:
    #             partial += ' ' + words[i]
    #         else:
    #             result.append( (last_bool, partial) ) 
    #             last_bool = el
    #             partial = words[i] 

    #     result.append( (last_bool, partial) )
    #     return result
    

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

        return p_time_wr_word >= p_other_wr_word