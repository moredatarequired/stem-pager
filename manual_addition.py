import lemmatizer
from textblob import TextBlob
import sys

review_file = sys.argv[1]
with open(review_file) as infile:
    text = TextBlob(infile.read())

for sentence in text.sentences:
    print('reviewing "{}"'.format(sentence.replace('\n', ' ')))
    lemmas = []
    for word in sentence.words:
        word = word.lower()
        lemma = lemmatizer.get_lemma(word)
        if lemma is not None:
            lemmas.append(lemma)
            continue
        guess = lemmatizer.guess_lemma(word)
        answer = input('{} -> {}? '.format(word, guess))
        if not answer:
            lemmatizer.add_lemma(guess)
            lemmas.append(guess)
        elif answer == '-':
            lemmatizer.add_skip('-')
            lemmas.append('-')
        else:
            lemmatizer.add_form(answer, word)
