import numpy as np
from collections import Counter
import math
import time
from img_to_colormatrix import img_to_colormatrix


def conditional_entropy(R, C, S):
    s = np.size(S, 0) * np.size(S, 1)
    res = 0
    for r in R:
        region_colors_arr = np.reshape(r, (np.size(r, 0) * np.size(r, 1), 3))
        region_colors_list = list(tuple(r) for r in region_colors_arr)

        set_c = set(C)
        region_colors_list_new = list(filter(lambda x: x in set_c, region_colors_list))
        counter1 = Counter(region_colors_list_new)

        s_r = np.size(r, 0) * np.size(r, 1) # r区域的面积
        p_r = s_r / s
        for item in counter1:
            c_p = counter1[item]/s_r  # c_p for conditional_probability
            j_p = c_p * p_r  # j_p for joint probability
            res += j_p * math.log(c_p, 2)

    res = round(res, 4)
    return -res

'''
if __name__ == "__main__":
    st = time.time()
    image = img_to_colormatrix('frame_000001.JPG')
    s = np.size(image, 0) * np.size(image, 1)
    image_colors_arr = np.reshape(image, (s, 3))
    image_colors_list1 = list(tuple(r) for r in image_colors_arr)
    image_colors_list = list(set([i for i in image_colors_list1]))

    r = []
    r.append(image[:, :1, :])
    r.append(image[:, -(np.size(image, 1) - 1):, :])

    print("entropy", conditional_entropy(r, image_colors_list, image))
    et = time.time()
    print("total time", et - st)'''