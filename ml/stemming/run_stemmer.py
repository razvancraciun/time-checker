import subprocess


def run_stemmer(word_list):
    result = subprocess.run(['php', 'run_stemmer.php', *word_list], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8').strip().splitlines()
    return result 