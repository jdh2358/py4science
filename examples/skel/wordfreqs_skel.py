#!/usr/bin/env python
"""Word frequencies - count word frequencies in a string."""

XXX = None # a sentinel for missing pieces

def word_freq(text):
    """Return a dictionary of word frequencies for the given text."""
    # you need to write this
    return XXX


def print_vk(lst):
    """Print a list of value/key pairs nicely formatted in key/value order."""

    # Find the longest key: remember, the list has value/key paris, so the key
    # is element [1], not [0]
    longest_key = max(map(lambda x: len(x[1]),lst))
    # Make a format string out of it
    fmt = '%'+str(longest_key)+'s -> %s'
    # Do actual printing
    for v,k in lst:
        print fmt % (k,v)


def freq_summ(freqs,n=10):
    """Print a simple summary of a word frequencies dictionary.

    Inputs:
      - freqs: a dictionary of word frequencies.

    Optional inputs:
      - n: the number of items to print"""

    words,counts =  XXX # look at the keys and values methods of dicts
    # Sort by count
    
    items =  XXX # think of a list, look at zip() and think of sort()

    print 'Number of words:',len(freqs)
    print
    print '%d least frequent words:' % n
    print_vk(items[:n])
    print
    print '%d most frequent words:' % n
    print_vk(items[-n:])


if __name__ == '__main__':
    # You need to read the contents of the file HISTORY.gz and store it in the
    # variable named 'text'.  Do NOT unzip it manually, look at the gzip module
    # from the standard library and the read() method of file objects.
    text =  XXX
    
    freqs = word_freq(text)
    freq_summ(freqs,20)
