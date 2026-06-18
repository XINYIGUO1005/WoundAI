import cv2
import numpy as np


def get_scratch_mask(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 高斯模糊
    gray = cv2.GaussianBlur(gray,(21,21),0)

    # Otsu阈值
    _, binary = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY+cv2.THRESH_OTSU
    )

    # 划痕亮，细胞暗
    binary = 255-binary

    # 沿纵向做闭运算
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (51,5)
    )

    binary = cv2.morphologyEx(
        binary,
        cv2.MORPH_CLOSE,
        kernel
    )

    return binary


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
