# def run_on_text(self, text):
#     result = []
#     tokens = list(custom_tokenize(text))
#     for (is_word, token) in tokens:
#         if is_word:
#             is_temporal_expr = self.classify(stem([token])[0])
#             result += [(is_temporal_expr, token)]
#         else:
#             result += [(False, token)]
#     return result


# def run_on_text(self, text):
#     tokenizer = RegexpTokenizer(r'\w+')
#     words = tokenizer.tokenize(text.lower())
#     return self.run(words)

# ''' Text should be a list of words (eg. ['după', 'câteva', 'luni']) without any spaces or punctuation. Use misc_utils.preprocess to preprocess the text'''
# def run(self, words):
#     if len(words) == 0:
#         return []

#     stemmed_words = stem(words)
#     bool_mask = [self.classify(word) for word in (stemmed_words)]
	
# 	# self.classify(stem([word])[0])

#     result = []
#     partial = ''
#     last_bool = bool_mask[0]
#     for i, el in enumerate(bool_mask):
#         if el == last_bool:
#             partial += ' ' + words[i]
#         else:
#             result.append( (last_bool, partial) ) 
#             last_bool = el
#             partial = words[i] 

#     result.append( (last_bool, partial) )
#     return result