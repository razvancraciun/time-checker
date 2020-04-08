import subprocess
import os

DATA_PATH = os.path.dirname(os.path.realpath(__file__))

def run_stemmer(word_list):
    result = subprocess.run(['php', f'{DATA_PATH}/run.php', *word_list], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8').strip().splitlines()
    return result 