import counter_stats
import lemmatizer
import pager
import sys

if len(sys.argv) > 2:
    MIN_RECOGNITION_PERCENT = float(sys.argv[2])
else:
    MIN_RECOGNITION_PERCENT = 0.95

BOOK = sys.argv[1]
with open(BOOK, encoding='utf-8') as infile:
    text = pager.tokens(infile.read())
unique = set(text)

lemma_counts = lemmatizer.examine(BOOK)
with open(BOOK, encoding='utf-8') as infile:
    text = pager.tokens(infile.read())

print(len(text), 'words,', len(unique), 'unique forms,', len(lemma_counts), 'lemmas')
counter_stats.full_table(lemma_counts)

table = counter_stats.cumulative_table(lemma_counts)

with open('words.txt', encoding='utf-8') as infile:
    known = set(pager.tokens(infile.read()))

coverage = sum(p for w,_,p,_ in table if w in known)
count = sum(1 for l in lemma_counts.keys() if l in known)
print(count, 'known words provide {:.3f} already'.format(coverage))
last_count = table[0][1]
for w,c,p,_ in table:
    if coverage > MIN_RECOGNITION_PERCENT:
        break
    if w in known:
        continue
    if c < last_count:
        last_count = c
        print('({})'.format(c))
    print(w)
    coverage += p
