# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 11:05:39 2018

@author: wstro
"""

from PIL import ImageTk, Image, ImageDraw
import PIL
from tkinter import *
import os, sys
import win32api
from random import randrange

import tensorflow as tf



game_name = "The Best"
canvas_width = 500
canvas_height = 500
center = canvas_height//2
white = (255, 255, 255)
green = (0,128,0)
forma = ""
    

def tensor(nome):
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# change this as you see fit
    #image_path = sys.argv[1]
    
    # Read in the image_data
    image_data = tf.gfile.FastGFile(nome, 'rb').read()
    
    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line 
                       in tf.gfile.GFile("retrained_labels.txt")]
    
    # Unpersists graph from file
    with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')
    
    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        
        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})
        
        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            print('%s (score = %.5f)' % (human_string, score))
        if(label_lines[0] == forma):
            win32api.MessageBox(0, "Parabens ", game_name, 0x00001000)
        else:
            win32api.MessageBox(0, "Tente Novamente", game_name, 0x00001000) 
        clean()
            
def start():
    opcao = randrange(1, 3)
    if(opcao == 1):
        forma = "Quadrado"
    elif(opcao == 2):
        forma  = "Triangulo"
    else :
        forma = "Circulo"
    win32api.MessageBox(0, "Desenhe um %s " % (forma), game_name, 0x00001000) 
    
def save():
    filename = "image.jpg"
    image1.save(filename)
    tensor(filename)
   
def clean():
    #print("testando")
    cv.create_rectangle(0,0, canvas_width+10, canvas_height+10, fill="white")
    start()

    
def paint(event):
    # python_green = "#476042"
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    cv.create_oval(x1, y1, x2, y2, fill="black",width=5)
    #draw.line([x1, y1, x2, y2],fill="black",width=5)

root = Tk()

# Tkinter create a canvas to draw on
cv = Canvas(root, width=canvas_width, height=canvas_height, bg='white')
root.title(game_name)
cv.pack()
start()


# PIL create an empty image and draw object to draw on
# memory only, not visible
image1 = PIL.Image.new("RGB", (canvas_width, canvas_height), white)
draw = ImageDraw.Draw(image1)

# do the Tkinter canvas drawings (visible)
# cv.create_line([0, center, width, center], fill='green')

cv.pack(expand=YES, fill=BOTH)
cv.bind("<B1-Motion>", paint)

# do the PIL image/draw (in memory) drawings
# draw.line([0, center, width, center], green)

# PIL image can be saved as .png .jpg .gif or .bmp file (among others)
#filename = "my_drawing.png"
#image1.save(filename)
button=Button(text="save",command=save)
button2=Button(text="clean",command=clean)
button.pack()
button2.pack()
root.mainloop()

