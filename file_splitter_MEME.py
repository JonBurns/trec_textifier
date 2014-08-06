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

# Compile our needed regex
# Each document ID/timestamp is 10 digits (For time, In UNIX) followed by a dash and then a 32 character document ID
p = re.compile(ur'([0-9]{10})-([a-zA-Z0-9]{32})')

with open(sys.argv[1]) as f:
    content = f.readlines()

all_sentences = "".join(content)

# MEMETRACKER only contains one document per file. Therefore we don't need to split on the document id's

# We do need the document Id, however
time_stamps_doc_ids = re.findall(p, all_sentences)




# First we will split on 'lingpipe' which seperates the original document from the extra trec information
html_with_header = re.split("lingpipe", all_sentences)

# We only need the top half of the document
html_with_header= html_with_header[0]

file_name = '{0}-{1}'.format(time_stamps_doc_ids[0][0], time_stamps_doc_ids[0][1])

# The header information, which we don't need, is held behind the MEMETRACKER tag. So we will split on it and 
# Throw out the header information
html = re.split("MEMETRACKER", html_with_header)[1]

# Soup the html for deliciousness 
soup = BeautifulSoup(html)

# This code will get all of the text that was visible on a webpage. Stored in a list. 
texts = soup.findAll(text=True)
visible_texts = filter(visible, texts)

# We need to keep track of each sentences index for the TREC submission
sentence_idx = 0



with open('filtered_documents/' + file_name + '.txt', 'w') as writer:
    # Iterate through the good sentences we've found
    for text in visible_texts:

        # Discard any small sentences. This is due to the sad fact that our filter will let some things slip through
        if len(text.encode('utf-8').strip(' ').split(' ')) < 2:
            continue

        temp_text = text
        # Web formatting makes me sad :(
        while '  ' in temp_text:
            temp_text = temp_text.replace('  ', ' ')
        
        # We need to output in this format for TREC submission    
        writer.write('{0} {1} {2}\n'.format(sentence_idx, file_name, temp_text.encode('utf-8').strip().replace('\t', '').replace('\n', '').replace('\r', '')))
        sentence_idx += 1
        