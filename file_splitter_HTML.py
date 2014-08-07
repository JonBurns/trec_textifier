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

p = re.compile(ur'([0-9]{10})-([a-zA-Z0-9]{32})')
p_test = re.compile(ur'([a-zA-Z0-9]{32})')
regex = re.compile('(?<=[.!?\n\r]) +', re.DOTALL|re.M)

# TODO: Split on punctuation?

with open(sys.argv[1]) as f:
    content = f.readlines()

# Should be of form folder/
destination = sys.argv[2]

all_sentences = "".join(content)

documents = re.split(p, all_sentences)[:-1]

documents = documents[::3]

time_stamps_doc_ids = re.findall(p, all_sentences)

time_stamps_doc_ids = ['{0}-{1}'.format(thing[0], thing[1]) for thing in time_stamps_doc_ids]

current_idx = 0

for document in documents:
    list_of_sentences = []
    string_of_sentences = ""

    html = re.split('lingpipe', document)[0]
    start_pos = html.find('<!DOCTYPE')


    html = html[start_pos:]

    soup = BeautifulSoup(html)


    texts = soup.findAll(text=True)

    visible_texts = filter(visible, texts)



    sentence_idx = 0
    with open(destination + time_stamps_doc_ids[current_idx] + '.txt', 'w') as writer:
        for thing in visible_texts:
            if len(thing.string.replace('\n', '').strip(' ').split(' ')) < 3:
                continue

            writer.write('{0} {1} {2}\n'.format(sentence_idx, time_stamps_doc_ids[current_idx], thing.string.encode('utf-8').strip('\n')))
            sentence_idx += 1
    current_idx += 1
        
        
