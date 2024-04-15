import numpy as np


def extract_colors(image):
    s = np.size(image, 0) * np.size(image, 1)

    image_colors_arr = np.reshape(image, (s, 3))  # 所有颜色
    image_colors_list1 = list(tuple(r) for r in image_colors_arr)  # 转换类型
    image_colors_list = list(set(image_colors_list1))

    return image_colors_list