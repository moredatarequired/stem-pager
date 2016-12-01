from collections import Counter, defaultdict
from nltk.stem.snowball import SpanishStemmer
import pager

stemmer = SpanishStemmer()

stem_counts = Counter()
stem_sources = defaultdict(Counter)
with open('escow14ax.freq10.l.tsv', encoding='utf-8') as infile:
    for line in infile:
        if len(stem_counts) == 15000:
            break
        parts = line.split('\t')
        count, lemma = int(parts[0]), parts[6].strip()
        clean = pager.clean_text(lemma)
        if len(clean) == len(lemma):
            stem = stemmer.stem(clean)
            stem_counts[stem] += count
            stem_sources[stem][clean] += count

with open('stem_to_lemma.txt', 'w', encoding='utf-8') as outfile:
    for stem, count in stem_counts.most_common():
        lemma_list = [(l, c / count) for l, c in stem_sources[stem].most_common() if c > 0.02 * count]
        lemma_format = ' '.join('{}*{:.2f}'.format(l, f) for l, f in lemma_list)
        outfile.write('{} : {}\n'.format(stem, lemma_format))
