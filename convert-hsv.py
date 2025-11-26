import numpy as np
import cv2


def percentual_to_opencv(hsv):
    abs_h = int((hsv[0] / 360) * 180)
    abs_s = int((hsv[1] / 100) * 255)
    abs_v = int((hsv[2] / 100) * 255)

    return np.array([abs_h, abs_s, abs_v])


def opencv_to_percentual(hsv):
    abs_h = int((hsv[0] / 180) * 360)
    abs_s = int((hsv[1] / 255) * 100)
    abs_v = int((hsv[2] / 255) * 100)

    return np.array([abs_h, abs_s, abs_v])


def rgb_to_opencvhsv(rgb):
    rgb_color = np.uint8([[[rgb[0], rgb[1], rgb[2]]]])
    hsv_color = cv2.cvtColor(rgb_color, cv2.COLOR_RGB2HSV)
    return hsv_color


def main():
    hsv_cv2 = np.array([8, 130, 10])
    print('percentual HSV value:', opencv_to_percentual(hsv_cv2))

    hsv_p = np.array([16, 50, 3])
    print('OpenCV range value:', percentual_to_opencv(hsv_p))

    rgb = np.array([40, 28, 18])
    print('HSV:', rgb_to_opencvhsv(rgb))


if __name__ == "__main__":
    main()
