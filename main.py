import cv2

#variables for camera dimension
width, height = 1280, 720

#Camera setup
cap =cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

while True:
    success, img=cap.read()
    cv2.imshow("Image",img)
    key=cv2.waitKey(1) ##for some delay
    if key == ord('q'):    ##to quit the camera when "q" is pressed
        break