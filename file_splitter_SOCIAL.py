import re
import sys

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

def visible(element):
    # This will grab comments that beautiful soup misses
    re_comment = re.compile(ur'.*<!--.*', re.DOTALL)

    if re.match(re_comment, element) or repr(type(element)) == "<class 'bs4.element.Comment'>":
        return False
       # print element
    elif element.parent.name in ['meta', 'style', 'script', '[document]', 'head', 'title']:
        return False

    return True


def replace_all_weird_chars(sentence):
    to_replace = {chr(0) : '' , chr(1) : '', chr(8) : '', chr(11) : ''}
    for i, j in to_replace.iteritems():
        sentence = sentence.replace(i, j)

    return sentence

p = re.compile(ur'([0-9]{10})-([a-zA-Z0-9]{32})')
regex = re.compile('(?<=[.!?\n\r]) +', re.DOTALL|re.M)

# TODO: Split on punctuation?

with open(sys.argv[1]) as f:
    content = f.readlines()

all_sentences = "".join(content)

# The document will look roughly like this:

# <Header Stuff> (Useless)
# social
#     text text text
# text/plain
#     text text text
#
# lingpipe
# lingpipe
#
# <Trec stuff> 
# .
# .
# lingpipe
# <Header Stuff>
# .
# .
# (Repeating)

# We will split on the lingpipe and grab:

# <Header Stuff> (Useless)
# social
#     text text text
# text/plain
#     text text text

# and 

# <Trec stuff> 
# .
# .
#

# and

# .
# (Repeating)

# So we will split on text/plain to just get the text text text This should work for multiple levels because lingpipe will be
# the bottom of each individual document, and we can just take what's between it and text/plain (Which should be good)

documents = re.split("lingpipe", all_sentences)[:-1]



time_stamps_doc_ids = re.findall(p, all_sentences)

time_stamps_doc_ids = ['{0}-{1}'.format(thing[0], thing[1]) for thing in time_stamps_doc_ids]

documents = [document for document in documents if len(replace_all_weird_chars(document)) > 0]

print 

documents = documents[::2]

current_idx = 0

for document in documents:
    list_of_sentences = []
    string_of_sentences = ""

    # We have to do extra work here in order to get the correct amount of text
    # We want to part after 'text.plain'
    html = re.split('text/plain', document)[1]

    soup = BeautifulSoup(html)

    texts = soup.findAll(text=True)

    visible_texts = filter(visible, texts)

    sentence_idx = 0
    with open('filtered_documents/' + time_stamps_doc_ids[current_idx] + '.txt', 'w') as writer:
        for thing in visible_texts:
            if len(thing.string.replace('\n', '').strip(' ').split(' ')) < 3:
                continue

            writer.write('{0} {1} {2}\n'.format(sentence_idx, time_stamps_doc_ids[current_idx], thing.string.encode('utf-8').strip('\n')))
            sentence_idx += 1

    current_idx += 1
        
        