from collections import Counter

lemma_file = 'texts/100years.txt.lemmas'

words = Counter()

with open(lemma_file) as infile:
    for line in infile:
        word, lemma, pos = line.split('\t')
        if pos.strip() in ('PUNCT', 'NUM', 'UNKNOWN', 'X'):
            continue
        words[word.lower()] += 1


def minimal_pair(word1, word2):
    if len(word1) != len(word2):
        return None
    difference = None
    for l, r in zip(word1, word2):
        if l != r:
            if difference:
                return None
            else:
                difference = (l, r)
    return difference


word_list = words.most_common(100)

for i, word_freq1 in enumerate(word_list):
    word1, freq1 = word_freq1
    for word_freq2 in word_list[i+1:]:
        word2, freq2 = word_freq2
        mp = minimal_pair(word1, word2)
        if mp is None:
            continue
        value = freq1 * freq2
        print(word1, word2, mp, value)
