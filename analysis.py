import cv2
import numpy as np


def get_scratch_mask(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Gaussian blur
    gray = cv2.GaussianBlur(gray, (15, 15), 0)

    # Otsu threshold
    _, binary = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # scratch区域通常更亮
    binary = 255 - binary

    # morphology close
    kernel = np.ones((25, 25), np.uint8)

    binary = cv2.morphologyEx(
        binary,
        cv2.MORPH_CLOSE,
        kernel
    )

    # connected components
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary)

    if num_labels <= 1:
        return binary

    # 最大连通区域（忽略背景）
    largest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])

    mask = np.zeros_like(binary)

    mask[labels == largest] = 255

    return mask


def get_area(mask):

    return np.sum(mask > 0)


def calculate_migration(area0, area24):

    if area0 == 0:
        return 0

    return round((area0 - area24) / area0 * 100, 2)


def make_overlay(img, mask):

    overlay = img.copy()

    overlay[mask > 0] = [255, 0, 0]

    return overlay
