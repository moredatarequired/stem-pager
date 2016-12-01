from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers

with open('ebook_ids.txt') as infile:
    ebook_ids = [int(n) for n in infile.read().split()]

for ebook in ebook_ids:
    text = strip_headers(load_etext(ebook)).strip()
    with open(str(ebook), 'w') as outfile:
        outfile.write(text)
