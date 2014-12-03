import re, collections

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(from_dict):
    model = collections.defaultdict(lambda: 1)
    for f in from_dict:
        model[f] += 1
    return model

WORDS_COUNT = train(words(file('dictionary.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def check(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def check_again(word):
    return set(e2 for e1 in check(word) for e2 in check(e1) if e2 in WORDS_COUNT)

def known(words):
    return set(w for w in words if w in WORDS_COUNT)

def correct(word):
    candidates = known([word]) or known(check(word)) or check_again(word) or [word]
    #the word that appears more time in WORDS_COUNT
    return max(candidates, key = WORDS_COUNT.get)

def correction(keystring):
    keystring = keystring.strip()
    words = keystring.split(" ")
    correction = []
    for word in words:
        correction.append(correct(word))
    corrected = " ".join(correction)
    return corrected
