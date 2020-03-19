from ml.misc_utils import preprocess
from ml.bayes import BayesClassifier


text = '''La 4 iulie 2019, Arjen Robben a ales să se retragă din fotbalul profesionist la doar 35 de ani, el spunând că aceasta a fost o decizie dificilă. Ultimul său meci a fost în luna mai a anului 2019 după câteva luni în care a stat pe bancă din cauza unei accidentări.'''

text = preprocess(text)
bc = BayesClassifier()
result = bc.run(text)
result_biased = bc.run_biased(text)
print(result)
print(result_biased)