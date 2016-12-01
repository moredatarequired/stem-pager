import word_family as wf
import pager
import sys
import textblob as tb

source_file = sys.argv[1]
with open(source_file) as infile:
    text = tb.TextBlob(infile.read())

for sentence in text.sentences:
    print(sentence)
    lemmas = []
    for word in sentence.words:
        word = pager.clean_text(word)
        lemma = wf.manual_lemma(word)
        if lemma is not None:
            lemmas.append(lemma)
            continue
        group = wf.word_matches(word)
        question = '{} -> ? {}: '.format(word, wf.format_group(group))
        answer = input(question)
        if not answer:
            lemma = group.most_common(1)[0][0]
        elif answer.isdigit():
            i = int(answer) - 1
            lemma = group.most_common()[i][0]
        else:
            lemma = answer
        wf.add_lemma(word, lemma)
        lemmas.append(lemma)
    print(sentence)
    print(' ==>', ' '.join(lemmas))
    print()
