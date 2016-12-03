from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
import os.path
import sys
from textblob import TextBlob


def analyze_syntax(text):
    """Use the NL API to analyze the given text string, and returns the
    response from the API.  Requests an encodingType that matches
    the encoding used natively by Python.  Raises an
    errors.HTTPError if there is a connection problem.
    """
    credentials = GoogleCredentials.get_application_default()
    scoped_credentials = credentials.create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    scoped_credentials.authorize(http)
    service = discovery.build(
        'language', 'v1beta1', http=http)
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'language': 'ES',
            'content': text,
        },
        'features': {
            'extract_syntax': True,
        },
        'encodingType': get_native_encoding_type(),
    }
    request = service.documents().annotateText(body=body)
    return request.execute()


def get_native_encoding_type():
    """Returns the encoding type that matches Python's native strings."""
    if sys.maxunicode == 65535:
        return 'UTF16'
    else:
        return 'UTF32'

def paginate(text):
    max_tokens = 25000
    text = TextBlob(text)
    sentences = text.sentences
    word_per_sentence = len(text.words) / len(sentences)
    sentences_per_page = int(max_tokens / word_per_sentence)
    for i in range(0, len(sentences), sentences_per_page):
        yield ' '.join(str(s) for s in sentences[i:i + sentences_per_page])

for filename in sys.argv[1:]:
    lemma_file = filename + '.lemmas'
    if os.path.isfile(lemma_file):
        print('Lemma file already exists for:', filename)
        continue
    print('Retrieving lemmas for:', filename)

    with open(filename) as infile:
        text = infile.read()

    lemma_triplets = []
    for i, page in enumerate(paginate(text)):
        for token in analyze_syntax(page)['tokens']:
            lemma_triplets.append(
                (token['text']['content'], token['lemma'], token['partOfSpeech']['tag']))
        print('finished page', i)

    with open(lemma_file, 'w') as outfile:
        for word, lemma, pos in lemma_triplets:
            outfile.write('{}\t{}\t{}\n'.format(word, lemma, pos))
