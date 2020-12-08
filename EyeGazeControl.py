# ALWAYS PRESS ESCAPE TO CLOSE CAMERA WINDOW
import cv2
import dlib
import math
import numpy as np
import pyautogui
pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()  # to detect face
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # to detect points on face (landmarks)
font = cv2.FONT_HERSHEY_SIMPLEX

def pointsForVerticalLine(p1, p2):
    return int((p1.x+p2.x)/2), int((p1.y+p2.y)/2)

def blinkDetremination(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    hLine = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    up_point = pointsForVerticalLine(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    down_point = pointsForVerticalLine(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
    vLine = cv2.line(frame, up_point, down_point, (0, 255, 0), 2)
    len_hLine = math.sqrt((left_point[0] - right_point[0]) ** 2 + (left_point[1] - right_point[1]) ** 2)
    len_vLine = math.sqrt((up_point[0] - down_point[0]) ** 2 + (up_point[1] - down_point[1]) ** 2)
    ratio = len_hLine / (len_vLine + 1)
    return ratio

def gazeDetectionLR(eye_points, facial_landmarks):
    eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                            (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                            (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                            (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                            (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                            (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)

    # SELECTING ONLY THE EYE FROM FACE
    h, w, _ = frame.shape
    mask = np.zeros((h, w), np.uint8)  # creating a black screen
    cv2.polylines(mask, [eye_region], True, 255, 2)
    cv2.fillPoly(mask, [eye_region], 255)  # filling the eye polygon with white color
    left_eye = cv2.bitwise_and(gray, gray, mask=mask)  # need to see what it does

    min_x = np.min(eye_region[:, 0])
    max_x = np.max(eye_region[:, 0])
    min_y = np.min(eye_region[:, 1])
    max_y = np.max(eye_region[:, 1])

    eye = frame[min_y: max_y, min_x: max_x]  # selecting the rectangular region with eye only
    gray_eye = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)  # making gray scale
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)  # creating a threshold

    h, w = threshold_eye.shape
    left_Threshold = threshold_eye[0:h, 0:int(w / 2)]  # left part of threshold_eye window
    left_White = cv2.countNonZero(left_Threshold)  # zero mean black so non zero mean white

    right_Threshold = threshold_eye[0:h, int(w / 2):w]  # right part of threshold_eye window
    right_White = cv2.countNonZero(right_Threshold)
    if left_White == 0:
        gaze_ratio = 1
    elif right_White == 0:
        gaze_ratio = 3
    else:
        gaze_ratio = left_White / right_White
    return gaze_ratio

def gazeDetectionUD(eye_points, facial_landmarks):
    eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                           (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                           (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                           (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                           (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                           (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)

    # SELECTING ONLY THE EYE FROM FACE
    h, w, _ = frame.shape
    mask = np.zeros((h, w), np.uint8)  # creating a black screen
    cv2.polylines(mask, [eye_region], True, 255, 2)
    cv2.fillPoly(mask, [eye_region], 255)  # filling the eye polygon with white color
    left_eye = cv2.bitwise_and(gray, gray, mask=mask)  # need to see what it does

    min_x = np.min(eye_region[:, 0])
    max_x = np.max(eye_region[:, 0])
    min_y = np.min(eye_region[:, 1])
    max_y = np.max(eye_region[:, 1])

    eye = frame[min_y: max_y, min_x: max_x]  # selecting the rectangular region with eye only
    gray_eye = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)  # making gray scale
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)  # creating a threshold dont know exactly what it mean
    h, w = threshold_eye.shape
    down_Threshold = threshold_eye[0:int(h/2), 0:w]  # bottom part of threshold_eye window
    down_White = cv2.countNonZero(down_Threshold)  # zero mean black non zero mean white

    up_Threshold = threshold_eye[int(h/2):h, 0:w]  # upper part of threshold_eye window
    up_White = cv2.countNonZero(up_Threshold)
    if up_White == 0:
        gaze_ratio = 0.00001
    elif down_White == 0:
        gaze_ratio = 30000
    else:
        gaze_ratio = up_White / down_White
    return gaze_ratio



def eye_movement_detectLR(net_gaze_ratio):

    if net_gaze_ratio <= 0.9:
        return "Right"
    elif net_gaze_ratio> 0.9 and net_gaze_ratio<= 1.1:
        return "Center"
    else:
        return "Left"

def eye_movement_detectUD(net_gaze_ratio):

    if net_gaze_ratio>= 1.4 and net_gaze_ratio<= 1.7:
        return "Up"
    elif net_gaze_ratio> 1.7 and net_gaze_ratio<=2.0:
        return "Center"
    else:
        return "Down"



while (True):
    _, frame = cap.read()
    gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:  # faces is the 2d array containing the region of face

        landmarks = predictor(gray, face)  # the points on the face

    # BLINK DETECTION
        right_ratio = blinkDetremination([36, 37, 38, 39, 40, 41], landmarks)
        left_ratio = blinkDetremination([42, 43, 44, 45, 46, 47], landmarks)
        net_blink_ratio = (right_ratio + left_ratio)/2

        if net_blink_ratio >= 5.7:
            cv2.putText(frame, "Eye Blink", (50, 200), font, 1, (255, 0, 0), 3)
            pyautogui.click()
        #if right_ratio >= 5.7:
            #cv2.putText(frame, "right blink", (200, 200), font, 1, (255, 0, 0), 3)
            #pyautogui.click(button='right')

    # GAZE DETECTION

        gaze_ratio_left_eyeLR = gazeDetectionLR([42, 43, 44, 45, 46, 47], landmarks)
        gaze_ratio_left_eyeUD = gazeDetectionUD([42, 43, 44, 45, 46, 47], landmarks)
        gaze_ratio_right_eyeLR = gazeDetectionLR([36, 37, 38, 39, 40, 41], landmarks)
        gaze_ratio_right_eyeUD = gazeDetectionUD([36, 37, 38, 39, 40, 41], landmarks)

        net_gaze_ratioLR = (gaze_ratio_left_eyeLR + gaze_ratio_right_eyeLR)/2
        net_gaze_ratioUD = (gaze_ratio_left_eyeUD + gaze_ratio_right_eyeUD)/2

        if net_gaze_ratioLR <= 0.9:
            cv2.putText(frame, "RIGHT", (200,50), font, 2, (0, 0, 255), 3)
        elif net_gaze_ratioLR > 0.1  and net_gaze_ratioLR <= 1.1 :
            cv2.putText(frame, "CENTER", (200, 50), font, 2, (0, 0, 255), 3)
        else:
            cv2.putText(frame, "LEFT", (200, 50), font, 2, (0, 0, 255), 3)

        if net_gaze_ratioUD >= 1.4 and net_gaze_ratioUD <= 1.6 :
            cv2.putText(frame, "UP", (500, 50), font, 1, (0, 0, 255), 3)
        elif net_gaze_ratioLR > 0.1 and net_gaze_ratioLR <= 1.1:
            cv2.putText(frame, "CENTER", (500, 50), font, 1, (0, 0, 255), 3)
        else:
            cv2.putText(frame, "DOWN", (500, 50), font, 1, (0, 0, 255), 3)

        cv2.putText(frame, "UD" + str(net_gaze_ratioUD), (200, 200), font, 2, (0, 0, 255), 3)
        cv2.putText(frame, "LR" + str(net_gaze_ratioLR), (200, 400), font, 2, (0, 0, 255), 3)

        if eye_movement_detectLR(net_gaze_ratioLR) == "Right":
            pyautogui.move(20, 0)
        if eye_movement_detectLR(net_gaze_ratioLR) == "Left":
            pyautogui.move(-20, 0)

        if eye_movement_detectUD(net_gaze_ratioUD) == "Up":
            pyautogui.move(0, 10)
        if eye_movement_detectUD(net_gaze_ratioUD) == "Down":
            pyautogui.move(0, -10)



        cv2.imshow("frame",frame)
    key = cv2.waitKey(1)
    if key == 27:  # 27 ==escape key
        break

cap.release()
cv2.destroyAllWindows()
