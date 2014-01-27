#!/usr/bin/env python3

PREFIX_FILE = "common-prefixes-why.txt"
WORD_LIST = "most-common-10000.txt"
OPTION = "bruteforce"
PREFIX = "Why"
DEPTH = 1
TIMEOUT = 3

import os
from json import loads
from urllib import request
from string import ascii_lowercase as alpha
from itertools import product
from time import sleep
from re import sub

def GetSuggestions(query, timeout = 0):
    sleep(timeout)
    return loads(request.urlopen("http://suggestqueries.google.com/complete/search?client=firefox&q=" + query).read().decode('utf-8'))[1]


def permutations(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    for indices in product(range(n), repeat=r):
        if len(set(indices)) == r:
            yield tuple(pool[i] for i in indices)

def BruteForce(depth):
    for i in permutations(alpha, depth):
        i = ''.join(i)
        yield i

def main(option = OPTION, depth = DEPTH, timeout = TIMEOUT, indice = 0):
    prefix = PREFIX
    output = open("output.txt", "a")
    if option == "bruteforce":
        for i in BruteForce(depth):
            parsed = (prefix + " " + i + " " + word).replace(" ", "%20")
            for suggestion in GetSuggestions(query, timeout):
                print(suggestion)
                output.write(suggestion + '\n')
    elif option == "wordlist":
        common_prefixes = (open(PREFIX_FILE, "r").read()).split('\n')
        common_prefixes.pop()
        word_list = (open(WORD_LIST, "r").read()).rsplit()
        try:
            for word in word_list[indice:]:
                for i in common_prefixes:
                    parsed = (prefix + " " + i + " " + word).replace(" ", "%20")
                    for suggestion in GetSuggestions(parsed, timeout):
                        print(suggestion)
                        output.write(suggestion + '\n')
                indice += 1
        except KeyboardInterrupt:
            print(indice)
    output.close()

main("wordlist", DEPTH, TIMEOUT, 2)

#BruteForce(2)
#print(GetSuggestions(""))
