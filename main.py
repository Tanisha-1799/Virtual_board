import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# Camera dimensions
width, height = 1280, 720
folderPath = "Image_keeper"

# Setup camera
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Load board images
boards = os.listdir(folderPath)
boards.sort()
print(boards)

# Parameters
num = 0
ws, hs = int(213 * 1), int(120 * 1)  # Small webcam window size
gestureThreshold = 700
buttonPressed = False
buttonCounter = 0
buttonDelay = 5

# For drawing
annotations = [[]]
annotationNumber = 0
annotationStart = False

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    board = os.path.join(folderPath, boards[num])
    currentBoard = cv2.imread(board)
    currentBoard = cv2.resize(
        currentBoard, (width, height))  # Match camera size

    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold),
             (width, gestureThreshold), (0, 255, 0), 10)

    if hands and not buttonPressed:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']
        indexFinger = lmList[8][0], lmList[8][1]
        # xVal = int(np.interp(lmList[8][0],[width//2, width],[0, width]))
        # yVal = int(np.interp(lmList[8][0], [150, height-150], [0, height]))
        # indexFinger =xVal,yVal

        if cy <= gestureThreshold:
            # Left gesture
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                if num > 0:
                    buttonPressed = True
                    annotations = [[]]
                    annotationStart = False
                    annotationNumber = 0
                    num -= 1

            # Right gesture
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                if num < len(boards) - 1:
                    buttonPressed = True
                    annotations = [[]]
                    annotationStart = False
                    annotationNumber = 0
                    num += 1

        # Pointer gesture
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(currentBoard, indexFinger, 20, (0, 0, 255), cv2.FILLED)

        # Draw gesture
        if fingers == [0, 1, 0, 0, 0]:
            if not annotationStart:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            annotations[annotationNumber].append(
                indexFinger)  # For Continuous drawing
            cv2.circle(currentBoard, indexFinger, 20, (0, 0, 255), cv2.FILLED)
        else:
            annotationStart = False

        # Eraser Gesture
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                if annotationNumber >= 0:
                    annotations.pop(-1)
                    annotationNumber -= 1
                    buttonPressed = True

    # Debounce button
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0  # Reset counter
            buttonPressed = False

    # Draw lines
    for i in range(len(annotations)):
        for j in range(1, len(annotations[i])):
            cv2.line(currentBoard,
                     annotations[i][j - 1], annotations[i][j], (0, 0, 255), 10)

    # Show small webcam preview on top-right
    smallImage = cv2.resize(img, (ws, hs))  # Resize webcam image, not board
    # webcam image overlay on currentBoard
    currentBoard[0:hs, width - ws:width] = smallImage

    # Display
    cv2.imshow("Image", img)
    cv2.imshow("Board", currentBoard)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
