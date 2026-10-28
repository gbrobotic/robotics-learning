# ex_c01.py  —  Chapter 1: Python + NumPy for OpenCV
# Meri practice file. Run:  python3 ex_c01.py

import numpy as np   # numpy = arrays (har image ek numpy array hai)
import cv2           # opencv = image save/show karne ke liye


# ===== EASY: 100x200 black image, pixel (50,150) green =====
img = np.zeros((100, 200, 3), dtype=np.uint8)   # 100 rows (height), 200 cols (width), 3 colours (BGR), sab 0 = black
img[50, 150] = [0, 255, 0]                       # row pehle, phir column. BGR mein green beech mein
print(img.shape)          # (100, 200, 3)
print(img[50, 150])       # [  0 255   0]  -> green pixel
print(img[50, 149])       # [0 0 0]        -> padosi abhi bhi black


# ===== EXPERIMENTS: ":" means all, "a:b" means a se b-1 tak =====
img[:, 150] = [0, 255, 0]           # saari rows, column 150 -> vertical green line
img[10, :] = [255, 0, 0]            # row 10, saare columns -> horizontal blue line
img[40:60, 100:120] = [0, 0, 255]   # rows 40-59, cols 100-119 -> 20x20 red square
print(img[40:60, 100:120].shape)    # (20, 20, 3) -> block ka size
print(img[10, 150])                 # [255 0 0] -> blue, kyunki blue line baad mein bani (last write wins)
cv2.imwrite("test.png", img)        # image file save karo, phir kholke dekho: xdg-open test.png


# ===== MEDIUM: 5x5 array (0-24), middle 3x3 block = 0, ek slice line mein =====
arr = np.arange(25).reshape(5, 5)   # 0 se 24 tak numbers, 5x5 grid mein
arr[1:4, 1:4] = 0                   # rows 1,2,3 aur cols 1,2,3 (4 included nahi). Ek number poore block mein bhar jata hai = broadcasting
print(arr)


# ===== ROBOT TASK: areas 8000 se 40000 ke beech -> unka INDEX print karo =====
# Robot use: camera mein bahut blobs milte hain. Chhote = noise, bahut bade = floor/wall. Sirf sahi size wale rakho.
areas = [12, 18000, 400, 17600, 2300]

for i, a in enumerate(areas):       # enumerate = index aur value dono saath mein deta hai
    print(i, a)

for i, area in enumerate(areas):
    if 8000 < area < 40000:         # Python mein comparison chain kar sakte hain, maths jaisa
        print(i)                    # 1 aur 3

big = [i for i, area in enumerate(areas) if 8000 < area < 40000]   # same kaam, ek line mein (list comprehension)
print(big)                          # [1, 3]


# ===== MY MISTAKES =====
# img[150, 50] -> IndexError, kyunki sirf 100 rows hain (0-99). Row pehle aata hai!
# 300 in uint8 -> 44 ban gaya (300 - 256). Values 0-255 mein rakho
# print(img) -> pura bada array print hota hai aur numpy "..." se chhota kar deta hai.
#               Isliye sirf jo chahiye woh print karo: img[50, 150], img.shape
# Do lines ek pixel par cross karein -> jo line baad mein bani uska colour dikhega