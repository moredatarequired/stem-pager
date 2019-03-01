from object_size import total_size
from collections import Counter, defaultdict
import random
from textblob import TextBlob

with open('texts/hp1-7.txt') as infile:
  text = TextBlob(infile.read())

table = defaultdict(Counter)
key = []
for word in text.words:
  word = word.lower()
  table[tuple(key)][word] += 1
  key = key[-2:] + [word]

print('Size of table:', total_size(table) / 1000000, 'MB')
