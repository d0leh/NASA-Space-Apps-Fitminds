import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe Pose and Drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Middle point
    c = np.array(c)  # Last point
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Initialize counters for exercises
squat_counter = 0
biceps_right_counter = 0
biceps_left_counter = 0
triceps_right_counter = 0
triceps_left_counter = 0
back_counter = 0

squat_completed = False
biceps_right_completed = False
biceps_left_completed = False
triceps_right_completed = False
triceps_left_completed = False
back_completed = False

# Initialize statuses
squat_status = "Up"
biceps_right_status = "Down"
biceps_left_status = "Down"
triceps_right_status = "Down"
triceps_left_status = "Down"
back_status = "Down"

#initialize display times
squat_display_time = None
biceps_right_display_time = None
biceps_left_display_time = None
triceps_right_display_time = None
triceps_left_display_time = None
back_display_time = None

#excercise completion dictionary
completion_dict = {
            "squat": 0,
            "biceps_right": 0,
            "biceps_left": 0,
            "triceps_right": 0,
            "triceps_left": 0,
            "back": 0
        }

# Start video capture
cap = cv2.VideoCapture(0)

# Set up Mediapipe Pose
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Recolor the image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # Make detections
        results = pose.process(image)
        
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        try:
        # Extract landmarks
            landmarks = results.pose_landmarks.landmark

            # Get coordinates for hip, knee, and ankle (for squats)
            hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, 
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, 
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, 
                        landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            
            # Calculate squat angle
            knee_angle = calculate_angle(hip, knee, ankle)

            # Check squat status
            if knee_angle < 90 and squat_status == "Up":
                squat_status = "Down"
            if knee_angle > 160 and squat_status == "Down":
                squat_counter += 1
                squat_status = "Up"

            # Get coordinates for elbows
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, 
                                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, 
                            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, 
                            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, 
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, 
                            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, 
                            landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            # Calculate angles for biceps and triceps
            right_bicep_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            left_bicep_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_tricep_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            left_tricep_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

            if right_bicep_angle > 70 and biceps_right_status == "Down" and right_elbow[1] > right_shoulder[1]:
                biceps_right_status = "Up"
            if right_bicep_angle < 35  and biceps_right_status == "Up" and right_elbow[1] > right_shoulder[1]:
                biceps_right_counter += 1
                biceps_right_status = "Down"
                back_status = "Down"
                

            if left_bicep_angle > 70 and biceps_left_status == "Down" and left_elbow[1] > left_shoulder[1]:
                biceps_left_status = "Up"
            if left_bicep_angle < 35 and biceps_left_status == "Up" and left_elbow[1] > left_shoulder[1]:
                biceps_left_counter += 1
                biceps_left_status = "Down"
                back_status = "Down"

            if right_tricep_angle < 100 and triceps_right_status == "Down" and right_elbow[1] > right_shoulder[1]:
                triceps_right_status = "Up"
            if right_tricep_angle > 165 and triceps_right_status == "Up" and right_elbow[1] > right_shoulder[1]:
                triceps_right_counter += 1
                triceps_right_status = "Down"
                back_status = "Down"

            if left_tricep_angle < 100 and triceps_left_status == "Down" and left_elbow[1] > left_shoulder[1]:
                triceps_left_status = "Up"
            if left_tricep_angle > 165 and triceps_left_status == "Up" and left_elbow[1] > left_shoulder[1]:
                triceps_left_counter += 1
                triceps_left_status = "Down"
                back_status = "Down"

            #back excercise
            right_back_angle = calculate_angle(right_hip, right_shoulder, right_elbow)
            left_back_angle = calculate_angle(left_hip, left_shoulder, left_elbow)
            if (right_back_angle > 150 and right_elbow[1] < right_shoulder[1]) and \
            (left_back_angle > 150 and left_elbow[1] < left_shoulder[1]):
                if back_status == "Up": 
                    back_counter += 1
                    back_status = "Down" 
                    biceps_left_status = "Down"
                    biceps_right_status = "Down"
                    triceps_right_status = "Down"
                    triceps_left_status = "Down"
            else:
                back_status = "Up"


            # # Display the counters on the frame
            # cv2.putText(image, f'Squats: {squat_counter}', (50, 50), 
            #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            # cv2.putText(image, f'Biceps Right: {biceps_right_counter}', (50, 100), 
            #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            # cv2.putText(image, f'Biceps Left: {biceps_left_counter}', (50, 150), 
            #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            # cv2.putText(image, f'Tricpes Right: {triceps_right_counter}', (50, 200), 
            #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            # cv2.putText(image, f'Tricpes Left: {triceps_left_counter}', (50, 250), 
            #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            # cv2.putText(image, f'Back: {back_counter}', (50, 300), 
            #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
            
        except Exception as e:
            print(e)
            pass

        mp_drawing.draw_landmarks(
            image, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),  # White dots
            mp_drawing.DrawingSpec(color=(173, 216, 230), thickness=2, circle_radius=2)   # Light blue lines
        )


        if squat_counter >= 2:
            completion_dict["squat"] += 1
            squat_display_time = time.time()
            squat_completed = True
            biceps_left_counter = 0
            biceps_right_counter = 0
            triceps_left_counter = 0
            triceps_right_counter = 0
            back_counter = 0
            squat_counter = 0

        if biceps_right_counter >= 5:
            completion_dict["biceps_right"] += 1
            biceps_right_display_time = time.time()
            biceps_right_completed = True
            biceps_right_counter = 0
            triceps_left_counter = 0
            triceps_right_counter = 0
            back_counter = 0
            squat_counter = 0

        if biceps_left_counter >= 5:
            completion_dict["biceps_left"] += 1
            biceps_left_display_time = time.time()
            biceps_left_completed = True
            biceps_left_counter = 0
            triceps_left_counter = 0
            triceps_right_counter = 0
            back_counter = 0
            squat_counter = 0

        if triceps_right_counter >= 5:
            completion_dict["triceps_right"] += 1
            triceps_right_display_time = time.time()
            triceps_right_completed = True
            biceps_left_counter = 0
            biceps_right_counter = 0
            triceps_right_counter = 0
            back_counter = 0
            squat_counter = 0

        if triceps_left_counter >= 5:
            completion_dict["triceps_left"] += 1
            triceps_left_display_time = time.time()
            triceps_left_completed = True
            biceps_left_counter = 0
            biceps_right_counter = 0
            triceps_left_counter = 0
            back_counter = 0
            squat_counter = 0

        if back_counter >= 5:
            completion_dict["back"] += 1
            back_display_time = time.time()
            back_completed = True
            biceps_left_counter = 0
            biceps_right_counter = 0
            triceps_left_counter = 0
            triceps_right_counter = 0
            back_counter = 0
            squat_counter = 0
        

        try:
            if squat_completed and squat_display_time > time.time() - 3:
                # Bottom center for squat
                cv2.putText(image, "Squat", 
                            (image.shape[1] // 2 - 100, image.shape[0] - 50),  # Bottom center
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            elif squat_completed:
                squat_completed = False
        except:
            pass

        try:
            if biceps_right_completed and biceps_right_display_time > time.time() - 3:
                # Top right for right biceps
                cv2.putText(image, "Right biceps", 
                            (image.shape[1] - 300, 50),  # Top right
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            elif biceps_right_completed:
                biceps_right_completed = False
        except:
            pass

        try:
            if biceps_left_completed and biceps_left_display_time > time.time() - 3:
                # Top left for left biceps
                cv2.putText(image, "Left biceps", 
                            (50, 50),  # Top left
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)    
            elif biceps_left_completed:
                biceps_left_completed = False
        except:
            pass

        try:
            if triceps_right_completed and triceps_right_display_time > time.time() - 3:
                # Top right for right triceps
                cv2.putText(image, "Right triceps", 
                            (image.shape[1] - 300, 100),  # Top right
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            elif triceps_right_completed:
                triceps_right_completed = False
        except:
            pass

        try:
            if triceps_left_completed and triceps_left_display_time > time.time() - 3:
                # Top left for left triceps
                cv2.putText(image, "Left triceps", 
                            (50, 100),  # Top left
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            elif triceps_left_completed:
                triceps_left_completed = False
        except:
            pass

        try:
            if back_completed and back_display_time > time.time() - 3:
                # Top center for back
                cv2.putText(image, "Back", 
                            (image.shape[1] // 2 - 100, 50),  # Top center
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            elif back_completed:
                back_completed = False
        except:
            pass


        # write the dict into a json file called exercise.json
        with open("exercise.json", "w") as f:
            f.write(str(completion_dict))

        # Display the resulting frame
        cv2.imshow('Exercise Counter', image)

        # Break loop on pressing 'q'
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
