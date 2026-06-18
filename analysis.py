import cv2
import numpy as np


def get_scratch_mask(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 平滑
    gray = cv2.GaussianBlur(gray, (9, 9), 0)

    h, w = gray.shape

    # 计算每一列的纹理（标准差）
    profile = np.std(gray, axis=0)

    # 划痕区纹理少，因此标准差低
    smooth_profile = cv2.GaussianBlur(
        profile.reshape(1, -1),
        (1, 31),
        0
    ).flatten()

    # 找最低点
    center = np.argmin(smooth_profile)

    # 最低值附近20%
作为划痕
    threshold = smooth_profile[center] * 1.2

    scratch_cols = smooth_profile <= threshold

    # 找包含中心的连续区域
    left = center
    while left > 0 and scratch_cols[left]:
        left -= 1

    right = center
    while right < w - 1 and scratch_cols[right]:
        right += 1

    mask = np.zeros_like(gray)

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

    red = np.zeros_like(img)
    red[:, :, 0] = 255

    alpha = 0.3

    overlay[mask > 0] = (
        (1 - alpha) * overlay[mask > 0]
        + alpha * red[mask > 0]
    )

    overlay = overlay.astype(np.uint8)

    return overlay
