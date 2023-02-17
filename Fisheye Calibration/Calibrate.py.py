import cv2 as cv
import numpy as np
import os
import glob

# Satranç tahtamızın boyutları.
CHECKERBOARD = (10, 7)
size = (1376, 917)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 3D Noktları
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

count=0
objpoints = []

imgpoints = []

# Dosyamızda önceden çektiğimiz resimleri bir değişkene atıyoruz 
images = glob.glob('*.png')      # sizin fotoğraflarınız ( dosya içine çektiğiniz fotoğrafları atmanız yeterli )
print("Debu1")  # Debug
for image in images:
    count+=1
    print("Kalibre ediliyor")
    print(count)
    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    ret, corners = cv.findChessboardCorners(gray, CHECKERBOARD, None)

    
    if ret == True:
        objpoints.append(objp)
        # Map köşelerinin 2 boyutlu tespiti
        corners2 = cv.cornerSubPix(gray, corners, (10, 7), (-1, -1), criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        cv.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)

    cv.imshow('img', img)
    cv.waitKey(10)

cv.destroyAllWindows()


ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, size, None, None)

print("\n Kalibre edildi.", ret)
print("\nCamera matrix:\n", mtx)
print("\ndist:\n", dist)
print("\nrotation vector : \n", rvecs)
print("\n translation vector : \n", tvecs)


img = cv.imread('foto28.png')         # fotoğraflarınızın birinin adı 
h,  w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))


dst = cv.undistort(img, mtx, dist, None, newcameramtx)
x, y, w, h = roi
dst = dst[x:y+h, x:x+w]


capt=cv.VideoCapture("rtsp://192.168.1.10:554/user=admin&password=EXLXEXKX&channel=1&stream=0.sdp")  # your rtsp url or 0 

num=0

while capt.isOpened():

    succes1, img = capt.read()

    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)
    x, y, w, h = roi
    dst = dst[x:y+h, x:x+w]   # Düzgün görüntü dışında kalan ama işimize yine de yarayan görüntüleri kurtarıyoruz.
    k = cv.waitKey(1)

    if k == 27:
        break
   
    cv.imshow('Img 1',dst)