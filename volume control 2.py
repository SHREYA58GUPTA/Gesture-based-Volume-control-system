import cv2
import mediapipe as mp
import pyautogui

# Initialize variables
x1 = x2 = y1 = y2 = 0

# Initialize the webcam and Mediapipe Hands
webcam = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

while True:
    ret, image = webcam.read()
    if not ret:
        break

    frame_height, frame_width, _ = image.shape

    # Convert the image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image to detect hands
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            # Draw landmarks on the image
            drawing_utils.draw_landmarks(image, hand, mp.solutions.hands.HAND_CONNECTIONS)

            # Iterate through landmarks to find the required points
            for id, landmark in enumerate(hand.landmark):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:  # Index finger tip
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                    x1 = x
                    y1 = y
                if id == 4:  # Thumb tip
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                    x2 = x
                    y2 = y

        # Calculate distance between index finger and thumb
        dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 // 4
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)

        # Control volume based on distance
        if dist > 50:
            pyautogui.press("volumeup")
        else:
            pyautogui.press("volumedown")

    # Display the image with drawn landmarks
    cv2.imshow("Hand volume control using Python", image)
    key = cv2.waitKey(10)
    if key == 27:  # Press 'Esc' to exit
        break

# Release the webcam and destroy all windows
webcam.release()
cv2.destroyAllWindows()
