import cv2
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.8, maxHands=1)
cap = cv2.VideoCapture(0)

print("Press 's' to save gesture data, 'q' to quit")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        if lmList:
            for point in lmList:
                cv2.circle(img, tuple(point[:2]), 5, (255, 0, 0), cv2.FILLED)

    cv2.imshow("Data Collector", img)
    key = cv2.waitKey(1)

    if key == ord('s') and hands:
        gesture_label = input("Enter gesture label (e.g., draw, erase, next, prev, pointer): ")
        flat_landmarks = [coord for point in lmList for coord in point]
        with open("gesture_data.csv", "a") as f:
            f.write(",".join(map(str, flat_landmarks)) + "," + gesture_label + "\n")
        print(f"Saved gesture: {gesture_label}")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
