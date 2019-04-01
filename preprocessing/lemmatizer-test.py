import lem


def test(st):
    # print(st)

    # aIn = lem.parse_text(st)

    tIn = lem.tokenize(st)
    # print("tokenized:")
    # print(tIn)
    tInLc = [x.lower() for x in tIn]
    aIn = lem.atomize(tIn)[:]

    set_tInLc = set(tInLc)
    set_aIn = list(set(aIn))
    set_aIn.sort()

    # print("set_tInLc: " + str(set_tInLc))
    # print("set_aIn: " + str(set_aIn))
    # print("set_tInLc length: ", len(set_tInLc))
    # print("set_aIn length:    ", len(set_aIn))
    print("atomized:")
    print(aIn)
    deparsed = lem.deparse_text(aIn)
    tOut = lem.tokenize(deparsed)
    # print("deparsed:")
    # print(deparsed)
    # print('##############################################################################')
    # print(tIn)
    # print('------------------------------------------------------------------------------')
    # print(tOut)
    # print('##############################################################################')
    # print("set_aIn")
    # print(set_aIn)
    result = '✅'
    for i in range(0, len(tIn)):
        if tIn[i] != tOut[i]:
            result = '❌'
            print("i:", i, "tIn[i]:", tIn[i], "tOut[i]:", tOut[i], "----", lem.getAdverbRoot(tIn[i]),
                  lem.getAdverb(lem.getAdverbRoot(tIn[i])))
    print('---------------------')
    print("set_tInLc length: ", len(set_tInLc))
    print("set_aIn length:    ", len(set_aIn))
    print('---------------------')
    print(" tIn len:", len(tIn))
    print("tOut len:", len(tOut))
    print(result)


# with open("../corpus/aliceInWonderland.txt", "r") as myfile:
with open("../corpus/harry-potter/original/text-processed/7.txt", "r") as myfile:
    data = myfile.read()
    test(data)

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

# text = """‘How queer it seems,’ Alice said to herself, ‘to be going messages for a rabbit! I suppose Dinah’ll be sending me on messages next!’ And she began fancying the sort of thing that would happen: ‘“Miss Alice! Come here directly, and get ready for your walk!” “Coming in a minute, nurse! But I’ve got to see that the mouse doesn’t get out.” Only I don’t think,’ Alice went on, ‘that they’d let Dinah stop in the house if it began ordering people about like that!’
# By this time she had found her way into a tidy little room with a table in the window, and on it (as she had hoped) a fan and two or three pairs of tiny white kid gloves: she took up the fan and a pair of the gloves, and was just going to leave the room, when her eye fell upon a little bottle that stood near the looking-glass. There was no label this time with the words ‘DRINK ME,’ but nevertheless she uncorked it and put it to her lips. ‘I know something interesting is sure to happen,’ she said to herself, ‘whenever I eat or drink anything; so I’ll just see what this bottle does. I do hope it’ll make me grow large again, for really I’m quite tired of being such a tiny little thing!’
# It did so indeed, and much sooner than she had expected: before she had drunk half the bottle, she found her head pressing against the ceiling, and had to stoop to save her neck from being broken. She hastily put down the bottle, saying to herself ‘That’s quite enough—I hope I shan’t grow any more—As it is, I can’t get out at the door—I do wish I hadn’t drunk quite so much!’"""
# test(text)

# test('"‘How queer ...it seems,’')
# test('how many training spellbooks wands agreement disregard.')
# test("""‘How queer
#
#
# ya'll        seems,’    Alice \"cOulD\" can didn't said Auf\'Has to herselF""")  # , ‘to be going messages for a rabbit! I suppose Dinah’ll be sending me’""")
# test('"‘How queer it seems,’ Alice didn\'t said Auf\'Has to herself! I suppose Dinah’ll’')
# test("ya'll y'all won't couldn't asdf'fwef")
# test('We see what he sees i kick he kicks he bites they bite he runs she ran wins win won ride rode clap claps write wrote')
# word = "'How'"
# parse(word, relations=True, lemmata=True)
# test("happen: ‘“Miss")

# TODO - how to clean specific formats ... specific code per each ... not as simple as regex matching line
# cos sometimes chapter name above or below "CHAPTER X" line
