import cv2
import mediapipe as mp
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

tipIds = [4, 8, 12, 16, 20]
state = None

wCam, hCam = 720, 640

def fingerPosition(image, handNo=0):
    lmList = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
    return lmList

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        lmList = fingerPosition(image)
        
        if len(lmList) != 0:
            fingers = []
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            totalFingers = fingers.count(1)
            print("Total Fingers:", totalFingers)
            
            if totalFingers == 4:
                state = "Play"
            elif totalFingers == 0 and state == "Play":
                state = "Pause"
                pyautogui.press('space')
            elif totalFingers == 2:
                if lmList[8][1] < 300:
                    pyautogui.press('left')
                elif lmList[8][1] > 400:
                    pyautogui.press('right')
            elif totalFingers == 1:
                if lmList[9][2] < 210:
                    pyautogui.press('up')
                elif lmList[9][2] > 230:
                    pyautogui.press('down')
        
        cv2.imshow("Media Controller", image)
        
        key = cv2.waitKey(30) & 0xFF
        if key == ord("q"):
            break

cv2.destroyAllWindows()
cap.release()
