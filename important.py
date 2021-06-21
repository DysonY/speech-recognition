import sys
from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer
from wordfreq import word_frequency


# Perform lemmatization
def lemmatize(lemmatizer, words):
    tags = ['A', 'R', 'N', 'V']
    lemmas = []
    for word, tag in pos_tag(words):
        if len(word) > sys.maxsize:
            continue
        if tag[0] in tags:
            lemma = lemmatizer.lemmatize(word, tag[0].lower())
            lemmas.append(lemma)
        else:
            lemmas.append(word)
    return lemmas


# Get language code
def code_of(language):
    langs = { 'English' : 'en',
              'German' : 'de' }
    return langs[language]


# Return list of most important words
def most_important(word_str, lang):
    #words = word_str.split() 
    words = nltk.word_tokenize(word_str)
    length = len(words)
    lemmatizer = WordNetLemmatizer()
    language = code_of(lang)

    # Get local and global frequencies
    words = lemmatize(lemmatizer, words)
    lfreqs = [ words.count(word) / length for word in words ]
    gfreqs = [ word_frequency(word, language) for word in words ]

    # Map words to ratios of frequencies
    ratios = [ l/g for (l,g) in zip(lfreqs, gfreqs) if g != 0 ]
    mappings = [ (a,b) for (a,b) in zip(words, ratios) ]

    # Remove duplicates
    mappings = list(set(mappings))

    # Sort using ratios as keys
    mappings.sort(reverse = True, key = lambda x : x[1])
    return [ word for word,freq in mappings if freq > 1000]


if __name__ == '__main__':
    lemmatizer = WordNetLemmatizer()
    words = ['antidisestablishmentarianism',
             'pneumonoultramicrosopicsilicovolcanocoiniosis',
             'Donaudampfschiffahrtsgesellschaftskapitän']
    print(lemmatize(lemmatizer, words))
