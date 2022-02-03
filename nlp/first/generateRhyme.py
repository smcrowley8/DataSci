import eng_to_ipa as phon
import spacy
import nltk
import os

#level is how good rhyme should be (bigger is better)
#syllables?
def generate_rhymes(inp, level): 
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
            rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
    return set(rhymes)

print(generate_rhymes('howdy', 3)) 