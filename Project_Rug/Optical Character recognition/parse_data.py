import sys
from nltk.tag import pos_tag
f = open(sys.argv[1], "r")
file_read = f.read()
all_text = file_read.split('\n')

for sentence in all_text:
    tagged_sent = pos_tag(sentence.split())
    # [('Michael', 'NNP'), ('Jackson', 'NNP'), ('likes', 'VBZ'), ('to', 'TO'), ('eat', 'VB'), ('at', 'IN'), ('McDonalds', 'NNP')]
    # propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
    print(tagged_sent)

