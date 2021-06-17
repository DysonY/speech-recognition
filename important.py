from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from wordfreq import word_frequency


# TODO make more efficient
def lemmatize(lemmatizer, words):
    tags = ['A', 'R', 'N', 'V']
    lemmas = []
    for word, tag in pos_tag(words):
        if tag[0] in tags:
            lemma = lemmatizer.lemmatize(word, tag[0].lower())
            lemmas.append(lemma)
        else:
            lemmas.append(word)
    return lemmas


def code_of(language):
    langs = { 'English' : 'en',
              'German' : 'de' }
    return langs[language]


# Return list of most important words
def most_important(word_str, lang):
    words = word_str.split(' ')
    length = len(words)
    lemmatizer = WordNetLemmatizer()
    language = code_of(lang)

    # Get local and global frequencies
    # TODO make lfreqs more efficient 
    # can be done in 2 passses; O(n^2) -> O(n)
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
    test1 = ['3D', 'printing', 'or', 'additive', 'manufacturing', 'is', 'the', 'construction', 'of', 'a', 'three-dimensional', 'object', 'from', 'a', 'cat', 'model', 'or', 'digital', '3D', 'model', 'it', "'s", 'Heavy', 'D', 'printing', 'can', 'refer', 'to', 'a', 'variety', 'of', 'processes', 'which', 'material', 'is', 'deposited', 'join', 'or', 'solidified', 'Under', 'Computer', 'control', 'to', 'create', 'a', 'three-dimensional', 'object', 'with', 'material', 'being', 'added', 'together', 'such', 'as', 'Plastics', 'liquid', 'or', 'powdered', 'greens', 'being', 'fused', 'together', 'typically', 'layer-by-layer'] 
    print(most_important(test1))

