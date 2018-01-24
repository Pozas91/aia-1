# -*- coding: utf-8 -*-

import re

path = "data/corpus.txt"
letters = {}
words = {}
totalWords = 0
totalLetters = 0

encodingDictionary = {
    '1': ['a', 'á', 'b', 'c'],
    '2': ['d', 'e', 'é', 'f'],
    '3': ['g', 'h', 'i', 'í'],
    '4': ['j', 'k', 'l'],
    '5': ['m', 'n', 'ñ', 'o', 'ó'],
    '6': ['p', 'q', 'r', 's'],
    '7': ['t', 'u', 'ú', 'v'],
    '8': ['w', 'x', 'y', 'z']
}

def encoding(word):
  res = ''
    
  for letter in list(word):
    for key in encodingDictionary:
      if letter in encodingDictionary.get(key):
        res += key
        break
            
  return res

def applyStatistics(items, total):
  for item in items:
    items[item][0] = items[item][0] / totalWords


# Programm execution
with open(path, "r", encoding="utf8") as file:

  for line in file.readlines():
      
    line = re.sub('[^A-Za-z\u00C0-\u017F]+', ' ', line)
    line = re.sub('[\s]+', ' ', line)
          
    for word in map(lambda x: x.strip().lower(), line.split(' ')):
              
      if word in words:
        words[word][0] += 1
      else:
        words[word] = [1, encoding(word)]
          
      totalWords += 1
          
      for letter in list(word):
          
        if letter in letters:
          letters[letter][0] += 1
        else:
          letters[letter] = [1, encoding(letter)]
              
        totalLetters += 1
        
applyStatistics(words, totalWords)
applyStatistics(letters, totalLetters)