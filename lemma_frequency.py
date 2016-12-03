from collections import Counter, defaultdict
import sys
from textblob import TextBlob

for filename in sys.argv[1:]:
    if not filename.endswith('.lemmas'):
        print(filename, 'is not a lemma file.')
        continue
    print('Getting frequencies for', filename)

    lemma_counts = Counter()
    lemma_words = defaultdict(Counter)
    lemma_appearance = dict()
    with open(filename) as infile:
        for i, line in enumerate(infile):
            parts = line.split('\t')
            if len(parts) != 3:
                continue
            word, lemma, pos = parts
            if pos.strip() in ('PUNCT', 'NUM', 'UNKNOWN', 'X'):
                continue
            lemma = lemma.lower()
            lemma_counts[lemma] += 1
            lemma_words[lemma][word.lower()] += 1
            if lemma not in lemma_appearance:
                lemma_appearance[lemma] = i

    with open(filename[:-7]) as original:
        sentences = TextBlob(original.read()).sentences
    sentence_index = dict()
    for s in sentences:
        for w in s.words:
            w = w.lower()
            if w not in sentence_index or len(sentence_index[w]) > len(s):
                sentence_index[w] = s.replace('\n', ' ')

    sorted_lemmas = sorted(lemma_counts.items(),
                           key=lambda lc:(-lc[1], lemma_appearance[lc[0]]))

    with open(filename[:-7] + '.frequency', 'w') as outfile:
        for lemma, count in sorted_lemmas:
            example = sentence_index.get(lemma_words[lemma].most_common(1)[0][0], '')
            outfile.write('{}\t{}\t"{}"\n'.format(count, lemma, example))
