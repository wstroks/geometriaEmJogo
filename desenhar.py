# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 11:05:39 2018

@author: wstro
"""

from PIL import ImageTk, Image, ImageDraw
import PIL
from tkinter import *
import os, sys

import tensorflow as tf



width = 500
height = 500
center = height//2
white = (255, 255, 255)
green = (0,128,0)

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
            
 
def save():
    filename = "image.jpg"
    image1.save(filename)
    tensor(filename)
   
    

def paint(event):
    # python_green = "#476042"
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    cv.create_oval(x1, y1, x2, y2, fill="black",width=5)
    draw.line([x1, y1, x2, y2],fill="black",width=5)

root = Tk()

# Tkinter create a canvas to draw on
cv = Canvas(root, width=width, height=height, bg='white')
cv.pack()

# PIL create an empty image and draw object to draw on
# memory only, not visible
image1 = PIL.Image.new("RGB", (width, height), white)
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
button.pack()
root.mainloop()
