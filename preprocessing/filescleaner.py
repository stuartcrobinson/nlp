import os

import lem

dir_in_og = "/Users/stuartrobinson/repos/nlp/corpus/harry-potter/original/text-unprocessed"
dir_ou_og = "/Users/stuartrobinson/repos/nlp/corpus/harry-potter/original/text-processed"
dir_in_ff = "/Users/stuartrobinson/repos/nlp/corpus/harry-potter/fanfiction/text-unprocessed"
dir_ou_ff = "/Users/stuartrobinson/repos/nlp/corpus/harry-potter/fanfiction/text-processed"

dir_in = dir_in_og
dir_ou = dir_ou_og

files_short = os.listdir(dir_in)

files_full = [os.path.join(dir_in, x) for x in files_short]

for input_file in files_short:
    # with open("../corpus/aliceInWonderland.txt", "r") as myfile:
    with open(os.path.join(dir_in, input_file), "r") as myfile:
        data = myfile.read()
        cleaned = lem.clean(data)
        print(cleaned, file=open(os.path.join(dir_ou, input_file), 'w'))

#
# print(files_short)
# print(files_full)
