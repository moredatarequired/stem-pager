import sys
from textblob import TextBlob

lemma_file = sys.argv[1]
if not lemma_file.endswith('.lemmas'):
    print('Please use lemma file.')
    sys.exit()

new_words = int(sys.argv[2])

with open('words.txt') as infile:
    known = set(infile.read().split('\n'))

original = lemma_file[:-7]

with open(original) as infile:
    text = infile.read().replace('\n', ' ').replace('\t', ' ')
    sentences = TextBlob(text).sentences

sentences_read = 0
def sentence_with(word):
    global sentences_read
    for i, s in enumerate(sentences):
        if word in s:
            if i > sentences_read:
                sentences_read = i
            return s

seen = set()
with open(lemma_file) as infile:
    for line in infile:
        parts = line.split()
        if len(parts) != 3:
            continue
        word, lemma, pos = parts
        if pos.strip() in ('PUNCT', 'NUM', 'UNKNOWN', 'X'):
            continue
        lemma = lemma.lower()
        if lemma in known or lemma in seen:
            continue
        seen.add(lemma)
        print('{:12} "{}"'.format(lemma, sentence_with(word)))
        new_words -= 1
        if new_words <= 0:
            break

print('Read {}/{} sentences ({:.2f}%)'.format(
    sentences_read, len(sentences), sentences_read * 100 / len(sentences)))

answer = input('Add these sentences? ')
if answer and answer.lower()[0] == 'y':
    with open('words.txt', 'a') as outfile:
        for lemma in seen:
            outfile.write('{}\n'.format(lemma))
