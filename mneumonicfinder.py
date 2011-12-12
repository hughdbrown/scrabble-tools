import os

def load_dictionary(longest_word_length):
    f = file('dict')
    out = f.readlines()
    # Strip the newlines
    out = map(lambda x: x[:-1], out)
    # Strip the acronyms
    out = filter(lambda x: not x==x.upper(), out)
    # Strip the long words
    if longest_word_length < 0:
        longest_word_length = 8
    out = filter(lambda x: len(x)<=longest_word_length, out)
    return out

def uniqueletters(chars):
    x=1
    while x<len(chars):
        chars=chars[:x] + chars[x:].replace(chars[x-1],'')
        x+=1
    return chars

def intersect(word, charlist):
    '''How many characters do these two strings have in common?'''
    word = uniqueletters(word)
    count = 0
    for key in word:
        if key in charlist: count+=1
    return count

def create_mneumonic(charlist, wordlist):
    '''Return an array of words from wordlist which covers all characters in charlist.'''
    out = []
    while len(charlist):
        best=0
        bestword = ''
        for word in wordlist:
            score = intersect(word,charlist)
            if score > best:
                best = score
                bestword = word
        if not len(bestword):
            print 'No further mneumonics can be found.'
            return []
        out.append(bestword)
        # Subtract the bestword from the remaining characters to cover
        for key in bestword:
            charlist = charlist.replace(key,'')
    return out


def get_subset_words(dictionary, charlist):
    out = []
    for word in dictionary:
        for letter in word:
            if not letter in charlist: break
        else:
            out.append(word)
    return out


def main(charlist, longest_word_length):
    charlist = charlist.lower()
    charlist = uniqueletters(charlist)
    print "==> MneumonicFinder v1.0"
    print "--> Loading dictionary..."
    dictionary = load_dictionary(longest_word_length)
    print "--> Search string:", charlist
    words = get_subset_words(dictionary, charlist)

    # Sort words by length
    def comparator(a,b):
        return len(a)-len(b)

    # Process the word list
    words.sort(cmp=comparator)

    # Build some mneumonics
    print '--> Generating...'
    while True:
        mneumonic = create_mneumonic(charlist, words)
        if not len(mneumonic): break
        print "--> Mneumonic:", mneumonic
        words = filter(lambda x: x not in mneumonic, words)



if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Search the dictionary for mneumonic strings of words used to memorize a set of characters.')
    parser.add_argument('charlist', metavar='characters', type=str, help='List of characters to memorize')
    parser.add_argument('--maxlen', dest='length', default=-1, type=int, help='Longest permitted length of word')

    args = parser.parse_args()
    main(args.charlist, args.length)
