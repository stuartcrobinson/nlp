import fileinput
import re

from pattern.en import parse, comparative, superlative, pluralize, conjugate
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.tokenize import word_tokenize

wnl = WordNetLemmatizer()

posChar = '▓'


#
# 1.  split corpus at spaces and punct:
# https://stackoverflow.com/questions/1059559/split-strings-with-multiple-delimiters
# https://stackoverflow.com/a/16840963/8870055
# https://stackoverflow.com/questions/17245123/getting-adjective-from-an-adverb-in-nltk-or-other-nlp-library


# TODO what if not found?
def getAdjectiveRoot(superlativeOrComparative):
    return wnl.lemmatize(superlativeOrComparative, 'a')


def isGerund(word):
    return pos_tag(word_tokenize(word))[0][1] == 'VBG'


def getGerundRoot(gerund):
    if gerund == "piping":
        return "pipe"
    return WordNetLemmatizer().lemmatize(gerund, 'v')


def getAdverbRoot(adverb):
    if adverb == 'ceremonially':
        return "ceremonial"
    if adverb == 'intensively':
        return 'intensive'
    if adverb == 'underhandedly':
        return 'underhanded'
    if adverb == 'effectively':
        return 'effective'
    if adverb == 'primarily':
        return 'primary'
    if adverb == 'uncontrollably':
        return 'uncontrollable'
    if adverb == 'palely':
        return 'pale'
    winner = ""
    try:
        wordtoinv = adverb
        s = []
        for ss in wn.synsets(wordtoinv):
            for lemmas in ss.lemmas():  # all possible lemmas.
                s.append(lemmas)
        for pers in s:
            posword = pers.pertainyms()[0].name()
            #             print(posword)
            if posword[0:3] == wordtoinv[0:3]:
                winner = posword
                break
    except IndexError:
        pass
    if winner == '':
        return adverb
    else:
        return winner


'''
failed adverbs:

intensively      intensely
untruly          untruely        (other ue words fit the rule)
underhandedly    underhandly
truly            truely
adjectively      adjectivally        - not words
ceremonially     ceremoniously
futilely         futily
unduly           unduely
shrilly          shrillly
fully            fullly

wryly wrily ---- wry wrily
shyly shily ---- shy shily
adjectively adjectivally ---- adjectival adjectivally
spatially spacially ---- spacial spacially
piping pipping ---- piping pipingly
publicly publically ---- public publically
effectively efficaciously ---- efficacious efficaciously
vilely vily ---- vile vily
agilely agily ---- agile agily
coyly coily ---- coy coily
primarily principally ---- principal principally
uncontrollably uncontrolledly ---- uncontrolled uncontrolledly
aborad aborally ---- aboral aborally
palely pallidly ---- pallid pallidly
wholly wholy ---- whole wholy



'''

m_adjective_adverb_special = {
    'futile': 'futilely',
    'untrue': 'untruly',
    'true': 'truly',
    'undue': 'unduly',
    'wry': 'wryly',
    'shy': 'shyly',
    'spacial': 'spatially',
    'public': 'publicly',
    'vile': 'vilely',
    'agile': 'agilely',
    'coy': 'coyly',
    'aborad': 'aborally',
    'pale': 'palely',
    'whole': 'wholly',
}


def getAdverb(word):
    if word in m_adjective_adverb_special:
        return m_adjective_adverb_special[word]
    if word[-1:] == 'y':  # hasty
        return word[:-1] + 'ily'
    if word[-2:] == 'le':  # probable responsible subtle
        return word[:-1] + 'y'
    if word[-1:] == 'c':  # probable responsible subtle
        return word + 'ally'
    if word[-2:] == 'll':  # probable responsible subtle
        return word + 'y'
    if word[-2:] == 'll':  # probable responsible subtle
        return word + 'y'
    return word + 'ly'


def postParse(patternParsed):
    '''
    if it can be broken, return array of root and POS atoms.  else, return array containing root
    also - return original word w/ no POS for unsupported POSs (like MD for can --> could. cant untokenize)
    '''
    word = patternParsed[0]
    root = patternParsed[5]
    pos = patternParsed[1]
    # print('root: <' + root + '>, pos: <' + pos + '>, patternParsed: <' + str(patternParsed) + '>')
    #
    unsupportedPosSet = set(['MD'])
    # adverb - get root adjective
    #     print(word, root, pos)
    if pos in unsupportedPosSet:
        #         print('yes pos in unspported pos set!')
        root = word.lower()
    elif pos == 'RB':
        root = getAdverbRoot(root)
    #
    # superlatives and comparative - get root adjective
    elif pos == 'JJS' or pos == 'JJR' or pos == 'RBR':
        root = getAdjectiveRoot(root)
    #
    # ends in ing - pattern.en fails to parse swimming and eating.  but works for talking (talk, VBG)
    # TODO start here = fails for piping, stopping, etc
    #     ''' TODO  - can't do this manually :('''
    elif root[-3:] == 'ing' and root == word.lower():
        if isGerund(root):
            root = getGerundRoot(root)
            pos = 'VBG'
    return word, root, posChar + pos


def getBrokenSimple(word):
    #     print('in get broken. word: ', word)
    ''' returns word parsed into array of caps chars, word root, and POS tag if any'''
    if word.isspace():
        return [word]
    returner = []
    patternParsedList = parse(word, relations=True, lemmata=True).split()[0]
    for patternParsed in patternParsedList:
        word, root, pos = postParse(patternParsed)
        print(patternParsed, word, root, pos)
        print()


# 1.  replace ... with █ xxxellipsisxxx █
# 2.  replace █’ █ with █ xxxcasaxxx █   //closing apostrophe space after
# 3.  replace █ ‘█ with █ xxxoasbxxx █      //open apostrophe space before

# 0.  replace ... w ellipsis token
# 1.  replace opening and closing single apostrophes by spaces
# 2.  split by non-word character (not a letter or a number) EXCEPT closing apostrophe (only internal apostrophes should remain)
# 3.  parse each word.  replace word element with array (concat to orig) of capchar, word root, and parsed tag.


# NO NO NO NO NO
# don't use smart quotes :( cos no smart quotes in twitter.  so STUPIDIFY ALL QUOTES

# text = "oh well here we go one, two, won't, can't; but...yeah okay! sounds 'good' to me. just ‘great’ what's \"your\" name? i am tired i went to the store and drank seven juices."

text = "run ran swim swam swum kick kicked kicks hat hats swift swiftness swiftly swifter swiftest taller tallest shorter shortest indifference strength alumnae loving beauty beautiful destroy	destruction	destructive	destructively absurdity	absurd	absurdly amuse amusing expandable miserable comfortable...regional"

text = text \
    .replace('...', ' xxxellipsis ') \
    .replace('”', '"') \
    .replace('“', '"') \
    .replace('‘', '"') \
    .replace('’', '"') \
    .replace("' ", ' xxxasa ') \
    .replace(" '", ' xxxasb ')

# keep apostrophes cos important for word parsing (like "won't"
ar = re.split('([^\w\'])', text)
ar = [x for x in ar if x != ' ' and x != '' and x != '\t']  # remove spaces
ar = ["' " if x == 'xxxasa' else
      " '" if x == 'xxxasb' else
      '...' if x == 'xxxellipsis' else
      x for x in ar]

print(*ar, sep='█\n')
#
# print()
# print()
#
# for s in ar:
#     getBrokenSimple(s)
