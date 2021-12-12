import numpy as np
import cv2 
import time
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVIB')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
time.sleep(2)
bg = 0
for i in range(60):
    ret,bg = cap.read()
    print(bg)

bg = np.flip(bg,axis= 1)
while(cap.isOpened()):
    ret,ing = cap.read()
    if not ret:
        break
    ing = np.flip(ing,axis= 1)
    hsv = cv2.cvtColor(ing, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,120,50])
    upper_red = np.array([10,255,255])
    mask_1 = cv2.inRange(hsv,lower_red,upper_red)

    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask_2 = cv2.inRange(hsv, lower_red, upper_red)
    mask_1 = mask_1 + mask_2
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))

    mask_2 = cv2.bitwise_not(mask_1)

    res_1 = cv2.bitwise_and(ing,ing,mask = mask_2)
    res_2 = cv2.bitwise_and(bg,bg,mask = mask_1)

    final_output = cv2.addWeighted(res_1, 1, res_2, 1 , 0 )
    output_file.write(final_output)

    cv2.imshow('magic masking', final_output)
    cv2.waitKey(1)

cap.release()
output_file.release()
cv2.destroyAllWindows()
