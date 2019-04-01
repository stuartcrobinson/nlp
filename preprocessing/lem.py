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


# note - this untokenizes text by using the dictionary of root+POS keys it created during tokenization: m_rootPos_word
# not super clever.

wnl = WordNetLemmatizer()

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

capsCharsList = ['█', '▟', '▙', '▛', '▜', '▞', '▚', '▘', '▝', '▗', '▖']

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
    """this is confusing cos capitalization count has to skip over caps chars.  is that stupid ?"""
    #     print('  in getCapsChars')
    if word.isupper():
        return [m_i_capChar[0]]
    wordlen = len(word)
    capsChars = []
    capsCount = 0
    for i in range(0, wordlen):
        letterIndex = wordlen - 1 - i
        letter = word[letterIndex]
        print('letter:', letter)
        if letter.isupper():
            try:
                capsChars = [m_i_capChar[wordlen - i + capsCount]] + capsChars
                print('capschars:', capsChars)
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
        word = capitalizeSpecificLetterAtIndex(
            word, m_capChar_i[capsChar] - 1 - count)
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


roots_to_ignore = {"fee", "layer", "be", "re-cover", "blac"}
words_to_ignore = {}

duplicateWordForms = []


# ?????
# was, were, am, are -- these words get tokenized/untokenized unreliably. :(
# ?????

def parse_custom(word_lower):
    # 'un
    # 'dis
    # ment'
    # ing'
    # 'over
    # 'under
    # ly'
    # ed'
    patterns = ['^un', '^dis', '^over', '^under', 'ment$', 'ing$', 'ly$', 'ed$']

    for pattern in patterns:
        # print("parse custom:", word_lower, pattern)
        if re.search(pattern, word_lower):
            root = re.sub(pattern, '', word_lower)
            pos = posChar + pattern
            # print('MATCHED', pattern, root, pos)
            return word_lower, root, pos

    return word_lower, word_lower, ''

def atomize_word(og_word):
    """wtf is going on here"""
    global duplicateWordForms
    ''' returns word parsed into array of caps chars, word root, and POS tag if any'''
    if og_word.isspace():
        return [og_word]
    returner = []
    if og_word in words_to_ignore:
        return getCapsChars(og_word) + [og_word.lower()]
    pattern_parsed_list = parse(og_word, relations=True, lemmata=True).split()[0]
    # print(og_word, pattern_parsed_list)  # keep this
    for patternParsed in pattern_parsed_list:
        word, root, pos = postParse(patternParsed)  # pos starts w/ posChar
        # print("word, root, pos")
        # print(word, root, pos)
        if len(pattern_parsed_list) == 1:
            word = og_word  # to keep the spaces attached to single tokens like "' "
        elif "'" in word:
            word = '←' + word
        caps_chars = []
        word_has_caps = not word.islower()
        word_lower = word.lower() if word_has_caps else word
        if word_has_caps:
            caps_chars = getCapsChars(word)
            print("caps_chars")
            print(caps_chars)
        if root == word_lower:
            ''' this means there are no pattern-supplied POS tags we need to keep '''
            # check for custom prefix/postfix
            if len(pattern_parsed_list) == 1:
                word_lower, root, pos = parse_custom(word_lower)
        if root == word_lower:
            ''' now there are def no POS tags we need to keep '''
            returner += caps_chars + [word_lower]
        else:
            if root in roots_to_ignore or "'" in word:
                returner += caps_chars + [word_lower]
            else:
                use_parsed = True
                key = root + pos
                if key in m_rootPos_word:
                    value = m_rootPos_word[key]
                    if value != word_lower:
                        duplicateWordForms += [(key, value, word_lower)]
                        use_parsed = False
                if use_parsed:
                    m_rootPos_word[key] = word_lower
                    #uncomment this stuff to allow for 2nd degree parsing!!!!
                    # word2, root2, pos2 = parse_custom(root)
                    # if word2 != root2:
                    #     m_rootPos_word[root2 + pos2] = word2
                    #     returner += caps_chars + [root2, pos2, pos]
                    # else:
                    returner += caps_chars + [root, pos]
                else:
                    returner += caps_chars + [word_lower]
    # 2nd degree parsing ?  worth it?  deparseable?
    # if len(returner) > 1:
    #     word_has_caps = returner[0] in caps_chars
    #     word = returner[0] if not word_has_caps else returner[1]
    #     pos_og =''
    #     for x in returner:
    #         if '▓' in x:
    #             pos_og = x
    #             break
    #     if re.search('\w+', word):
    #         word_lower, root, pos = parse_custom(word)
    #     if word_lower != root:
    #         if word_has_caps:
    #             returner = returner[0]
    print('atomize_word returner:', returner)
    return returner


def stupidify_quotes(text):
    return text \
        .replace('”', '"') \
        .replace('“', '"') \
        .replace('‘', "'") \
        .replace('’', "'")


def parse_text(text):
    """tokenize - break into original-capitalization word or punctuation units array
       atomize - break words into atoms parsed by both lemmatization and capitalization"""
    tokenized = tokenize(text)
    print("tokenized:")
    print(tokenized)
    atomized = atomize(tokenized)
    print("atomized:")
    print(atomized)
    return atomized


def maskInternalApostrophes(text, mask):
    # https://stackoverflow.com/questions/32389636/how-to-replace-multiple-overlapping-patterns-with-regex?rq=1
    return re.sub(r"(\w+)\'(?=\w+)", r'\1' + mask, text)


def splitNonWordExceptInternalApostrophe(text):
    # return re.split('[^\w]', text)
    # return re.split('([^(\w|.\'.)])', text)
    # return re.split(r'([^\w|\'])', text)
    return re.split(r'([^\w]|乂)', text)


def is_junk(line):
    return (line.isupper() and "." not in line) or \
           (not ('"' in line or '.' in line)) or \
           "Generated by " in line or \
           "-The End-" in line or \
           "Chapter" in line or \
           "CHAPTER" in line or \
           "Notes" in line or \
           "end of the chapter" in line or \
           "tumblr" in line or \
           re.match("^\d.*", line) or \
           re.match("2\d\d\d", line) or \
           re.match("fan *fic", line) or \
           line.lower().startswith("Page ".lower()) or \
           line.lower().startswith("This eBook was created ".lower()) or \
           line.lower().startswith("About this Title".lower()) or \
           line.lower().startswith("Summary".lower()) or \
           line.lower().startswith("Warning".lower()) or \
           line.lower().startswith("Disclaimer".lower())


def removeLinesBefore(lines, param):
    i = 0
    firstLineIndex = 0
    while i < len(lines):
        if param in lines[i]:
            firstLineIndex = i
            break
        i += 1
    return lines[firstLineIndex:]


def clean(text):
    text = re.sub('\t+', ' ', text).strip()
    text = re.sub('“ ', '“', text)  # “Patil”
    text = re.sub(' ”', '”', text)
    text = re.sub(' ,', ',', text)
    text = re.sub(' \\.', '.', text)
    text = re.sub(' \\?', '?', text)
    text = re.sub(' !', '!', text)
    text = re.sub('\\.\\.\\.', '…', text)

    lines = text.split('\n')

    lines = removeLinesBefore(lines, "CHAPTER ONE")  # hp originals
    lines = removeLinesBefore(lines, "Notes")  # hp originals

    lines = [x.strip() for x in lines if not is_junk(x)]

    text = '\n'.join(lines)
    text = stupidify_quotes(text)
    # print(0)
    # print("[" + text + "]")
    return text


def tokenize(text):
    text = clean(text)
    """tokenize - break into original-capitalization word or punctuation units list"""
    text = text \
        .replace("' ", '乂xxxasaxxx乂') \
        .replace(" '", '乂xxxasbxxx乂') \
        .replace('" ', '乂xxxdqsaxxx乂') \
        .replace(' "', '乂xxxdqsbxxx乂') \
        .replace('"', '乂xxxdqxxx乂')
    # print(1)
    # print("[" + text + "]")

    internalApostropheMask = '乂A乂'
    text = maskInternalApostrophes(text, internalApostropheMask)
    # print(2)
    # print("[" + text + "]")

    # keep apostrophes cos important for word parsing (like "won't"
    ar = splitNonWordExceptInternalApostrophe(text)
    # print(3)
    # print(ar)

    ar = [x for x in ar if x != ' ' and x != '' and x != '\t' and x != '乂']  # remove spaces
    # print(4)
    # print(ar)

    ar = ["' " if x == 'xxxasaxxx' else
          " '" if x == 'xxxasbxxx' else
          '" ' if x == 'xxxdqsaxxx' else
          ' "' if x == 'xxxdqsbxxx' else
          '"' if x == 'xxxdqxxx' else
          "'" if x == 'xxxsqxxx' else
          x for x in ar]
    # print(5)
    # print(ar)

    ar = [x.replace(internalApostropheMask, "'") if internalApostropheMask in x else x for x in ar]
    # print(6)
    # print(ar)

    return list(filter(None, ar))


def atomize(tokens):
    """parse each token by its capitalization and lemma"""
    parsed = []
    count = -1
    for token in tokens:
        count += 1
        if count % 10000 == 0:
            print(count)
        word_atoms = atomize_word(token)
        parsed += word_atoms
    return parsed


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

m_rootPos_word = {}


# #metrically
# def untokenizeWord(atom, pos):
#     return m_rootPos_word[atom + pos]


def deparse_text(atoms):
    ''' have to go backwards from the end to untokenize words before applying correct caps '''
    #     atoms = atoms_[:]
    caps_chars = []
    i = len(atoms)
    print('here WTFFFFFF')
    while i >= 0:
        i -= 1
        atom = atoms[i]
        print("in untokenize: i: " + str(i) + " , atom: " + atom)
        if atom[0] == posChar:
            pos = atom  # [1:]  # remove the leading posChar
            prevAtom = atoms[i - 1]
            print('atom:', atom, 'prevatom:', prevAtom)
            del atoms[i]
            i -= 1
            result = ''
            if prevAtom[0] == posChar:
                prevPrevAtom = atoms[i - 1]
                del atoms[i]
                i -= 1
                result1 = m_rootPos_word[prevPrevAtom + prevAtom]
                if result1 is None:
                    raise Exception("nonetype found 1, ", prevPrevAtom, prevAtom, result1)
                print('prevprevatom', prevPrevAtom, 'prevatom', prevAtom, 'result1', result1)
                result = m_rootPos_word[result1 + pos]
                if result is None:
                    raise Exception("nonetype found 1, ", result1, pos, result)
                print('result', result)
            else:
                result = m_rootPos_word[prevAtom + pos]
                if result is None:
                    raise Exception("nonetype found 1, ", prevAtom, pos, result)
            atoms[i] = result
            continue
        if atom in capsCharsList:
            caps_chars = [atom] + caps_chars
            del atoms[i]
            while atoms[i - 1] in capsCharsList and i > 1:
                ''' now build entire caps_chars array - and delete them from atoms as u go'''
                i -= 1
                caps_chars = [atoms[i]] + caps_chars
                del atoms[i]
            if i < len(atoms):
                atoms[i] = capitalizeWord(atoms[i], caps_chars)
                if atoms[i] == None:
                    raise Exception("nonetype found 2")
                caps_chars = []
            else:
                raise Exception(
                    "there wasn't a word to capitalize, after caps chars")
    # atoms = [x if x == "..." or '"' in x or "'" in x else (x + " ") for x in atoms]

    i = 0
    output = ""
    while i < len(atoms) - 1:
        atom = atoms[i]
        atom_next = atoms[i + 1]
        output += atoms[i]

        if ("←" in atom_next):
            atoms[i + 1] = atoms[i + 1][1:]
        elif (not ('"' in atom or "' " == atom or " '" == atom or "'" == atom or "…" == atom or
                   '"' in atom_next or "' " == atom_next or " '" == atom_next or "'" == atom_next or "…" == atom_next or
                   "." in atom_next or "," in atom_next or
                   '?' in atom_next or "!" in atom_next)):
            output += " "
        i += 1
    output += atoms[len(atoms) - 1]
    return output


'''
TODO - caps chars.  then tokenizing and untokeninzing will be complete!!!!!!!!!!!!!!!!!!!

then, get texts, read texts, build word2vec (or glove????) embedding, then use to train NN!

'''


# displayParsed("isn't rather we're very quickly exceedingly sleep-deprived deprived of sleep hungrier than their's quicken the sunken ship")

# st = "Mrs. Stephens took in her long flowing auburn hair, her slightly pale face with large blue eyes. She wore a fair bit of make up, with blue eyeshadow filling her eyelids and deep red lipstick emphasisng her lips. She wore clothes Severus could only identify as a Muggles mini dress mixed with a traditional witch's corset."
# st = "do you want an apple or a carrot"
# print(tokenize(str))


# st = """‘How queer it seems,’ Alice said to herself, ‘to be going messages for a rabbit! I suppose Dinah’ll be sending me on messages next!’ And she began fancying the sort of thing that would happen: ‘“Miss Alice! Come here directly, and get ready for your walk!” “Coming in a minute, nurse! But I’ve got to see that the mouse doesn’t get out.” Only I don’t think,’ Alice went on, ‘that they’d let Dinah stop in the house if it began ordering people about like that!’
# By this time she had found her way into a tidy little room with a table in the window, and on it (as she had hoped) a fan and two or three pairs of tiny white kid gloves: she took up the fan and a pair of the gloves, and was just going to leave the room, when her eye fell upon a little bottle that stood near the looking-glass. There was no label this time with the words ‘DRINK ME,’ but nevertheless she uncorked it and put it to her lips. ‘I know something interesting is sure to happen,’ she said to herself, ‘whenever I eat or drink anything; so I’ll just see what this bottle does. I do hope it’ll make me grow large again, for really I’m quite tired of being such a tiny little thing!’
# It did so indeed, and much sooner than she had expected: before she had drunk half the bottle, she found her head pressing against the ceiling, and had to stoop to save her neck from being broken. She hastily put down the bottle, saying to herself ‘That’s quite enough—I hope I shan’t grow any more—As it is, I can’t get out at the door—I do wish I hadn’t drunk quite so much!’"""

# str = ' afterward already almost back better best even far fast hard here how late long low more near never next now often quick rather slow so soon still then today tomorrow too very well where yesterday quickly eat the pizzas'


def asdf(st):
    #     st = 'QUICK eat the pizzas'
    atoms = tokenize(st, stupidifyQuotes=False)
    atoms2 = atoms[:]
    untokenized = deparse_text(atoms2)
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
    untokenized = deparse_text(atoms2)

    strSplit = st.split(' ')
    untSplit = untokenized.split(' ')
    print('here')
    for i in range(0, len(strSplit)):
        if (strSplit[i] != untSplit[i]):
            print(strSplit[i], untSplit[i], "----", getAdverbRoot(strSplit[i]),
                  getAdverb(getAdverbRoot(strSplit[i])))

# # with open ("aliceInWonderland.txt", "r") as myfile:
# #     data=myfile.read()


# from os import listdir
# from os.path import isfile, join

# files = listdir('/Users/stuart.robinson/Downloads/HarryPotterSeriesAllEbooksByJKRowlingDobd99')
# # hpstring = ''
# #
# # for f in files:
# #     if ".txt" in f:
# #         print(f)
# #         with open ('/Users/stuart.robinson/Downloads/HarryPotterSeriesAllEbooksByJKRowlingDobd99/' + f, "r") as myfile:
# #             hpstring += myfile.read()


# # asdf('"‘How queer it seems,’')
# #
# # word = "'How'"
# # parse(word, relations=True, lemmata=True)
