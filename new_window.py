# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 16:32:34 2018

@author: Pozas91
"""

def button_pressed(code):
  
  previous = e5.get()
  code = previous + code
  
  e5.delete(0, END)
  e5.insert(0, code)
  
  update_unigram_letters_input(code)
  update_unigram_words_input(code)
  update_bigram_letters_input(code)
  update_bigram_words_input(code)
  
def update_unigram_letters_input(code):
  e1.delete(0, END)
  e1.insert(0, unigram_letras(code))
  
def update_unigram_words_input(code):
  e2.delete(0, END)
  e2.insert(0, unigram_palabras(code))
  
def update_bigram_letters_input(code):
  e3.delete(0, END)
  e3.insert(0, bigram_letters(code))
  
def update_bigram_words_input(code):
  e4.delete(0, END)
  e4.insert(0, bigram_words(code))

gui = Tk()
gui.title('N-grams - Texto Predictivo (Aplicación)')
gui.minsize(width = 535, height = 220)

Label(gui, text = "Unigram letras", padx = 2, pady = 2).grid(row = 0, column = 0, padx = 10)
e1 = Entry(gui, width = 50)
e1.grid(row = 1, column = 0, padx = 10)

Label(gui, text = "Unigram palabras", padx = 2, pady = 2).grid(row = 2, column = 0, padx = 10)
e2 = Entry(gui, width = 50)
e2.grid(row = 3, column = 0, padx = 10)

Label(gui, text = "Bigram letras", padx = 2, pady = 2).grid(row = 4, column = 0, padx = 10)
e3 = Entry(gui, width = 50)
e3.grid(row = 5, column = 0, padx = 10)

Label(gui, text = "Bigram palabras", padx = 2, pady = 2).grid(row = 6, column = 0, padx = 10)
e4 = Entry(gui, width = 50)
e4.grid(row = 7, column = 0, padx = 10)

Button(gui, text = 'a b c', command = lambda : button_pressed('1'), width = 7, padx = 2, pady = 2).grid(row = 1, column = 1)
Button(gui, text = 'd e f', command = lambda : button_pressed('2'), width = 7, padx = 2, pady = 2).grid(row = 1, column = 2)
Button(gui, text = 'g h i', command = lambda : button_pressed('3'), width = 7, padx = 2, pady = 2).grid(row = 1, column = 3)
Button(gui, text = 'j k l', command = lambda : button_pressed('4'), width = 7, padx = 2, pady = 2).grid(row = 2, column = 1)
Button(gui, text = 'espacio', command = lambda : button_pressed(' '), width = 7, padx = 2, pady = 2).grid(row = 2, column = 2)
Button(gui, text = 'm n ñ o', command = lambda : button_pressed('5'), width = 7, padx = 2, pady = 2).grid(row = 2, column = 3)
Button(gui, text = 'p q r s', command = lambda : button_pressed('6'), width = 7, padx = 2, pady = 2).grid(row = 3, column = 1)
Button(gui, text = 't u v', command = lambda : button_pressed('7'), width = 7, padx = 2, pady = 2).grid(row = 3, column = 2)
Button(gui, text = 'w x y z', command = lambda : button_pressed('8'), width = 7, padx = 2, pady = 2).grid(row = 3, column = 3)

Label(gui, text = "Entrada", width = 21, padx = 2, pady = 2).grid(row = 5, column = 1, columnspan = 3)
e5 = Entry(gui, width = 33)
e5.grid(row = 6, column = 1, columnspan = 3)

Button(gui, text = 'limpiar', command = lambda : e5.delete(0, END), width = 7, padx = 2, pady = 2).grid(row = 7, column = 1, columnspan = 3)