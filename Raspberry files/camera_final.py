# -*- coding: utf-8 -*-

import time
from time import sleep
import tflite_runtime.interpreter as tflite
import numpy as np
import cv2
from picamera import PiCamera
import tkinter as tk
from segDisplay import Display #importa classe display
from preprocessamento import Preprocessamento

#start = time.time()

root= tk.Tk()
display = Display() #define a classe Display na variável displays
processamento = Preprocessamento()

def takePicture():
  camera = PiCamera()
  print("foto tirada")
  camera.resolution = (1024, 768)
  camera.start_preview()
  camera.contrast = 10
  sleep(5)
  camera.capture("img.jpg")
  camera.stop_preview()
  camera.close()
  

def processar(path):
  print("processamento")
  img = processamento.processarImg(path)
  cv2.imwrite('resultado.jpg', img)
  return(img)
  
#def setImage(number):
def result(event):
    #if int(input.get()) < 10:
    #print("numero digitado: "+input.get())
    res.configure(text= "Resultado: " + ia(input.get()))
    #else:
     # res.configure(text= "Digite um numero menor que 10")
        
def ia():
    takePicture()
    image_teste = cv2.imread("img.jpg",cv2.IMREAD_GRAYSCALE)#importa a imagem na escala de cinzaa
    processar(image_teste)
    image = cv2.imread("resultado.jpg", cv2.IMREAD_GRAYSCALE)#importa a imagem na escala de cinzaa
    image = cv2.resize(image, (28,28)).astype("float32")#define o tipo da imagem pra float32
    img_expanded = np.expand_dims(image, axis=0)#expande para 3 dimensões 
    img_expanded2 = np.expand_dims(img_expanded, axis=img_expanded.ndim)#expande para 4 dimenções
    
    interpreter = tflite.Interpreter("model.tflite")#importa o modelo model.tflite
    interpreter.allocate_tensors()#aloca tensores para otimizar a inferencia

    input_details = interpreter.get_input_details() #retorna os detalhes de entrada
    output_details = interpreter.get_output_details() #retorna os detalhes de saida

    interpreter.set_tensor(input_details[0]["index"], img_expanded2)#define o interpretador para ler a imagem
    interpreter.invoke()#garante que as configurações foram confirmadas
    pred = interpreter.get_tensor(output_details[0]['index']) #retorna a predição da IA
    
    with open("labels.txt") as f:     #abre o arquivo com os números
        labels = f.read().splitlines()#a serem identificados

    i = int(np.argmax(pred))
    label = labels[i]#retorna o numero da predição

    display.numero(int(label))#mostra o numero no display
    return label

def init():
    ia()

#tk.Label(root, text="digite o numero a ser lido: ").grid(row=0)
#input = tk.Entry(root)
#input.bind("<Return>", result)
#input.grid(row=0, column=1)

tk.Button(root, text="tirar foto", command=init).grid(row=1, column=0)
res = tk.Label(root)
res.grid(row=3, column= 0)

root.mainloop()


#end = time.time()
#exec_time = (end-start) * 10**3


#print("O tempo de execução foi de :",
#      "%2.f" % exec_time, "ms")
