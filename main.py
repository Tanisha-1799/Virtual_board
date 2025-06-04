import os
import cv2
from cvzone.HandTrackingModule import HandDetector


#variables for camera dimension
width, height = 900, 720
folderPath="Image_keeper"

#Camera setup
cap =cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

#Get the list of images
boards = os.listdir(folderPath)
#If you want to sort it based onn length if there are more than 10 pages then use the below expression
#boards=sorted(os.listdir(folderPath), key=len)

print(boards)

#variables
num=0
ws, hs =400, 200

#Hand detector code
detector=HandDetector(detectionCon=0.8, maxHands=1)


while True:
    # Importing the images
    success, img=cap.read()
    #Since image is a mirror one so need to flip the image
    img = cv2.flip(img,1)   # 1:Horizontal, 0:Vertical

    #extracting images from folder
    board=os.path.join(folderPath,boards[num])
    currentBoard=cv2.imread(board)

    hands, img=detector.findHands(img,flipType=False)


    # Resize webcam image and board size
    # since the size of the image is too large so adjusting it to the screen resolution
    currentBoard=cv2.resize(currentBoard,(1360,760))
    smallImage = cv2.resize(img, (ws, hs))
    # Overlay webcam image in top-right corner
    h, w, _ = currentBoard.shape
    if h >= hs and w >= ws:
        currentBoard[0:hs, w - ws:w] = smallImage

    cv2.imshow("Image",img)
    cv2.imshow("Board",currentBoard)

    key=cv2.waitKey(1) ##for some delay
    if key == ord('q'):    ##to quit the camera when "q" is pressed
        break