import spacy
import os

nlp=spacy.load('en_core_web_sm')

txt="howdy partner, I want a scotch on the rocks and make it fast."

exampleDoc=nlp( (txt) ) #text has to be encapsulated?

print( [token.text for token in exampleDoc] )

#now for file stuff
cwd=os.getcwd()
filename='first.txt'

exFileTxt=open(cwd+'/'+filename).read()
exDoc=nlp(exFileTxt)

print([token.text for token in exDoc]) 


#now for sentence detection
txt=(
    'if a chunk of text is sperated '  #note, need space at end of chiunk or start in order to work
    'into multiple chuinks of text, '
    'they can be put into a single encapsulator. '
    'this will cause the nlp constructor to automatically parse it together. '
    'however, the chunks have to be in order in the encapsulation. '
)
exDoc=nlp(txt)
sentences=list(exDoc.sents) #get sentences as a list of each sentence
for s in sentences:
    print(s)

## check out all the attributes tokens have
for token in exDoc:
    print(f'\ntoken: {token}\ttoken.idx: {token.idx}\ttoekn.text_with_ws: {token.text_with_ws}')
    print(f'token.is_alpha: {token.is_alpha}\ttoken.is_punct: {token.is_punct}\ttoken.is_space: {token.is_space}')
    print(f'token.shape: {token.shape}\ttoken.is_stop: {token.is_stop}\n')