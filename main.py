import sys

import cv2
import numpy as np

OUTPUT_DIR = "images"
DEFAULT_WIDTH = 1280


def main():
    image = np.random.normal(0, 1, (get_height(), get_width()))
    # image = cv2.bitwise_not(image)  # Black and white reversal
    draw_quad_markers(image)
    cv2.imwrite(get_output_filepath(), image.astype(np.uint8))


def draw_quad_markers(image: np.ndarray):
    left = 0
    top = 0
    right = get_width() - get_marker_background_size()
    bottom = get_height() - get_marker_background_size()
    draw_marker(image, 0, left, top)
    draw_marker(image, 1, right, top)
    draw_marker(image, 2, right, bottom)
    draw_marker(image, 3, left, bottom)


def draw_marker(image: np.ndarray, id: int, x: int, y: int):
    # Draw white background
    cv2.rectangle(
        image,
        (x, y),
        (x + get_marker_background_size(), y + get_marker_background_size()),
        (255, 255, 255),
        thickness=-1,
    )
    # Draw marker
    marker = create_marker(id)
    marker_left = x + get_marker_padding()
    marker_right = marker_left + get_marker_size()
    marker_top = y + get_marker_padding()
    marker_bottom = marker_top + get_marker_size()
    image[marker_top:marker_bottom, marker_left:marker_right] = marker


def create_marker(id: int):
    aruco = cv2.aruco
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    return aruco.drawMarker(dictionary, id, get_marker_size())


def get_output_filepath() -> str:
    width = get_width()
    height = get_height()
    return f"{OUTPUT_DIR}/background-{width}x{height}.png"


def get_width() -> int:
    args = sys.argv
    if len(args) < 2:
        return DEFAULT_WIDTH
    return int(args[1])


def get_height() -> int:
    return round(get_width() * 9 / 16)


def get_marker_background_size() -> int:
    return get_marker_size() + get_marker_padding() * 2


def get_marker_size() -> int:
    return round(get_width() / 20)


def get_marker_padding() -> int:
    return round(get_marker_size() / 8)


if __name__ == "__main__":
    main()
