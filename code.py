# -*- coding: utf-8 -*-

# Importaciones de librerías requeridas
import re
import time
import tkinter as tk
import sys
import textwrap
import random
from collections import Counter

# Variables globales
path = "data/corpus.txt"
letters = {}
letters_pair = {}
words = {}
words_pair = {}
total_words = 0
total_letters = 0

encoding_dictionary = {
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

"""
Método utilizado para realizar el conteo de las letras
"""
def encoding(word):
    res = ''
    
    for letter in list(word):
        if letter == ' ':
            res += letter
            continue
    
        for key in encoding_dictionary:
            if letter in encoding_dictionary.get(key):
                res += key
                break
            
    return res

"""
Método utilizado para calcular la distancia entre dos palabras codificadas.
Es utilizado para dar una palabra favorable en caso de no encontrar la
original en el diccionario.
"""
def hamming_distance(a, b):
    distance = 0
  
    if len(a) > len(b):
        a, b = b, a
  
    for i, x in enumerate(a):
        if a[i] != b[i]:
            distance += 1

    distance += (len(b) - len(a))
      
    return distance

"""
Método utilizado para calcular la distancia entre dos palabras codificadas.
Es utilizado para dar una palabra favorable en caso de no encotrar la original
en el diccionario. Esta implementación ha sido sacada de la Wikipedia
"""
def levenshtein_distance(a, b):
  d = dict()
  
  for i in range(len(a) + 1):
     d[i] = dict()
     d[i][0] = i
     
  for i in range(len(b) + 1):
     d[0][i] = i
     
  for i in range(1, len(a) + 1):
     for j in range(1, len(b) + 1):
        d[i][j] = min(d[i][j - 1] + 1, d[i - 1][j] + 1, d[i - 1][j - 1] + (not a[i - 1] == b[j - 1]))
        
  return d[len(a)][len(b)]

"""
Método utilizado para dividir el texto en n letras separadas.
Ejemplo: hola -> h o l a
"""    
def wrap(s, w):
    return textwrap.fill(s, w)

"""
Método utilizado para aplicar estadística a los distintos items, es decir,
este método nos calcula la probabilidad de las palabras/letras en base al total de ellas.
"""
def apply_statistics(items, total):
    for a in items:
        for b in items[a]:
            items[a][b] = items[a][b] / total

"""
En esta sección abrimos el fichero como lectura y con codificación utf8 para así tratar tildes, etc.
Además, sacamos todas las palabras y letras del corpus y realizamos el conteo de las mismas.
"""
with open(path, "r", encoding="utf8") as file:

    for line in file.readlines():
      
        line = re.sub('[^A-Za-z\u00C0-\u017F]+', ' ', line)
        line = re.sub('[\s]+', ' ', line)
          
        for word in map(lambda x: x.strip().lower(), line.split(' ')):
            
            encoding_word = encoding(word)
            
            if encoding_word in words:
                if word in words[encoding_word]:
                    words[encoding_word][word] += 1
                else:
                    words[encoding_word].update({word: 1})
            else:
                words[encoding_word] = dict()
                words[encoding_word].update({word:  1})
          
            total_words += 1
          
            for letter in list(word):
                
                encoding_letter = encoding(letter)
                
                if encoding_letter in letters:
                    if letter in letters[encoding_letter]:
                        letters[encoding_letter][letter] += 1
                    else:
                        letters[encoding_letter].update({letter: 1})
                else:
                    letters[encoding_letter] = dict()
                    letters[encoding_letter].update({letter: 1})
              
                total_letters += 1
                
"""
Método que aplica estadística a todos los items
"""
apply_statistics(words, total_words)
apply_statistics(letters, total_letters)

"""
En esta sección abrimos el fichero como lectura y con codificación utf8 para así tratar tildes, etc.
Además, sacamos todas las palabras y letras del corpus y realizamos el conteo de las mismas para obtener así el bigram.
"""

with open(path, "r", encoding="utf8") as file2:
    
    corpus = ''
    
    for line in file2.readlines():
      
        line = re.sub('[^A-Za-z\u00C0-\u017F]+', ' ', line)
        line = re.sub('[\s]+', ' ', line)
        corpus += line
    
    #Pongo todo el corpus en minúsculas
    corpus = corpus.lower()
    
    # Genero una lista donde añado el par de palabras
    line_list = list()
    line_list.append(corpus)
    
    # Genero una lista donde añado el par de letras
    line_letters_list = list()
    line_letters_list.append(wrap(corpus, 1))
        
    # Genero el par de palabras (bigram) con listas de compresión
    bigrams = [b for l in line_list for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
    words_pair = Counter(bigrams)
    
     # Genero el par de letras (bigram) con listas de compresión
    bigrams_letters = [b for l in line_letters_list for b in zip(l.split("\n")[:-1], l.split("\n")[1:])]
    letters_pair = Counter(bigrams_letters)
    
    # Contador de palabras y letras totales para estudiar la probabilidad
    total_words_pair = dict()
    total_letters_pair = dict()
    
    """
    Obtenemos los totales de las palabras y letras encontradas para realizar
    la estadística condicionada
    """
    for key in words_pair:        
        if key[0] in total_words_pair:
            total_words_pair[key[0]] += words_pair[key]
        else:
            total_words_pair[key[0]] = words_pair[key]
    
    for key in letters_pair:
        if key[0] in total_letters_pair:
            total_letters_pair[key[0]] += letters_pair[key]
        else:
            total_letters_pair[key[0]] = letters_pair[key]
    
    # Nuevo diccionario para limpiar el proceso de salida (palabras/letras)
    clean_dictionary_words = dict()
    clean_dictionary_letters = dict()
    
    # Añado la probabilidad correspondiente a cada par de palabras
    for k in words_pair:
      
        if k[0] not in clean_dictionary_words:
            clean_dictionary_words[k[0]] = dict()
        
        encoding_word = encoding(k[1])
        
        if encoding_word not in clean_dictionary_words[k[0]]:
            clean_dictionary_words[k[0]][encoding_word] = dict()
        
        clean_dictionary_words[k[0]][encoding_word].update({
            k[1]: words_pair[k] / total_words_pair[k[0]]
        })
        
    # Añado la probabilidad correspondiente a cada par de letras
    for k in letters_pair:
        
        if k[0] not in clean_dictionary_letters:
            clean_dictionary_letters[k[0]] = dict()
        
        encoding_letter = encoding(k[1])
        
        if encoding_letter not in clean_dictionary_letters[k[0]]:
            clean_dictionary_letters[k[0]][encoding_letter] = dict()
        
        clean_dictionary_letters[k[0]][encoding_letter].update({
            k[1]: letters_pair[k] / total_letters_pair[k[0]]
        })
        
    #Actualizo las variables correspondientes a los diccionarios de letras y palabras después de la limpieza
    words_pair = clean_dictionary_words
    letters_pair = clean_dictionary_letters

"""      
Método para obtener una palabra similar a una dada, en caso de que no se
en el diccionario
"""
def similar_word(code):
    
    res = ''
    min_distance = sys.maxsize
  
    for key, values in words.items():
        
        distance = levenshtein_distance(code, key)
        
        if distance < min_distance:
            # Cogemos la primera palabra que haya
            res = next(iter(words[key]))
            min_distance = distance
  
    return res

"""
Método unigram_letters usado para proporcionar predicciones de letras 
en base a una cadena de números separados por espacio
"""
def unigram_letters(code):
    
    res = ''
    
    for num in list(code):
        
        max_prob = 0
        letter_max_prob = ''
        
        if num in letters:
            
            for key in letters[num]:
                
                prob = letters[num][key]
                
                """
                Compruebo que la probabilidad sea más alta que la anterior.
                Sí es más alta obtengo su probabilidad y la letra a la que se corresponde.
                """
                if prob > max_prob:
                    max_prob = prob
                    letter_max_prob = key
            
            # Almaceno la letra más probable en la variable res
            res += letter_max_prob + ' '
    
    # Devolvemos el valor encontrado limpiando los espacios iniciales y finales
    return res.strip()

"""
Método unigram_words usado para proporcionar predicciones de palabras 
en base a una cadena de números separados por espacio
"""
def unigram_words(code):
    
    res = ''
    
    for num in code.split(' '):
        
        max_prob = 0
        word_max_prob = ''
        
        if num in words:
        
            for key in words[num]:
                
                prob = words[num][key]
                
                """
                Compruebo que la probabilidad sea más alta que la anterior.
                Sí es más alta obtengo su probabilidad y la palabra a la que se corresponde.
                """
                if prob > max_prob:
                    max_prob = prob
                    word_max_prob = key
                
        if word_max_prob == '':
            res += similar_word(num) + ' '
        else:
            # Almaceno la letra más probable en la variable res
            res += word_max_prob + ' '
            
    # Devolvemos el valor encontrado limpiando los espacios iniciales y finales
    return res.strip()

"""
Método bigram_words_base usado para proporcionar predicciones de palabras
en base a una cadena de números separadas por espacio teniendo en cuenta la
palabra anteriormente predicha.
"""
def bigram_words_base(last_word, code):
    
    max_prob_word = ''
    max_prob = 0
  
    if last_word in words_pair:
        
        if code in words_pair[last_word]:
            
            for key in words_pair[last_word][code]:
            
                prob = words_pair[last_word][code][key]
            
                """
                Compruebo que la probabilidad sea más alta que la anterior.
                Sí es más alta obtengo su probabilidad y la palabra a la que se corresponde.
                """
                if prob > max_prob:
                    max_prob = prob
                    max_prob_word = key
            
        else:
            return similar_word(code)

    else:
        return similar_word(code)
      
    if max_prob_word == '':
        max_prob_word = similar_word(code)
  
    # Devolvemos el valor encontrado limpiando los espacios iniciales y finales
    return max_prob_word.strip()

"""
Método de invocación inicial del método bigram_words, usado para predeccir
la primera palabra, ya que esta no tiene una referencia anterior.
"""
def bigram_words(code):
    
    res = ''
    last_word = ''
  
    for index, numBlock in enumerate(code.split(' ')):
        
      if index == 0:
        word = unigram_words(numBlock)
        res += word
        last_word = word
      else:
        word = bigram_words_base(last_word, numBlock)
        res += word
        last_word = word
        
      res += ' '

    # Devolvemos el valor encontrado limpiando los espacios iniciales y finales
    return res.strip()

"""
Método bigram_letters_base usado para proporcionar predcciones de letras
en base a un número teniendo en cuenta la letra anteriormente predicha.
"""
def bigram_letters_base(last_letter, code):
    
    max_prob_letter = ''
    max_prob = 0
  
    if last_letter in letters_pair:
        
        if code in letters_pair[last_letter]:
            
            for key in letters_pair[last_letter][code]:
            
                prob = letters_pair[last_letter][code][key]
            
                """
                Compruebo que la probabilidad sea más alta que la anterior.
                Sí es más alta obtengo su probabilidad y la letra a la que se corresponde.
                """
                if prob > max_prob:
                    max_prob = prob
                    max_prob_letter = key
            
        else:
            return similar_word(code)

    else:
        return similar_word(code)
      
    if max_prob_letter == '':
        max_prob_letter = similar_word(code)
  
    # Devolvemos el valor encontrado limpiando los espacios iniciales y finales
    return max_prob_letter.strip()

"""
Método de invocación inicial del método bigram_letters, usado para predeccir
la primera letra, ya que esta no tiene una referencia anterior.
"""
def bigram_letters(code):
    
    res = ''
    last_letter = ''
  
    for index, numBlock in enumerate(code):
        if index == 0:
            letter = unigram_letters(numBlock)
            res += letter
            last_letter = letter
        else:
            letter = bigram_letters_base(last_letter, numBlock)
            res += letter
            last_letter = letter
      
        res += ' '
    
    return res.strip()

# TESTING  
print("************************** TESTING ******************************")
print("Texto: Hola -> Predicción: " + unigram_letters('3 5 4 1'));
print("Texto: Hola -> Predicción: " + unigram_words('3541'));
print("Texto: Hola que tal estas -> Predicción: " + unigram_words('3541 672 714 26716'));
print("Texto: Tengo mucho miedo -> Predicción: " + unigram_words('72535 57135 53225'));

# Tiempo de ejecución obtenido
print("Tiempo de ejecución en segundos: --- %s seconds ---" % (time.time() - start_time))

"""
Definición de la ventana de testing, se llama a este método cuando
queremos arrancar esta vista
"""
def startTestingFrame():
    
    def show_unigram_letters():
      
        e3.delete(0, tk.END)
        e2.delete(0, tk.END)
        
        e2.insert(10, encoding(e1.get()))
        res = unigram_letters(e2.get())
        e3.insert(10, res)
       
    def show_unigram_words():
      
        e3.delete(0, tk.END)
        e2.delete(0, tk.END)
        
        e2.insert(0, encoding(e1.get()))
        res = unigram_words(e2.get())
        e3.insert(0, res)
        
    def show_bigram_words():
    
        e3.delete(0, tk.END)
        e2.delete(0, tk.END)
      
        e2.insert(0, encoding(e1.get()))
        res = bigram_words(e2.get())
        e3.insert(0, res)
      
    def show_bigram_letters():
      
        e3.delete(0, tk.END)
        e2.delete(0, tk.END)
      
        e2.insert(0, encoding(e1.get()))
        res = bigram_letters(e2.get())
        e3.insert(0, res)
    
    testingFrame = tk.Tk()
    testingFrame.title("N-grams - Texto Predictivo (Testing)")
    testingFrame.minsize(width = 465, height = 140)
    
    tk.Label(testingFrame, text = "Texto").grid(row = 0)
    tk.Label(testingFrame, text = "Entrada").grid(row = 1)
    tk.Label(testingFrame, text = "Predicción").grid(row = 3)
    
    e1 = tk.Entry(testingFrame, width = 35)
    e2 = tk.Entry(testingFrame, width = 35)
    e3 = tk.Entry(testingFrame, width = 35)
    
    e1.insert(0, "soy bueno")
    
    e1.grid(row = 0, column = 1)
    e2.grid(row = 1, column = 1)
    e3.grid(row = 3, column = 1)
    
    tk.Button(testingFrame, text='Unigram letras', command = show_unigram_letters, width = 30, padx = 2, pady = 2).grid(row = 6, column = 0, sticky = tk.W, pady = 5, padx = 5)
    tk.Button(testingFrame, text='Unigram palabras', command = show_unigram_words, width = 30, padx = 2, pady = 2).grid(row = 6, column = 1, sticky = tk.W, pady = 5, padx = 5)  
    tk.Button(testingFrame, text='Bigram letras', command = show_bigram_letters, width = 30, padx = 2, pady = 2).grid(row = 7, column = 0, sticky = tk.W, pady = 5, padx = 5)
    tk.Button(testingFrame, text='Bigram palabras', command = show_bigram_words, width = 30, padx = 2, pady = 2).grid(row = 7, column = 1, sticky = tk.W, pady = 5, padx = 5)
    
    testingFrame.mainloop()

"""
Definición de la ventana de la aplicación, se llama a este método cuando
queremos arrancar esta vista
"""
def startApplicationFrame():
    
    def button_pressed(code):
  
      previous = e5.get()
      code = previous + code
      
      e5.delete(0, tk.END)
      e5.insert(0, code)
      
      update_unigram_letters_input(code)
      update_unigram_words_input(code)
      update_bigram_letters_input(code)
      update_bigram_words_input(code)
      
    def update_unigram_letters_input(code):
      e1.delete(0, tk.END)
      e1.insert(0, unigram_letters(code))
      
    def update_unigram_words_input(code):
      e2.delete(0, tk.END)
      e2.insert(0, unigram_words(code))
      
    def update_bigram_letters_input(code):
      e3.delete(0, tk.END)
      e3.insert(0, bigram_letters(code))
      
    def update_bigram_words_input(code):
      e4.delete(0, tk.END)
      e4.insert(0, bigram_words(code))
    
    guiFrame = tk.Tk()
    guiFrame.title('N-grams - Texto Predictivo (Aplicación)')
    guiFrame.minsize(width = 535, height = 220)
    
    tk.Label(guiFrame, text = "Unigram letras", padx = 2, pady = 2).grid(row = 0, column = 0, padx = 10)
    e1 = tk.Entry(guiFrame, width = 50)
    e1.grid(row = 1, column = 0, padx = 10)
    
    tk.Label(guiFrame, text = "Unigram palabras", padx = 2, pady = 2).grid(row = 2, column = 0, padx = 10)
    e2 = tk.Entry(guiFrame, width = 50)
    e2.grid(row = 3, column = 0, padx = 10)
    
    tk.Label(guiFrame, text = "Bigram letras", padx = 2, pady = 2).grid(row = 4, column = 0, padx = 10)
    e3 = tk.Entry(guiFrame, width = 50)
    e3.grid(row = 5, column = 0, padx = 10)
    
    tk.Label(guiFrame, text = "Bigram palabras", padx = 2, pady = 2).grid(row = 6, column = 0, padx = 10)
    e4 = tk.Entry(guiFrame, width = 50)
    e4.grid(row = 7, column = 0, padx = 10)
    
    tk.Button(guiFrame, text = 'a b c', command = lambda : button_pressed('1'), width = 7, padx = 2, pady = 2).grid(row = 1, column = 1)
    tk.Button(guiFrame, text = 'd e f', command = lambda : button_pressed('2'), width = 7, padx = 2, pady = 2).grid(row = 1, column = 2)
    tk.Button(guiFrame, text = 'g h i', command = lambda : button_pressed('3'), width = 7, padx = 2, pady = 2).grid(row = 1, column = 3)
    tk.Button(guiFrame, text = 'j k l', command = lambda : button_pressed('4'), width = 7, padx = 2, pady = 2).grid(row = 2, column = 1)
    tk.Button(guiFrame, text = 'espacio', command = lambda : button_pressed(' '), width = 7, padx = 2, pady = 2).grid(row = 2, column = 2)
    tk.Button(guiFrame, text = 'm n ñ o', command = lambda : button_pressed('5'), width = 7, padx = 2, pady = 2).grid(row = 2, column = 3)
    tk.Button(guiFrame, text = 'p q r s', command = lambda : button_pressed('6'), width = 7, padx = 2, pady = 2).grid(row = 3, column = 1)
    tk.Button(guiFrame, text = 't u v', command = lambda : button_pressed('7'), width = 7, padx = 2, pady = 2).grid(row = 3, column = 2)
    tk.Button(guiFrame, text = 'w x y z', command = lambda : button_pressed('8'), width = 7, padx = 2, pady = 2).grid(row = 3, column = 3)
    
    tk.Label(guiFrame, text = "Entrada", width = 21, padx = 2, pady = 2).grid(row = 5, column = 1, columnspan = 3)
    e5 = tk.Entry(guiFrame, width = 33)
    e5.grid(row = 6, column = 1, columnspan = 3)
    
    tk.Button(guiFrame, text = 'limpiar', command = lambda : e5.delete(0, tk.END), width = 7, padx = 2, pady = 2).grid(row = 7, column = 1, columnspan = 3)
    
    guiFrame.mainloop()
    
"""
Definición de la ventana del cuento, se llama a este método cuando
queremos arrancar esta vista
"""
def startTaleFrame():
    
    max_len_tale = 400
    
    def get_random_word():
        
        index = random.randint(0, len(words_pair) - 1)
        return [key for (i, key) in enumerate(words_pair) if i == index][0]
    
    def bigram_word_max_prob(last_word):
              
        if last_word not in words_pair:
            return get_random_word()
        
        max_prob_word = ''
        roulette = random.uniform(0, 1)
        count = 0
      
        """
        En esta parte del código se realiza una pequeña ruleta, obteniendo una palabra aleatoria
        pero no de forma caótica, este ruleta le da más peso a la palabra con mayor probabilidad.
        """
        for code in words_pair[last_word]:
            
            for word in words_pair[last_word][code]:
                
                count += words_pair[last_word][code][word]
                
                if count >= roulette:
                    max_prob_word = word
                    break
                
            if max_prob_word != '':
                break
          
        if max_prob_word == '':
            return get_random_word()
      
        return max_prob_word.strip()
        
      
    def bigram_words_tale():
        
      e1.delete(1.0, tk.END)
      last_word = get_random_word()
      text =  last_word + ' '
      
      while len(text) <= max_len_tale:
          
          last_word = bigram_word_max_prob(last_word)
          text += last_word + ' '
      
      e1.insert(tk.INSERT, text)
    
    taleFrame = tk.Tk()
    taleFrame.title('N-grams - Texto Predictivo (Cuento)')
    taleFrame.minsize(width = 660, height = 220)
    
    e1 = tk.Text(taleFrame)
    e1.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    
    tk.Button(taleFrame, text='Cuéntame un cuento (Bigram)', command = bigram_words_tale, width = 30, padx = 2, pady = 2).grid(row = 1, column = 0, columnspan = 2, pady = 5, padx = 5)
    
    taleFrame.mainloop()

root = tk.Tk()
root.title('N-grams - Texto Predictivo (Menú)')
root.minsize(width = 410, height = 50)
tk.Button(root, text = 'Testing', command = lambda : startTestingFrame(), width = 15, padx = 2, pady = 2).grid(row = 0, column = 0, padx = 10, pady = 10)
tk.Button(root, text = 'Aplicación', command = lambda : startApplicationFrame(), width = 15, padx = 2, pady = 2).grid(row = 0, column = 1, padx = 10, pady = 10)
tk.Button(root, text = 'Cuento', command = lambda : startTaleFrame(), width = 15, padx = 2, pady = 2).grid(row = 0, column = 2, padx = 10, pady = 10)
root.mainloop()
