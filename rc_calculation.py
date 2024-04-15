import numpy as np
from gained_information import gained_information


def rc_calculation(image):
    #print(type(image))
    height = np.size(image, 0)  # 行数
    width = np.size(image, 1)  # 列数
    s = height * width  # 图像的面积
    rc = 0 # 最后的返回值

    image_colors_arr = np.reshape(image, (s, 3)) # 所有颜色
    image_colors_list1 = list(tuple(r) for r in image_colors_arr) # 转换类型
    image_colors_list = list(set(image_colors_list1)) # 去除重复元素
    # 对横向每一切片(竖着切分）计算gain_information 存储在数组info_hori[1, width]中
    info_hori = []
    for i in range(width - 1):
        r = []
        r.append(image[:, :i+1, :])
        r.append(image[:, -(width-1-i):, :])
        info_hori.append(gained_information(image, r, image_colors_list))   # 需要进一步优化

    # 对竖向每一切片(横着切分）计算gain_information 存储在数组info_vert[1, height]中
    info_vert = []
    for i in range(height - 1):
        r = []
        r.append(image[:i+1, ...])
        r.append(image[-(height-1-i):, ...])
        info_vert.append(gained_information(image, r, image_colors_list))

    max_info_hori = max(info_hori)
    max_info_hori_index = info_hori.index(max(info_hori))
    max_info_vert = max(info_vert)
    max_info_vert_index = info_vert.index(max(info_vert))

    flag_hori = flag_vert = 0
    if (len(np.unique(info_hori)) == 1) and (len(info_hori) != 1): # 所有值都相等
        flag_hori = 1
    if (len(np.unique(info_vert)) == 1) and (len(info_vert) != 1):
        flag_vert = 1

    if flag_hori and flag_vert:  # 分割失败
        return 0.5

        # 正常情况 继续递归
    if (max_info_hori > max_info_vert and (not flag_hori)) or \
            (max_info_hori < max_info_vert and flag_vert) or \
            (max_info_hori == max_info_vert and flag_vert):
        rc = (max_info_hori_index + 1) / width
    elif (max_info_hori < max_info_vert and (not flag_vert)) or \
            (max_info_hori > max_info_vert and flag_hori) or \
            (max_info_hori == max_info_vert and (not flag_vert)):
        rc = (max_info_vert_index + 1) / height

    return rc


