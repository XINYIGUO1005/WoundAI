import cv2
import numpy as np


def get_scratch_mask(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 平滑
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # 每一列平均亮度
    profile = gray.mean(axis=0)

    # 找最亮位置（通常是划痕中心）
    center = np.argmax(profile)

    # 峰值的50%
    threshold = profile[center] * 0.5

    left = center
    while left > 0 and profile[left] > threshold:
        left -= 1

    right = center
    while right < len(profile)-1 and profile[right] > threshold:
        right += 1

    mask = np.zeros_like(gray)

    # 整个高度范围内标记划痕
    mask[:, left:right] = 255

    return mask


def get_area(mask):

    return np.sum(mask > 0)


def calculate_migration(area0, area24):

    if area0 == 0:
        return 0

    return round(
        (area0 - area24) / area0 * 100,
        2
    )


def make_overlay(img, mask):

    overlay = img.copy()

    overlay[mask > 0] = [255, 0, 0]

    return overlay
