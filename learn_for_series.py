from collections import Counter
import counter_stats
import lemmatizer
import pager
import sys

num_new_words = int(sys.argv[1])

files = [
    'texts/el principito.txt',
    'texts/avatar1.txt',
    'texts/Paulo Coelho - El Alquimista.txt',
    'texts/C. S. Lewis - Las Crónicas de Narnia 1 - El León, la Bruja y el Ropero.txt',
    'texts/como agua para chocolate.txt',
    'texts/J.K. Rowling - Harry Potter 1 - La Piedra Filosofal.txt',
    'texts/100years.txt',
]

aggregate_counts = Counter()
for f in files:
    aggregate_counts.update(counter_stats.normalize_counter(lemmatizer.examine(f)))

table = counter_stats.cumulative_table(aggregate_counts)

known = set(pager.tokens_from_file('words.txt'))
coverage = sum(p for w,_,p,_ in table if w in known)
count = sum(1 for l in aggregate_counts.keys() if l in known)
print(count, 'known words provide {:.3f} already'.format(coverage))

unknown_counter = Counter()
for word, count in aggregate_counts.items():
    if word in known:
        unknown_counter['--known--'] += count
    else:
        unknown_counter[word] += count
benchmarks = [0.90 + i / 100 for i in range(10)]
print(counter_stats.short_table_header(benchmarks))
print(counter_stats.short_table(unknown_counter, benchmarks))

words_shown = 0
for w,c,p,_ in table:
    if words_shown > num_new_words:
        break
    if w in known:
        continue
    print(w)
    words_shown += 1
    coverage += p

print('coverage would increase to', coverage)
