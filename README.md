# Automatic Camera Calibration using Zhang's Method

![Original Calibration Image](https://github.com/MayankD409/AutoCalib/blob/main/Results/original_1.png)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Methodology](#methodology)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview

This repository provides an implementation of **Automatic Camera Calibration** based on the method presented in ["A Flexible New Technique for Camera Calibration" by Zhengyou Zhang](https://www.microsoft.com/en-us/research/publication/a-flexible-new-technique-for-camera-calibration/). The calibration process utilizes a checkerboard pattern to accurately determine camera parameters, enabling applications in computer vision, robotics, and augmented reality.

## Features

- **Automatic Detection**: Automatically detects checkerboard corners in images.
- **Flexible Calibration**: Handles various camera models and distortion parameters.
- **Visualization Tools**: Provides tools to visualize detected points and calibration results.
- **Extensible Codebase**: Easily extendable for different calibration patterns or additional features.
- **Comprehensive Documentation**: Detailed instructions and explanations to facilitate understanding and usage.

## Installation

### Prerequisites

- [Python 3.7+](https://www.python.org/downloads/)
- [OpenCV](https://opencv.org/) (`opencv-python` package)
- [NumPy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/) (optional, for visualization)

### Steps

1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. **Create a Virtual Environment (Optional but Recommended)**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Capturing Calibration Images

Before running the calibration, you need to capture multiple images of the checkerboard pattern from different angles and distances. This can be done using the provided `capture.py` script.

#### **Steps to Capture Images**

1. **Prepare the Checkerboard**
    - **Print the Checkerboard Pattern**: Ensure the printed checkerboard is flat and has known square sizes (e.g., 25mm squares).
    - **Mount the Checkerboard**: Place the checkerboard on a flat surface or mount it on a rigid board to maintain its shape.

2. **Run the Image Capture Script**
    ```bash
    python capture.py --output calibration_images/ --show
    ```
    - `--output`: (Optional) Specify the directory to save captured images. Default is `calibration_images/`.
    - `--show`: (Optional) Display the live video feed with instructional overlays.

3. **Capture Images**
    - **Position the Checkerboard**: Move the checkerboard to different angles, orientations, and distances within the camera's view.
    - **Capture Image**: Press the **Spacebar** to capture and save an image when the checkerboard is well-positioned.
    - **Exit**: Press the **Esc** key to exit the capture mode.

4. **Ensure Image Quality**
    - **Lighting**: Ensure good lighting to avoid shadows and reflections.
    - **Focus**: The checkerboard should be in focus and occupy a significant portion of the frame.
    - **Variety**: Capture images from various perspectives to improve calibration accuracy.

5. **Verify Captured Images**
    - Check the `calibration_images/` directory to ensure that images are saved correctly.
    - Ensure that each image has a clearly visible checkerboard pattern.

### Running the Calibration

1. **Place Calibration Images**
    - Store all calibration images in a designated folder, e.g., `calibration_images/`.

2. **Execute the Calibration Script**
    ```bash
    python calibrate.py --images calibration_images/ --pattern-size 7x6 --square-size 25
    ```

    - `--images`: Path to the folder containing calibration images.
    - `--pattern-size`: Number of inner corners per a chessboard row and column (e.g., `7x6`).
    - `--square-size`: Size of a square in your defined unit (e.g., millimeters).

3. **Review Calibration Results**
    - The script will output the camera matrix and distortion coefficients in the console.
    - It will also generate a `reprojection_error.png` plot showing the reprojection error for each image.
    - Undistorted images will be saved in the `undistorted/` folder, and original images with detected corners will be saved in the `original/` folder.

