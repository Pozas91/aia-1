# -*- coding: utf-8 -*-

import re

path = "corpus.txt"

letters = {}
words = {}

with open(path, "r", encoding="utf8") as file:
    
    for line in file.readlines():
        
        filtered = re.sub('[^A-Za-z\u00C0-\u017F]+', ' ', line)
        lineClean = re.sub('[\s]+', ' ', filtered)
        
        preWords = filter(lambda x: len(x) > 1, lineClean.split(' '))
        
        for word in preWords:
            
            word = word.strip().lower()
            
            if word in words:
                words[word] += 1
            else:
                words[word] = 1
            
        