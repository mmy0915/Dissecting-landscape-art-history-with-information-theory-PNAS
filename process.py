import numpy as np
from gained_information import gained_information
import time
from img_to_colormatrix import img_to_colormatrix


def process(image):
    print(type(image))
    height = np.size(image, 0)  # 行数
    width = np.size(image, 1)  # 列数
    s = height * width  # 图像的面积

    num_blocks = 1
    if height == 1 or width == 1:  # 如果只剩一列/行颜色 直接退出
        # print("only 1 line/column, num_blocks:", num_blocks)
        # print("return1")
        return num_blocks
    else: # 多行颜色 继续分割
        image_colors_arr = np.reshape(image, (s, 3)) # 所有颜色
        image_colors_list1 = list(tuple(r) for r in image_colors_arr) # 转换类型
        image_colors_list = list(set(image_colors_list1)) # 去除重复元素
        # print('image_colors_list1 length（所有颜色个数）:', len(image_colors_list1))
        # print('image_colors_list length（去除重复颜色的个数）:', len(image_colors_list))
        # print('type(image_colors_list)', type(image_colors_list))
        # print('type(image_colors_list[0])', type(image_colors_list[0]))

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
            info_vert.append(gained_information(image, r, image_colors_list))   # 需要进一步优化

        # print("info_hori:", info_hori)
        # print("info_vert:", info_vert)
        # 如果至少有一组所有information都相等 直接退出
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
            # print("return2")
            return num_blocks

        # 正常情况 继续递归
        if (max_info_hori > max_info_vert and (not flag_hori)) or \
                (max_info_hori < max_info_vert and flag_vert) or \
                (max_info_hori == max_info_vert and flag_vert):
            image_left = image[:, :max_info_hori_index+1, :]
            image_right = image[:, -(width-1-max_info_hori_index):, :]
            print('process(image_left):')
            num_blocks += process(image_left)
            print('process(image_right):')
            num_blocks += process(image_right)
        elif (max_info_hori < max_info_vert and (not flag_vert)) or \
                (max_info_hori > max_info_vert and flag_hori) or \
                (max_info_hori == max_info_vert and (not flag_vert)):
            image_up = image[:max_info_vert_index+1, ...]
            image_down = image[-(height-1-max_info_vert_index):, ...]
            print('process(image_up):')
            num_blocks += process(image_up)
            print('process(image_down):')
            num_blocks += process(image_down)

    # print("return3")
    return num_blocks


