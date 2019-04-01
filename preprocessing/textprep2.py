#copied from repo dt2.  written 2017 ?
import re

# from PIL.WmfImagePlugin import word
from nltk import pos_tag
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# import capsParser
from pattern.en import parse, comparative, superlative, pluralize
# from _operator import pos

wnl = WordNetLemmatizer()

##################################################################################################################################################################
###############################################################  capsParser.py - eclipse too stupid for sep file? ################################################
##################################################################################################################################################################
##################################################################################################################################################################
'''
use these for caps chars:
█ - all caps
▟ -1
▙ -2
▛ -3
▜ -4
▞ -5
▚ -6
▘ -7
▝ -8
▗ -9
▖ -10 

# utf8 shapes http://www.fileformat.info/info/charset/UTF-8/list.htm?start=8000

input a word.  

create empty array of caps chars

make int count = 0

start at the end.  i = 0.  last letter.  if it's cap, prepend capschar(len(word)).  and count++

move to prev letter.  i = 1.  if cap, prepend capschar(len(word) - i + count).  and count++
move to prev letter.  i = 2.  if not cap, move on
move to prev letter.  i = 3.  if cap, prepend capschar(len(word) - i + count).  and count++

salaD

len = 5
5th letter
caps char - 5 letters away
capschar(5)


sAlaDS

len = 6
... eh let's just try it
'''

capsCharsList = ['█' , '▟' , '▙' , '▛' , '▜' , '▞' , '▚' , '▘' , '▝' , '▗' , '▖']

m_i_capChar = dict((i, c) for i, c in enumerate(capsCharsList))
m_capChar_i = dict((c, i) for i, c in enumerate(capsCharsList))
# 
# 
# def getCapsChar(n):
#     # this is stupid.  should be a map.
#     if n == 0: return '█'  # all caps
#     if n == 1: return '▟'  # all caps
#     if n == 2: return '▙'  # all caps
#     if n == 3: return '▛'  # all caps
#     if n == 4: return '▜'  # all caps
#     if n == 5: return '▞'  # all caps
#     if n == 6: return '▚'  # all caps
#     if n == 7: return '▘'  # all caps
#     if n == 8: return '▝'  # all caps
#     if n == 9: return '▗'  # all caps
#     if n == 10: return '▖'  # all caps
#     raise Exception("n must be between 0 and 10 inclusive")


def getCapsChars(word):
#     print('  in getCapsChars')
    if word.isupper():
        return [m_i_capChar[0]]
    wordlen = len(word)
    capsChars = []
    capsCount = 0
    for i in range(0, wordlen):
        letterIndex = wordlen - 1 - i
        letter = word[letterIndex]
        if letter.isupper():
            try:
                capsChars = [m_i_capChar[wordlen - i + capsCount]] + capsChars
#             print('    capsChars:', capsChars, 'word: ', word)
                capsCount += 1
            except:
                print('    ERROR capsChars:', capsChars, 'word: ', word)
    return capsChars


def capitalizeSpecificLetterAtIndex(my_string, n):
    try:
        return ''.join([my_string[:n], my_string[n].upper(), my_string[n + 1:]])
    except:
        return my_string


def capitalizeWord(word, capsChars):
    '''
    salaD
    
    
    for char in capsChar, GOING BACKWARDS - start at end!
    
    count = 0;
    
    determine capNumber cn.  capitalize word at index CN - 1.  then count++
    
    next caps char
    
    determine capNmber CN.  capitalize word at index CN - 1 + count
    '''
    if capsChars[0] == '█':
        return word.upper()
    
    count = 0
    for i in range(len(capsChars) - 1, 0 - 1, -1):
        capsChar = capsChars[i]
        word = capitalizeSpecificLetterAtIndex(word, m_capChar_i[capsChar] - 1 - count)
        count += 1
    return word
##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################

 

# TODO what if not found?
def getAdjectiveRoot(superlativeOrComparative):
    return wnl.lemmatize(superlativeOrComparative, 'a')


def isGerund(word):
    return pos_tag(word_tokenize(word))[0][1] == 'VBG'


def getGerundRoot(gerund):
    if gerund == "piping":
        return "pipe"
    return WordNetLemmatizer().lemmatize(gerund, 'v')

# think about 'quickening' - nested lemmas


posChar = '▓'


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


roots_to_ignore = set(["fee", "layer", "be", "re-cover", "blac"])
words_to_ignore = set([])

duplicateWordForms = []

def getBroken(word):
    global duplicateWordForms
#     print('in get broken. word: ', word)
    ''' returns word parsed into array of caps chars, word root, and POS tag if any''' 
    if word.isspace():
        return [word]
    returner = []
    if word in words_to_ignore:
        return getCapsChars(word) + [word.lower()]
    patternParsedList = parse(word, relations=True, lemmata=True).split()[0]
    for patternParsed in patternParsedList:
        word, root, pos = postParse(patternParsed)
        capsChars = []
        wordLower = word.lower()
        wordHasCaps = not word.islower()
        wordLower = word.lower() if wordHasCaps else word
#         print("wordHasCaps", wordHasCaps)
#         print(word, root, pos)
        if wordHasCaps:
            capsChars = getCapsChars(word)
#         if pos in unsupportedPoss:
#             returner += capsChars + [wordLower]
        if root == wordLower:
            ''' this means there are no POS tags we need to keep '''
            returner += capsChars + [wordLower]
        else:
            if root in roots_to_ignore or "'" in word or "‘" in word  or "’" in word :
                returner += capsChars + [wordLower]     #was, were, am, are -- these words get tokenized/untokenized unreliably. :(
            else:
                useParsed = True
                key = root + pos
                if key in m_rootPos_word:
                    value = m_rootPos_word[key]
                    if value != wordLower:
                        duplicateWordForms += [(key, value, wordLower)]
                        useParsed = False
                if useParsed:
                    m_rootPos_word[root + pos] = wordLower
                    returner += capsChars + [root, pos]
                else:
                    returner += capsChars + [wordLower]
    return returner

# getBroken(str)


#         text = text.replace('′', "'")
#         text = text.replace('‘', "'")
#         text = text.replace('’', "'")
#         text = text.replace('“', '"')
# 
# def displayParsed(text):
#     text = text.lower()
#     text = text.replace('′', "'")
#     text = text.replace('‘', "'")
#     text = text.replace('’', "'")
#     text = text.replace('“', '"')
#     text = text.replace('”', '"')
#     text = text.replace('“', '"')
#     text = text.replace('”', '"')
#     ar = re.split('([^\w\'′]|_| |-)', text) 
#     ar = list(filter(None, ar))
#     # print(*ar, sep='\n')
#     for s in ar:
#         wordAtoms = getBroken([s])
#         print('orig: <' + str(s) + '> broken: ' + str(wordAtoms))


def parseCapitalization(wordAtoms):
    return wordAtoms



def tokenize(text, stupidifyQuotes=True):
#     print("in tokenize")
    if stupidifyQuotes:
        text = text.replace('′', "'")
        text = text.replace('‘', "'")
        text = text.replace('’', "'")
        text = text.replace('“', '"')
        text = text.replace('”', '"')
        text = text.replace('“', '"')
        text = text.replace('”', '"')
    ar = re.split('([^\w\'′]|_| )', text)     
    ar = list(filter(None, ar))
    parsed = []
    count = -1
    for s in ar:
        count += 1
        if count % 10000 == 0:
            print(count)
        capsChars = []
#         s = s.lower()
#         print("s: ", s)
        wordAtoms = getBroken(s)
#         print('  wordAtoms', wordAtoms)
#         print('  capsChars', capsChars)
#         print('  type(capsChars)', type(capsChars))
        parsed_ = parseCapitalization(wordAtoms)
        parsed += capsChars + wordAtoms
#         print('  parsed', parsed)
    return parsed


#
# 1.  split corpus at spaces and punct:
# https://stackoverflow.com/questions/1059559/split-strings-with-multiple-delimiters
# https://stackoverflow.com/a/16840963/8870055
# https://stackoverflow.com/questions/17245123/getting-adjective-from-an-adverb-in-nltk-or-other-nlp-library
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
    'futile':'futilely',
    'untrue':'untruly',
    'true':'truly',
    'undue':'unduly',
    'wry':'wryly',
    'shy':'shyly',
    'spacial':'spatially',
    'public':'publicly',
    'vile':'vilely',
    'agile':'agilely',
    'coy':'coyly',
    'aborad':'aborally',
    'pale':'palely',
    'whole':'wholly',
    }


m_rootPos_word = {}

# #metrically
# def untokenizeWord(atom, pos):
#     return m_rootPos_word[atom + pos]


def untokenize(atoms):
    ''' have to go backwards from the end to untokenize words before applying correct caps '''
    capsChars = []
    i = len(atoms)
    while i >= 0:
        i -= 1
        atom = atoms[i]
#         print("in untokenize: i: " + str(i) + " , atom: " + atom)
        if atom[0] == posChar:
            pos = atom #[1:]  # remove the leading posChar
            prevAtom = atoms[i - 1]
            del atoms[i]
            i -= 1
            result = m_rootPos_word[prevAtom + pos]
            if result == None:
                raise Exception("nonetype found 1, ", prevAtom, pos, result)
            atoms[i] = result
            continue
        if atom in capsCharsList:
            capsChars = [atom] + capsChars
            del atoms[i]
            while atoms[i - 1] in capsCharsList and i > 1:
                ''' now build entire capsChars array - and delete them from atoms as u go'''
                i -= 1
                capsChars = [atoms[i]] + capsChars
                del atoms[i]
            if i < len(atoms):
                atoms[i] = capitalizeWord(atoms[i], capsChars)
                if atoms[i] == None:
                    raise Exception("nonetype found 2")
                capsChars = []
            else:
                raise Exception("there wasn't a word to capitalize, after caps chars")
    return ''.join(atoms)


'''
TODO - caps chars.  then tokenizing and untokeninzing will be complete!!!!!!!!!!!!!!!!!!!

then, get texts, read texts, build word2vec (or glove????) embedding, then use to train NN!



'''

# displayParsed("isn't rather we're very quickly exceedingly sleep-deprived deprived of sleep hungrier than their's quicken the sunken ship")

# st = "Mrs. Stephens took in her long flowing auburn hair, her slightly pale face with large blue eyes. She wore a fair bit of make up, with blue eyeshadow filling her eyelids and deep red lipstick emphasisng her lips. She wore clothes Severus could only identify as a Muggles mini dress mixed with a traditional witch's corset."
# st = "do you want an apple or a carrot"
# print(tokenize(str))


st = """‘How queer it seems,’ Alice said to herself, ‘to be going messages for a rabbit! I suppose Dinah’ll be sending me on messages next!’ And she began fancying the sort of thing that would happen: ‘“Miss Alice! Come here directly, and get ready for your walk!” “Coming in a minute, nurse! But I’ve got to see that the mouse doesn’t get out.” Only I don’t think,’ Alice went on, ‘that they’d let Dinah stop in the house if it began ordering people about like that!’
# By this time she had found her way into a tidy little room with a table in the window, and on it (as she had hoped) a fan and two or three pairs of tiny white kid gloves: she took up the fan and a pair of the gloves, and was just going to leave the room, when her eye fell upon a little bottle that stood near the looking-glass. There was no label this time with the words ‘DRINK ME,’ but nevertheless she uncorked it and put it to her lips. ‘I know something interesting is sure to happen,’ she said to herself, ‘whenever I eat or drink anything; so I’ll just see what this bottle does. I do hope it’ll make me grow large again, for really I’m quite tired of being such a tiny little thing!’
# It did so indeed, and much sooner than she had expected: before she had drunk half the bottle, she found her head pressing against the ceiling, and had to stoop to save her neck from being broken. She hastily put down the bottle, saying to herself ‘That’s quite enough—I hope I shan’t grow any more—As it is, I can’t get out at the door—I do wish I hadn’t drunk quite so much!’""" 

# str = ' afterward already almost back better best even far fast hard here how late long low more near never next now often quick rather slow so soon still then today tomorrow too very well where yesterday quickly eat the pizzas' 


def asdf(st):
#     st = 'QUICK eat the pizzas'
    atoms = tokenize(st, stupidifyQuotes=False)
    atoms2 = atoms[:]
    untokenized = untokenize(atoms2)
    print()
    print(st)
    print()
    print(atoms)
    print()
    print("scr untokenized")
    print(untokenized)


def test(st):
    atoms = tokenize(st, stupidifyQuotes=False)
    atoms2 = atoms[:]
    print(atoms)
    print(atoms2)
    untokenized = untokenize(atoms2)
    
    strSplit = st.split(' ')
    untSplit = untokenized.split(' ')
    print('here')
    for i in range(0, len(strSplit)):
        if (strSplit[i] != untSplit[i]):
            print(strSplit[i], untSplit[i], "----", getAdverbRoot(strSplit[i]),  getAdverb(getAdverbRoot(strSplit[i])))


# with open ("aliceInWonderland.txt", "r") as myfile:
#     data=myfile.read()


# from os import listdir
# from os.path import isfile, join

# files = listdir('/Users/stuart.robinson/Downloads/HarryPotterSeriesAllEbooksByJKRowlingDobd99')
# hpstring = ''
# 
# for f in files:
#     if ".txt" in f:
#         print(f)
#         with open ('/Users/stuart.robinson/Downloads/HarryPotterSeriesAllEbooksByJKRowlingDobd99/' + f, "r") as myfile:
#             hpstring += myfile.read()



# asdf('"‘How queer it seems,’')
# 
# word = "'How'"
# parse(word, relations=True, lemmata=True)


test(st)
