import cv2
import mediapipe as mp

# Initialize the Pose model from MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Drawing utility for landmarks and connections
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam feed
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    
    # Convert the BGR frame (default for OpenCV) to RGB (required by MediaPipe)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect pose
    result = pose.process(rgb_frame)

    # Check if any pose landmarks were detected
    if result.pose_landmarks:
        # Draw the pose landmarks and connections on the frame
        mp_drawing.draw_landmarks(
            frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),  # Customizing landmark drawing
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)   # Customizing connection drawing
        )

    # Display the output frame
    cv2.imshow('Full Body Pose Detection', frame)

    # Break loop on 'q' key press
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
