
def tokenizeOld(text):
    """break the text into an array of atoms"""
    text = re.sub('\t', ' ', text).strip()
    text = stupidify_quotes(text) \
        .replace('...', ' xxxellipsis ') \
        .replace("' ", ' xxxasa ') \
        .replace(" '", ' xxxasb ') \
        .replace('" ', ' xxxdqsa ') \
        .replace(' "', ' xxxdqsb ') \
        .replace('"', ' xxxdq ')
    # .replace("'", ' xxxsq ')

    # keep apostrophes cos important for word parsing (like "won't"
    ar = re.split('([^\w\'])', text)
    print("after split in tokenize:")
    print(ar)
    ar = [x for x in ar if x != ' ' and x != '' and x != '\t']  # remove spaces
    ar = ["' " if x == 'xxxasa' else
          " '" if x == 'xxxasb' else
          '" ' if x == 'xxxdqsa' else
          ' "' if x == 'xxxdqsb' else
          '"' if x == 'xxxdq' else
          "'" if x == 'xxxsq' else
          '...' if x == 'xxxellipsis' else
          x for x in ar]

    ar = list(filter(None, ar))

    print('ar in tokenize:')
    print(ar)
    parsed = []
    count = -1
    for s in ar:
        count += 1
        if count % 10000 == 0:
            print(count)
        word_atoms = atomize_word(s)
        parsed += word_atoms
    return parsed

