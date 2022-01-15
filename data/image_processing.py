# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 23:27:19 2021

@author: Stevanus Darwin
"""
# TODO: 
# - extract constant path ke luar proses
# - masukin proses ke dalam fungsi
# - siapkan return
# - integrasi ke proyek utama

import cv2
import numpy as np
import random as rng
import time

# Tambahan dimulai di sini =============================================
import os
from datetime import datetime
import pytz
from .models import Result
from.constant import UPLOAD_FOLDER, RETRIEVE_FOLDER, OUTPUT_FOLDER


def process_image(filename):  

  # Tambahan berhenti di sini =============================================
  rng.seed(12345)

  start = time.time()
  print('Whitefly Detection Algorithm Starting...')

  img = cv2.imread(os.path.join(UPLOAD_FOLDER, filename)) #Path file gambar (folder/nama file)
  img_gs = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Ubah ke Grayscale

  #BinaryThreshold Parameter 190-225
  ret, th = cv2.threshold(img_gs,200,255,cv2.THRESH_BINARY_INV) 

  #Menghitung Objek setelah di threshold
  _, contours, _ = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
  contours_poly = [None]*len(contours)
  boundRect = [None]*len(contours)
  centers = [None]*len(contours)
  radius = [None]*len(contours)
  for i, c in enumerate(contours):
      contours_poly[i] = cv2.approxPolyDP(c, 3, True)
      boundRect[i] = cv2.boundingRect(contours_poly[i])
      centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])
      
      
  drawing = np.zeros((th.shape[0], th.shape[1], 3), dtype=np.uint8)
      
      
  for i in range(len(contours)):
          color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
          cv2.drawContours(drawing, contours_poly, i, color)
          cv2.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
            (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)

  #Gambar objek yang terdeteksi di gambar original
  num = len(contours)
  text = "Jumlah Whitefly: " + str(num-1)
  cv2.drawContours(img, contours, -1, (255, 0, 0), 2) #Gambar objek di gambar original
  cv2.putText(img, text, (20, 400), #Kasih Text Jumlah Whitefly
              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
  cv2.imwrite(os.path.join(RETRIEVE_FOLDER, filename),img) #Gambar di save di Path yang ditentukan

  print("Gambar telah disimpan di folder Output")
  end = time.time()
  print("Waktu Eksekusi: " + str(end-start) + " detik") #Print Waktu running
  #cv2.waitKey(5) #Tunggu 5 detik sebelum stop script

  # Tambahan dimulai di sini =============================================
  jumlah_whitefly = num-1
  #jumlah_thripps = ???
  #jumlah_lalatbuah = ???
  #jumlah_leafminer = ???
  
  
  total = 0

  total += jumlah_whitefly
  #total += jumlah_thripps
  #total += jumlah_lalatbuah
  #total += jumlah_leafminer

  result =  Result(
            image=os.path.join(OUTPUT_FOLDER, filename),
            total = total,
            uploaded_at = datetime.utcnow().astimezone(pytz.timezone("Asia/Jakarta")),
            whitefly = jumlah_whitefly #,
            #thripps = jumlah_thripps,
            #lalatbuah = jumlah_lalatbuah,
            #leafminer = jumlah_leafminer,
            #damage = ???
  )

  return result