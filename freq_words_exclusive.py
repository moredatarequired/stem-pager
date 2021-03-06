from collections import Counter
import counter_stats
import sys

COUNT = float(sys.argv[2])

with open('words.txt') as infile:
    known = set(infile.read().split('\n'))

lemma_file = sys.argv[1]
if not lemma_file.endswith('.frequency'):
    print('Please use frequency file instead')
    sys.exit()
print(lemma_file)
lemmas = Counter()
order = dict()
with open(lemma_file) as infile:
    for i, line in enumerate(infile):
        parts = line.split('\t')
        if len(parts) != 3:
            continue
        count, lemma, sentence = parts
        lemmas[lemma] += int(count)
        order[lemma] = i

req_file = sys.argv[3]
if not req_file.endswith('.frequency'):
    print('Please use frequency file instead')
    sys.exit()
choices = set()
sentences = dict()
with open(req_file) as infile:
    for i, line in enumerate(infile):
        parts = line.split('\t')
        if len(parts) != 3:
            continue
        count, lemma, sentence = parts
        choices.add(lemma)
        sentences[lemma] = sentence

counter_stats.full_table(lemmas)

table = counter_stats.cumulative_table(lemmas)

coverage = sum(p for w,_,p,_ in table if w in known)
count = sum(1 for l in lemmas.keys() if l in known)
print(count, 'known words provide {:.3f} already'.format(coverage))
last_count, number = table[0][1], 0
add = []
for w,c,p,_ in table:
    if len(add) > COUNT:
        break
    if w in known:
        continue
    if w not in choices:
        continue
    if c < last_count:
        if number:
            print('({}), +{}'.format(last_count, number))
        last_count = c
        number = 0
    add.append(w)
    number += 1
    coverage += p
if number:
    print('({}), +{}'.format(last_count, number))

if add:
    print(len(add))
    for w in add:
        print(w)

    answer = input('Add these words? ')
    if answer and answer.lower()[0] == 'y':
        with open('words.txt', 'a') as outfile:
            for lemma in add:
                outfile.write('{}\n'.format(lemma))
