import re

def custom_tokenize(text):
    start = 0
    while start < len(text):
        match = re.search(r'^\w+(\s+\w+)*', text[start:])
        if match:
            start += len(match.group(0))
            yield (True, match.group(0))

        match = re.search(r'^\W+', text[start:])
        if match:
            start += len(match.group(0))
            yield (False, match.group(0))