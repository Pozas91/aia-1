# -*- coding: utf-8 -*-

# Importaciones de librerías requeridas
import re

# Variables globales
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


# Método utilizado para realizar el conteo de las letras
def encoding(word):
  res = ''
    
  for letter in list(word):
    for key in encodingDictionary:
      if letter in encodingDictionary.get(key):
        res += key
        break
            
  return res

# Método utilizado para aplicar estadística a los distintos items, es decir,
# este método nos calcula la probabilidad de las palabras/letras en base al total de ellas.
def applyStatistics(items, total):
  for item in items:
    items[item][0] = items[item][0] / totalWords


# En esta sección abrimos el fichero como lectura y con codificación utf8 para así tratar tildes, etc.
# Además, sacamos todas las palabras y letras del corpus y realizamos el conteo de las mismas.
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


# Método unigram_letras usado para proporcionar predicciones de letras 
# en base a una cadena de números separados por espacio
def unigram_letras(texto):
    res = ''
    
    for num in texto.split(' '):
        
        max_prob = 0
        letter_max_prob = ''
        
        for key, value in letters.items():
            
            # Compruebo si el número que estamos recorriendo es igual al encontrado en el diccionario
            # de ser así entonces compruebo también que la probabilidad sea más alta que la anterior.
            # Sí es más alta obtengo su probabilidad y la letra a la que se corresponde.
            if value[1] == num and value[0] > max_prob:
                max_prob = value[0]
                letter_max_prob = key

        # Almaceno la letra más probable en la variable res
        res += letter_max_prob
    
    return res
    

# Llamamos al método unigram_letras pasandole como números la palabra HOLA    
print(unigram_letras('3 5 4 1'));
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    