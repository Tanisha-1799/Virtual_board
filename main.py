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
gestureThreshold=300
buttonPressed = False
buttonCounter=0
buttonDelay=30

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

    hands, img=detector.findHands(img)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx,cy = hand['center']
        #accessing lmlist that is landmark list is basically the hand dictionary
        lmList = hand['lmList']
        #we will get 8 point that is the index finger
        indexFinger = lmList[8][0], lmList[8][1]

        #print(fingers)

        #if hand is at the height of the face then we are going to take that gesture
        if cy<=gestureThreshold :
            # Gesture 1 - left
            if fingers == [1,0,0,0,0]: # fingers:[thumb,fin1,fin2,fin3,fin4]
                print("Left")

                if num >0:
                    buttonPressed = True
                    num -= 1

            # Gesture 2 - Right
            if fingers == [0, 0, 0, 0, 1]:  # fingers:[thumb,fin1,fin2,fin3,fin4]
                print("Right")

                if num < len(boards)-1:
                    buttonPressed = True
                    num += 1

        # Gesture 3 - Show Pointer
        if fingers == [0, 1, 1, 0, 0]:
            #Adding a pointer at the tip of the index finger using gesture
            cv2.circle(currentBoard, indexFinger, 12, (0, 0, 255), cv2.FILLED)

    #Button Pressed iterations
    if buttonPressed:
        buttonCounter +=1
        if buttonCounter > buttonDelay :
            buttonPressed =False




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