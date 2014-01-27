#!/usr/bin/env python3

import os
from json import loads
from urllib import request
from string import ascii_lowercase as alpha
from itertools import product
from time import sleep
from re import sub

class GoogleQuery:

  def __init__(self):
    self.PREFIX_FILE = "common-prefixes-why.txt"
    self.WORD_LIST = "most-common-10000.txt"
    self.OPTION = "wordlist"
    self.PREFIX = "Why"
    self.DEPTH = 1
    self.TIMEOUT = 2

  def Query(self, query, timeout = 0):
    sleep(timeout)
    return loads(request.urlopen("http://suggestqueries.google.com/complete/search?client=firefox&q=" + query).read().decode('utf-8'))[1]

  def permutations(self, iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    for indices in product(range(n), repeat=r):
      if len(set(indices)) == r:
        yield tuple(pool[i] for i in indices)

  def BruteForce(self, depth):
    for i in self.permutations(alpha, depth):
      i = ''.join(i)
      yield i

  def GetSuggestions(self, indice = 0, option = None, depth = None, timeout = None, prefix = None):
    if not option:
      option = self.OPTION
    if not depth:
      depth = self.DEPTH
    if not timeout:
      timeout = self.TIMEOUT
    if not prefix:
      prefix = self.PREFIX
    common_prefixes = (open(self.PREFIX_FILE, "r").read()).split('\n')
    common_prefixes.pop()
    output = open("output.txt", "a")
    if option == "bruteforce":
      for b in self.BruteForce(depth):
        for i in common_prefixes:
          parsed = (prefix + i + " " + b).replace(" ", "%20")
          for suggestion in self.Query(parsed, timeout):
            print(suggestion)
            output.write(suggestion + '\n')
    elif option == "wordlist":
      word_list = (open(self.WORD_LIST, "r").read()).rsplit()
      try:
        for word in word_list[indice:]:
          for i in common_prefixes:
            parsed = (prefix + " " + i + " " + word).replace(" ", "%20")
            for suggestion in self.Query(parsed, timeout):
              print(suggestion)
              output.write(suggestion + '\n')
          indice += 1
      except KeyboardInterrupt:
        print(indice)
    output.close()

def main():
  g = GoogleQuery()
  g.GetSuggestions(65)

if __name__ == '__main__':
  main()
