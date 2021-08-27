import mediapipe as mp
import cv2
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)
up = 0
down = 0
count = 0
with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame")
            continue

        image_height, image_width, _ = image.shape
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            sx = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width)
            sy = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height)
            #
            ex = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x * image_width)
            ey = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y * image_height)
            #
            wx = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x * image_width)
            wy = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * image_height)
            #print(results)

            distance = math.sqrt((sx-wx)**2 + (sy-wy)**2)
            #print(distance)

            if distance > 280:
                down = distance

            if distance < 150 and down > 270:
                count += 1
                down = 0

            print(count)
            cv2.putText(image, str(count), (40,80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,102,255), 5)

            cv2.circle(image, (sx, sy), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(image, (ex, ey), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(image, (wx, wy), 5, (0, 0, 255), cv2.FILLED)

            cv2.line(image, (sx,sy), (ex, ey), (255, 255, 255), 2)
            cv2.line(image, (wx, wy), (ex, ey), (0, 255, 0), 2)
            cv2.imshow("image", image)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
cap.release()
