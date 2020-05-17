import sys
import spacy
from collections import defaultdict
#f = open(sys.argv[1], "r")
#file_read = f.read()
#all_text = file_read.split('\n')
def NLP(all_text):
    all_text = all_text.split('\n')
    nlp = spacy.load("en_core_web_sm")
    ner = defaultdict(list)
    for sentence in all_text:
        doc = nlp(sentence)
        doc_l = nlp(sentence.lower())
        
        if doc.ents:
            for ent in doc.ents:
                #print(ent.text, ent.start_char, ent.end_char, ent.label_)
                ner[ent.label_].append(ent.text)
        elif doc_l.ents:
            doc = doc_l
            for ent in doc.ents:
                #print(ent.text, ent.start_char, ent.end_char, ent.label_)
                ner[ent.label_].append(ent.text)
        else:
            for token in doc:
                #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
                ner[token.pos_].append(token.text)
    return ner