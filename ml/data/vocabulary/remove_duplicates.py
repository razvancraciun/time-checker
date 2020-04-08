import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

words = []
with open(f'{DIR_PATH}/voc_w_dupes.txt', 'r') as f:
    words = f.readlines()
    words = set(map(lambda x: x.strip(), words))
    words = list(words)
    words.sort()
    
with open(f'{DIR_PATH}/vocabulary.txt', 'w') as f:
    for word in words:
        f.write(word + '\n')