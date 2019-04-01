import lem

# print(lem.atomize_word('uncertainly'))


#
capsCharsList = ['█', '▟', '▙', '▛', '▜', '▞', '▚', '▘', '▝', '▗', '▖']

m_i_capChar = dict((i, c) for i, c in enumerate(capsCharsList))

i = -1
while i < 9:
    i += 1
    print(i, m_i_capChar[i])

print(lem.getCapsChars('McDonald'))