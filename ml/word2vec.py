import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

from stemming.run_stemmer import run_stemmer
from nltk.tokenize import RegexpTokenizer

import os
import random
from tqdm import tqdm

VOCABULARY_PATH = os.path.dirname(os.path.realpath(__file__)) + '/data/vocabulary/vocabulary.txt'
CORPUS_PATH = os.path.dirname(os.path.realpath(__file__)) + '/data/raw/'

BATCH_SIZE = 512
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Running on {DEVICE}')

class NNClassifier(nn.Module):
    def __init__(self):
        super(NNClassifier, self).__init__()

        self.conv = nn.Sequential(
            nn.Conv1d(300, 512, kernel_size=3)
        )


    def forward(x):
        y = self.conv(x)
        print(y.shape)




class Word2Vec(nn.Module):
    def __init__(self, n_words):
        super(Word2Vec, self).__init__()

        self.embeddings = nn.Linear(n_words, 300)
        self.output = nn.Sequential(
            nn.Linear(300, n_words),
            nn.Softmax(dim=1)
        )

        self.loss = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.parameters(), lr=0.01)
    
    def forward(self, x):
        y = self.reprs(x)
        y = self.output(y)
        return y

    def train(self, generator, epochs):
        for epoch in range(epochs):
            print(f'Epoch: {epoch}')
            
            for batch in tqdm(range(generator.words_len // BATCH_SIZE)):
                batch_x, batch_y = generator.get_pairs(BATCH_SIZE)
                batch_x = batch_x.to(DEVICE)
                batch_y = batch_y.to(DEVICE)
                self.optimizer.zero_grad()

                outputs = self(batch_x)
                loss = self.loss(outputs, batch_y)
                loss.backward()
                self.optimizer.step()

class PairGenerator:
    def __init__(self, text, vocabulary, window_size = 1):
        tokenizer = RegexpTokenizer(r'\w+')
        self.words = tokenizer.tokenize(text.lower())
        self.words = run_stemmer(self.words)
        self.words = list(map(lambda word: voc_index(word, vocabulary), self.words))
        self.words = [word for word in self.words if word is not None]
        self.words_len = len(self.words)
        self.window_size = window_size
        self.voc_size = len(vocabulary)
        self.index = 0

    def get_pairs(self, count):
        self.index = 0 if (self.index + count) >= self.words_len else self.index 
        xs = list(map(lambda x: one_hot(x, self.voc_size), self.words[self.index:self.index+count]))
        ys = []
        for index in range(self.index, self.index + count):
            low = max(0, index % self.words_len - self.window_size)
            high = min(self.words_len - 1, index % self.words_len + self.window_size)
            y = random.choice(self.words[low:high])
            ys.append(y)
        self.index += count
        return torch.tensor(xs, dtype=torch.float), torch.tensor(ys, dtype=torch.long)

def load_vocabulary(path):
    vocabulary = []
    with open(path, 'r') as f:
        vocabulary = f.readlines()
        vocabulary = list(map(lambda x: x.strip(), vocabulary))
    return vocabulary


''' Returns a numpy array '''
def voc_index(stem, vocabulary):
    try:
        index = vocabulary.index(stem)
        return index
    except:
        return

def one_hot(index, length):
    result = [0 for _ in range(length)]
    result[index] = 1
    return result

def load_training_corpus(dirpath):
    other = ''
    times = ''
    for file in os.listdir(os.fsdecode(dirpath)):
        filepath = dirpath + os.fsdecode(file)
        if not filepath.endswith('.txt'):
            continue
        with open(filepath, 'r') as f:
            if 'times' in os.fsdecode(file):
                times += ' ' + f.read()
            else:
                other += ' ' + f.read()

    return times + other


print('Loading vocabulary...')
voc = load_vocabulary(VOCABULARY_PATH)

print('Loading training corpus...')
text = load_training_corpus(CORPUS_PATH)

pairGenerator = PairGenerator(text, vocabulary=voc, window_size=5)

print('Creating network...')
net = Word2Vec(len(voc)).to(DEVICE)

print('Training....')
#net.train(pairGenerator, 10)
print('Done!')

embeddings = net.embeddings

classifier = NNClassifier()

index = voc.index(run_stemmer(['luna']))
x = embeddings[index]
print(x.shape)

classifier.forward()
