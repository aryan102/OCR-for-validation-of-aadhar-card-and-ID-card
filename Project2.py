import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def display(img,cmap='gray'):
    fig = plt.figure(figsize=(12,10))
    ax = fig.add_subplot(111)
    ax.imshow(img,cmap='gray')
    plt.show()
img = cv2.imread("ID1.jpg")
plt.imshow(img)
plt.show()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
display(gray)
th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
display(threshed)

text1 = pytesseract.image_to_data(threshed, lang="eng",output_type='data.frame')
n_boxes = len(text1['text'])
for i in range(n_boxes):
    if int(text1['conf'][i]) > 60:
        (x, y, w, h) = (text1['left'][i], text1['top'][i], text1['width'][i], text1['height'][i])
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
display(img)

text2 = pytesseract.image_to_string(threshed, lang="eng")
print(text2)

text = text1[text1.conf > 80]
lines = text.groupby('block_num')['text'].apply(list)
conf = text.groupby(['block_num'])['conf'].mean()
pd.set_option('max_columns', None)
pd.set_option('display.max_rows', text.shape[0]+1)
print("text1 : \n")
print(text1,"\n\n")

print("text : \n")
print(text, "\n\n")
  
print("lines : \n")
for i in range(len(lines)) :
    print("level", i, ": ", lines.iloc[i])

print("\n\n conf : \n")
print(conf)

from pytesseract import Output
img = cv2.imread('ac_test.jpg')
d = pytesseract.image_to_data(img, output_type=Output.DICT)
print(d.keys())

print(text)
i=len(lines)-3
name=""
for j in range(len(lines[i])) :
    if(lines[i][j] == 'ID') :
        break  
    if(j!=0) :
        name=name+" "
    name=name+lines[i][j]

print ("Name of student : ",name)
import csv
import re
flag=0
with open("Student.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        if(row[0]==name) :
            print("The Student is verified")
            flag=1
            break

if flag==0:
    print("The Student is not verified")
