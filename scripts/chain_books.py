from collections import Counter
import counter_stats
import lemmatizer
import sys

cutoff = 0.95
context = 10

previous_lemmas = Counter()

for filename in sys.argv[1:]:
    lemma_counts = lemmatizer.examine(filename)
    table = counter_stats.cumulative_table(lemma_counts)
    index = counter_stats.at_percentile(table, cutoff)[0]
    print(filename)
    print('\tneeds', index, 'lemmas for', cutoff, 'coverage')
    coverage = sum(p for w,_,p,_ in table if previous_lemmas[w] >= context)
    count = sum(1 for l in lemma_counts.keys() if previous_lemmas[l] >= context)
    print('\tprevious work provides {:.3f}'.format(coverage), 'coverage with', count, 'lemmas')
    learn_from_context = 0
    for w, c, p, _ in table:
        old_count = previous_lemmas[w]
        previous_lemmas[w] += c
        if previous_lemmas[w] >= context > old_count:
            if not learn_from_context:
                print(w)
            learn_from_context += 1
            coverage += p
    print('\t', learn_from_context, 'words are learnable from context, increasing comprehension to {:.3f}'.format(coverage))
    new_lemmas_count = 0
    for w,_,p,_ in table:
        if coverage > cutoff:
            break
        if previous_lemmas[w] < context:
            new_lemmas_count += 1
            previous_lemmas[w] = context
            coverage += p
    print('\t', new_lemmas_count, 'were required to get to', cutoff)

total = sum(1 for _, c in previous_lemmas.most_common() if c >= context)
print(total, 'lemmas acquired')
