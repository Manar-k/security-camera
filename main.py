import urllib.request
import cv2
import numpy as np
import winsound

# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
URL = "http://192.168.43.5/shot.jpg"
# While loop to fetch data from the Url.
while True:
    img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img_arr2 = np.array(bytearray(urllib.request.urlopen(URL).read()), dtype=np.uint8)
    img2 = cv2.imdecode(img_arr2, -1)
    # a function which helps in finding the absolute difference between the pixels of the two image arrays.
    diff = cv2.absdiff(img, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    # Image Smoothing techniques help in reducing the noise.
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    # this allows us to sort our contours according to their area (i.e. size) from largest to smallest (Line 70).
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        winsound.Beep(500, 450)
    q = cv2.waitKey(1)
    # Press q key to exit
    if q == ord("q"):
        break;
    cv2.imshow('IPWebcam', img)
cv2.destroyAllWindows()
