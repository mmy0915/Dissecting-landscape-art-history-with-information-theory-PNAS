import math
import time
import numpy as np
from img_to_colormatrix import img_to_colormatrix
from collections import Counter
# from scipy.stats import entropy


def my_entropy(c, a):
    s = np.size(a, 0) * np.size(a, 1)  # 图像的面积
    image_colors_arr = np.reshape(a, (s, 3))  # 图像中的所有颜色值 numpy.ndarray

    # C中颜色在本图像中所对应的数目
    image_colors_list = list(tuple(r) for r in image_colors_arr) # 转换类型
    # with open('image_colors_list.txt', 'w') as fp:
    #     fp.write('\n'.join('%s %s %s' % x for x in image_colors_list))

    set_c = set(c)
    image_colors_list_new = list(filter(lambda x: (x in set_c), image_colors_list))
    # with open('image_colors_list_new.txt', 'w') as fp:
    #     fp.write('\n'.join('%s %s %s' % x for x in image_colors_list_new))

    # image_colors_list中每一个颜色的总数目
    counter1 = Counter(image_colors_list_new)
    res = 0
    for item in counter1:
        p = counter1[item] / s
        res += p * math.log(p, 2)

    res = round(res, 4)
    return -res
    # 计算结果


'''    pk = []
    for item in counter1:
        p = counter1[item] / s
        pk.append(p)
    return entropy(pk, base=2)'''

'''
if __name__ == "__main__":
    st = time.time()
    matrix = img_to_colormatrix('frame_000001.JPG')
    list_c = [(0, 0, 0), (217, 220, 227),(221, 224, 231)]
    print("entropy", my_entropy(matrix, list_c))
    et = time.time()
    print("total time", round(et - st, 4))'''