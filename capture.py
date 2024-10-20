import cv2
import os
import argparse
import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(description='Capture calibration images using your laptop camera.')
    parser.add_argument('--output', type=str, default='calibration_images', help='Directory to save captured images.')
    parser.add_argument('--show', action='store_true', help='Show live video feed with overlays.')
    parser.add_argument('--delay', type=int, default=1000, help='Delay in milliseconds between captures when using automatic capture.')
    return parser.parse_args()

def create_output_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory {directory} for saving calibration images.")
    else:
        print(f"Saving calibration images to existing directory: {directory}")

def main():
    args = parse_arguments()
    output_dir = args.output
    create_output_dir(output_dir)

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot access the camera.")
        return

    print("Press 'Spacebar' to capture an image.")
    print("Press 'Esc' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame from camera.")
            break

        display_frame = frame.copy()

        if args.show:
            # Overlay instructions on the frame
            cv2.putText(display_frame, "Press 'Spacebar' to capture image", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(display_frame, "Press 'Esc' to exit", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Camera Feed', display_frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # Esc key to exit
            print("Exiting image capture.")
            break
        elif key == 32:  # Spacebar to capture
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(output_dir, f"calib_{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Captured image saved as {filename}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
