import numpy as np
import cv2 as cv
import glob
import matplotlib.pyplot as plt
import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='Automatic Camera Calibration using Zhang\'s Method')
    parser.add_argument('--images', type=str, required=True, help='Path to the folder containing calibration images.')
    parser.add_argument('--pattern-size', type=str, default='9x6', help='Number of inner corners per a chessboard row and column (e.g., 9x6).')
    parser.add_argument('--square-size', type=float, default=25.0, help='Size of a square in your defined unit (e.g., millimeters).')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Parse pattern size
    try:
        pattern_cols, pattern_rows = map(int, args.pattern_size.lower().split('x'))
    except:
        print("Invalid pattern size format. Use format like 9x6.")
        return

    # Termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Prepare object points based on the actual pattern size
    objp = np.zeros((pattern_rows * pattern_cols, 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_cols, 0:pattern_rows].T.reshape(-1, 2)
    objp *= args.square_size  # Scale object points by square size

    # Arrays to store object points and image points
    objpoints = []  # 3D point in real world space
    imgpoints = []  # 2D points in image plane

    # Get list of images
    images = glob.glob(os.path.join(args.images, '*.jpg'))

    if not images:
        print(f"No images found in {args.images}. Please check the path.")
        return

    # Process each image
    for fname in images:
        img = cv.imread(fname)
        if img is None:
            print(f"Failed to load image {fname}. Skipping.")
            continue
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Find chessboard corners
        ret, corners = cv.findChessboardCorners(gray, (pattern_cols, pattern_rows), None)

        if ret:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

    if not objpoints:
        print("No corners were found in any image. Calibration failed.")
        return

    # Calibrate the camera
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    print("Camera matrix:")
    print(mtx)
    print("\nDistortion coefficients:")
    print(dist)

    # Plot reprojection error
    reprojection_errors = []
    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
        reprojection_errors.append(error)

    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(reprojection_errors) + 1), reprojection_errors, marker='o')
    plt.title('Reprojection Error for Each Image')
    plt.xlabel('Image Number')
    plt.ylabel('Reprojection Error')
    plt.grid(True)
    plt.savefig('reprojection_error.png')
    plt.show()

    # Create directories for output images if they don't exist
    os.makedirs('original', exist_ok=True)
    os.makedirs('undistorted', exist_ok=True)

    # Visualize detected corners before and after calibration
    num_images = len(images)
    for idx in range(num_images):
        img = cv.imread(images[idx])
        if img is None:
            print(f"Failed to load image {images[idx]}. Skipping.")
            continue
        h, w = img.shape[:2]

        # Draw original detected corners
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(gray, (pattern_cols, pattern_rows), None)
        if ret:
            cv.drawChessboardCorners(img, (pattern_cols, pattern_rows), corners, ret)
        original_path = f'original/original_{idx + 1}.png'
        cv.imwrite(original_path, img)

        # Undistort image
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        dst = cv.undistort(img, mtx, dist, None, newcameramtx)

        # Project and draw reprojected corners
        if idx < len(rvecs):
            corners_reproj, _ = cv.projectPoints(objpoints[idx], rvecs[idx], tvecs[idx], mtx, dist)
            corners_reproj = corners_reproj.reshape(-1, 2)
            for (x, y) in corners_reproj:
                cv.circle(dst, (int(x), int(y)), 5, (0, 255, 0), -1)
        
        undistorted_path = f'undistorted/undistorted_{idx + 1}.png'
        cv.imwrite(undistorted_path, dst)

    print("Calibration and visualization completed. Check the 'original/' and 'undistorted/' folders for results.")

if __name__ == "__main__":
    main()
