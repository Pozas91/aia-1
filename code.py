# -*- coding: utf-8 -*-

# Importaciones de librerías requeridas
import re
import time
from tkinter import *

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

# Variable usada para medir los tiempos de ejecución
start_time = time.time()


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
        res += letter_max_prob + ' '
    
    return res


# Método unigram_palabras usado para proporcionar predicciones de palabras 
# en base a una cadena de números separados por espacio
def unigram_palabras(texto):
    res = ''
    
    for numBlock in texto.split(' '):
        
        max_prob = 0
        word_max_prob = ''
        
        for key, value in words.items():
            
            # Compruebo si el número que estamos recorriendo es igual al encontrado en el diccionario
            # de ser así entonces compruebo también que la probabilidad sea más alta que la anterior.
            # Sí es más alta obtengo su probabilidad y la letra a la que se corresponde.
            if value[1] == numBlock and value[0] > max_prob:
                max_prob = value[0]
                word_max_prob = key

        # Almaceno la letra más probable en la variable res
        res += word_max_prob + ' '
    
    return res

# TESTING  
print("************************** TESTING ******************************")
print("Texto: Hola -> Predicción: " + unigram_letras('3 5 4 1'));
print("Texto: Hola -> Predicción: " + unigram_palabras('3541'));
print("Texto: Hola que tal estas -> Predicción: " + unigram_palabras('3541 672 714 26716'));
print("Texto: Tengo mucho miedo -> Predicción: " + unigram_palabras('72535 57135 53225'));

# Tiempo de ejecución obtenido
print("Tiempo de ejecución en segundos: --- %s seconds ---" % (time.time() - start_time))

# Interfaz gráfica
def show_unigram_letras():
    e3.delete(0,END)
    res = unigram_letras(e2.get())
    print("Entrada: %s\n" % res)
    e3.insert(10,res)
   
def show_unigram_palabras():
    e3.delete(0,END)
    res = unigram_palabras(e2.get())
    print("Entrada: %s\n" % res)
    e3.insert(10,res)

master = Tk()
master.title("Texto predictivo")
master.minsize(width=350, height=150)

Label(master, text="Text").grid(row=0)
Label(master, text="Entrada").grid(row=1)
Label(master, text="Predicción").grid(row=3)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)

e1.insert(10,"soy bueno") 
e2.insert(10,"658 18255") #El bloque de números equivale a "Soy bueno"
e3.insert(10,"")

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=3, column=1)

Button(master, text='Unigram letras', command=show_unigram_letras).grid(row=6, column=0, sticky=W, pady=10)
Button(master, text='Unigram palabras', command=show_unigram_palabras).grid(row=6, column=1, sticky=W, pady=10)  

mainloop()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    