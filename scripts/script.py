import pager
import stem_word

BOOK, LIMIT = 'huge.txt', 65000000

with open(BOOK, encoding='utf-8') as infile:
    text = pager.tokens(infile.read())

word_appearance_order = dict()
for i, word in enumerate(text):
    if word not in word_appearance_order:
        word_appearance_order[word] = i

ordered_words = pager.word_frequency(text)
frequency_order = [(c, word_appearance_order[w], w) for w, c, in ordered_words.most_common()]
frequency_order = sorted(frequency_order, reverse=True, key=lambda t: (t[0], -t[1], t[2]))

retrieved = 0
for i, word_count in enumerate(frequency_order):
    count, index, word = word_count
    if stem_word.cached_stems(word) is not None:
        continue
    else:
        retrieved += 1
    try:
        print('{} pos:{} count:{} {}->{}'.format(i, index, count, word, stem_word.stems(word)))
    except TypeError:
        print('only retrieved', retrieved, 'words')
        break
    if retrieved > LIMIT:
        print('more to go, come back tomorrow ({} of {})'.format(i, len(ordered_words)))
        break
