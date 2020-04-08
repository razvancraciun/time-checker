import subprocess


def run_stemmer(word_list):
    result = subprocess.run(['php', 'run_stemmer.php', *word_list], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8') 