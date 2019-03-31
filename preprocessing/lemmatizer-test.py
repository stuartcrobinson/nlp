import lem


def test(st):
    atoms = lem.tokenize(st)
    atoms2 = atoms[:]
    print(atoms2)
    untokenized = lem.untokenize(atoms2)
    print(st)
    print(untokenized)


    strSplit = st.split(' ')
    untSplit = untokenized.split(' ')
    print('------------------------------------------------------------------------------')
    print(strSplit)
    print(untSplit)
    print('------------------------------------------------------------------------------')
    for i in range(0, len(strSplit)):
        if (strSplit[i] != untSplit[i]):
            print(strSplit[i], untSplit[i], "----", lem.getAdverbRoot(strSplit[i]),
                  lem.getAdverb(lem.getAdverbRoot(strSplit[i])))


# with open("../corpus/aliceInWonderland.txt", "r") as myfile:
#     data = myfile.read()
#     test(data)

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


test('"‘How queer it seems,’')
# 
# word = "'How'"
# parse(word, relations=True, lemmata=True)
