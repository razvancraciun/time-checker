import os
import time

TIME_PATH = os.path.dirname(os.path.realpath(__file__)) + '/data/TIMES_RAW.txt'
OTHER_PATH = os.path.dirname(os.path.realpath(__file__)) + '/data/OTHER_RAW.txt'

def load_set(filepath):
    with open(filepath) as f:
        lines = f.read().splitlines()
        words = []
        for line in lines:
            if line != '\n':
                words += [word for word in line.split() if not word.isspace()]
        return words
    return None

class BayesClassifier:
    def __init__(self, time_set=load_set(TIME_PATH), other_set=load_set(OTHER_PATH)):
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
        for word in text:
            if self.classify(word):
                result.append(word)
        print(f'Origin: {len(text)} words. Result: {len(result)} words')
        print(f'Duration {round(time.time() - start, 3)} seconds')
        return result
    

    ''' True if word is part of timex, False otherwids '''
    def classify(self, word):
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
        for word in text:
            if self.classify_biased(word):
                result.append(word)
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

        return p_time_wr_word * 1.01 >= p_other_wr_word