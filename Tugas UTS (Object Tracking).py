#mengimport library yang digunakan

import cv2
import numpy as np
import imutils

# pendefinisian fungsi "nothing" untuk melengkapi parameter di Trackbar
def nothing(x):
    pass

#tools pengambilan video dari kamera
cap = cv2.VideoCapture(0)

# pembuatan Jendela Trackbars
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 161, 180, nothing)
cv2.createTrackbar("L-S", "Trackbars", 78, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 148, 155, nothing)
cv2.createTrackbar("U-H", "Trackbars", 180, 180, nothing)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 255, 255, nothing)

# resolusi kamera yang digunakan
cap.set(4, 640)
cap.set(3, 480)

#pembuatan jendela per frame
while True:
    _, frame = cap.read()
    # transfer warna rgb ke hsv dari kamera
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # inisialisasi dari hasil nilai Trackbars
    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")
    # inisialisasi untuk batas atas dan bawah
    lower_color = np.array([l_h, l_s, l_v])
    upper_color = np.array([u_h, u_s, u_v])

    # pembuatan jendela mask untuk menampilkan hasil dari penentuan HSV
    mask = cv2.inRange(hsv, lower_color, upper_color)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    # pendeteksian area menggunakan cv2.findContours
    cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        area = cv2.contourArea(c)
        if area > 500:

            cv2.drawContours(frame, [c], -1, (0, 255, 200), 3)

            M = cv2.moments(c)
            # penentua dimensi titik tengah (center)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
            cv2.putText(frame, "Centre", (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            print("area is ....", area)
            print("centroid is at...", cx, cy)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()