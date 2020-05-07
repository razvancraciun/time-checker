from os import path
import pickle
import torch
import torch.nn as nn

PREPROCESSED_PATH = path.dirname(path.realpath(__file__)) + '/data/preprocessed/'

class NN(nn.Module):
    def __init__(self):
        pass




with open(PREPROCESSED_PATH + 'vec.pkl', 'rb') as f:
        data = pickle.load(f)
        print(data['adsafas'])
        print( (data['rege'] - data['bărbat'] + data['femeie']))

