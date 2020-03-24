import string

#DEPREACATED use nltk.word_tokenize instead
def preprocess(text):
        print('DEPREACATED use nltk.word_tokenize instead')
        result = []
        text = text.strip().split()
        text = [word for word in text if not word.isspace()]
        for word in text:
            modded = word.replace('_', ' ')
            modded = ''.join(list(filter(lambda x: x not in ['.', ',', '!', '?', '(', ')', '"', ';', '/'], modded)))
            modded = modded.strip()
            modded = modded.lower()
            if not modded.isspace():
                result.append(modded)
        return result