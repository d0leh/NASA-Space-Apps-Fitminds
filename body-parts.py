import cv2
import mediapipe as mp
import numpy as np

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

# Initialize statuses
squat_status = "Up"
biceps_right_status = "Down"
biceps_left_status = "Down"
triceps_right_status = "Down"
triceps_left_status = "Down"

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

            # Check biceps (80 - 35 degrees)
            if right_bicep_angle > 70 and biceps_right_status == "Up":
                biceps_right_status = "Down"
            if right_bicep_angle < 35  and biceps_right_status == "Down":
                biceps_right_counter += 1
                biceps_right_status = "Up"

            if left_bicep_angle > 70 and biceps_left_status == "Up":
                biceps_left_status = "Down"
            if left_bicep_angle < 35 and biceps_left_status == "Down":
                biceps_left_counter += 1
                biceps_left_status = "Up"

            # Check triceps (110 - 170 degrees)
            if right_tricep_angle < 100 and triceps_right_status == "Up":
                triceps_right_status = "Down"
            if right_tricep_angle > 160 and triceps_right_status == "Down":
                triceps_right_counter += 1
                triceps_right_status = "Up"

            if left_tricep_angle < 100 and triceps_left_status == "Up":
                triceps_left_status = "Down"
            if left_tricep_angle > 160 and triceps_left_status == "Down":
                triceps_left_counter += 1
                triceps_left_status = "Up"

            # Display the counters on the frame
            cv2.putText(image, f'Squats: {squat_counter}', (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(image, f'Biceps Right: {biceps_right_counter}', (50, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(image, f'Biceps Left: {biceps_left_counter}', (50, 150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(image, f'Tricpes Right: {triceps_right_counter}', (50, 200), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f'Tricpes Left: {triceps_left_counter}', (50, 250), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        except:
            pass

        # Render the pose landmarks on the video
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))
        
        # Display the resulting frame
        cv2.imshow('Exercise Counter', image)

        # Break loop on pressing 'q'
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
