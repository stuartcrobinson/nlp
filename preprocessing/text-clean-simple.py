import fileinput
import re


# for line in fileinput.input(['thefile.txt'], inplace=True):
#     print(line.replace('old stuff', 'shiny new stuff'), end='')

f = open("tmp.txt", "w")


with open('thefile.txt', 'r') as myfile:
    text = myfile.read() \
        .replace('shiny', 'crusty') \
        .replace('new', 'old') \
        .replace('”', '"') \
        .replace('“', '"') \
        .replace('‘', '"') \
        .replace('’', '"')

    ar = re.split('([^\w\'′]|_| )', text)   
    print(ar)  
    # ar = list(filter(None, ar))
    
    # f.write(text)
