import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import joblib  # <-- added

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
buttonDelay = 10

# For drawing
annotations = [[]]
annotationNumber = -1
annotationStart = False

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Load AI gesture model
model = joblib.load("gesture_model.pkl")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    board = os.path.join(folderPath, boards[num])
    currentBoard = cv2.imread(board)
    currentBoard = cv2.resize(currentBoard, (width, height))  # Match camera size

    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and not buttonPressed:
        hand = hands[0]
        lmList = hand['lmList']
        cx, cy = hand['center']
        indexFinger = lmList[8][0], lmList[8][1]

        if lmList:
            # Prepare input for model prediction
            flat_landmarks = [coord for point in lmList for coord in point]
            predicted_gesture = model.predict([flat_landmarks])[0]
            print("Predicted Gesture:", predicted_gesture)

            if cy <= gestureThreshold:
                if predicted_gesture == "prev":
                    print("Prev Board")
                    if num > 0:
                        buttonPressed = True
                        num -= 1

                elif predicted_gesture == "next":
                    print("Next Board")
                    if num < len(boards) - 1:
                        buttonPressed = True
                        num += 1

            if predicted_gesture == "pointer":
                cv2.circle(currentBoard, indexFinger, 20, (0, 0, 255), cv2.FILLED)

            elif predicted_gesture == "draw":
                if not annotationStart:
                    annotationStart = True
                    annotationNumber += 1
                    annotations.append([])
                annotations[annotationNumber].append(indexFinger)
                cv2.circle(currentBoard, indexFinger, 20, (0, 0, 255), cv2.FILLED)
            else:
                annotationStart = False

            # You can add eraser gesture logic here:
            # elif predicted_gesture == "erase":
            #     # Implement erase logic

    # Debounce button
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0  # Reset counter
            buttonPressed = False

    # Draw lines
    for i in range(len(annotations)):
        for j in range(1, len(annotations[i])):
            cv2.line(currentBoard, annotations[i][j - 1], annotations[i][j], (0, 0, 255), 10)

    # Show small webcam preview on top-right
    smallImage = cv2.resize(img, (ws, hs))
    currentBoard[0:hs, width - ws:width] = smallImage

    # Display
    cv2.imshow("Image", img)
    cv2.imshow("Board", currentBoard)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
