import numpy as np
from gained_information import gained_information
import multiprocessing as mp
from multiprocessing import Manager
import os
from regional_entropy import regional_entropy
from gained_information_2 import gained_information2
from entropy import my_entropy
from extract_colors import extract_colors
import math
from collections import Counter

'''
def process_image(slice_order, return_dict):
    if slice_order != 7:
        if slice_order == 0:  # 图像名称的数字是个位数
            for j in range(image_jump_unit): # (0, 9)
                filename = 'frame_00000.jpg' + str(j + 1) + '.jpg'
                return_dict[filename] = process(filename)
        else: # 其他情况
            for j in range(image_jump_unit): # (0, 9)
                filename = 'frame_0000.jpg' + str(slice_order * image_jump_unit + j + 1) + '.jpg'
                return_dict[filename] = process(filename)
    else: # 最后一个进程 需要把剩下的图像都
        for j in range(file_num - slice_order * image_jump_unit):
            filename = 'frame_0000.jpg' + str(slice_order * image_jump_unit + j + 1) + '.jpg'
            return_dict[filename] = process(filename)
'''


def process(image):
    height = np.size(image, 0)  # 行数
    width = np.size(image, 1)  # 列数
    s = height * width  # 图像的面积

    num_blocks = 1
    if height == 1 or width == 1:  # 如果只剩一列/行颜色 直接退出
        # print("only 1 line/column, num_blocks:", num_blocks)
        print("return1")
        return num_blocks
    else:  # 多行颜色 继续分割
        image_colors_list = extract_colors(image)  # 去除重复元素
        # print('image_colors_list1 length（所有颜色个数）:', len(image_colors_list1))
        # print('image_colors_list length（去除重复颜色的个数）:', len(image_colors_list))
        # print('type(image_colors_list)', type(image_colors_list))
        # print('type(image_colors_list[0])', type(image_colors_list[0]))
        hc = my_entropy(image_colors_list, image)

        # 对横向每一切片(竖着切分）计算gain_information 存储在数组info_hori[1, width]中
        info_hori = []
        h_c_r1_hori = h_c_r2_hori = []
        for i in range(width - 1):
            r = []
            r.append(image[:, :i + 1, :])
            r.append(image[:, -(width - 1 - i):, :])

            pi_h = []  # pi1、pi2
            for item in r:
                p_r = np.size(item, 0) * np.size(item, 1) / s
                pi_h.append(p_r)

            if i == 0:  # 第一个I(C, R)数值直接计算
                h_c_r1_hori.append(regional_entropy(image_colors_list, r[0]))
                h_c_r2_hori.append(regional_entropy(image_colors_list, r[1]))
                info_hori.append(hc - pi_h[0] * h_c_r1_hori[0] - pi_h[1] * h_c_r2_hori[0])
            else: # 第二个I(C, R)数值开始用lub算法
                # 计算H(C,r1')
                c01_h = extract_colors(image[:, :i, :])  # C0 只属于前一个区域的颜色
                # cm1 = extract_colors(image[:, :i + 1, :])  # Cm 原区域和新增区域的公有颜色
                ca1_h = extract_colors(image[:, i: i + 1, :])  # Ca 新增区域的特有颜色

                counter_c01_h = Counter(c01_h)  # N(c)
                counter_ca_h = Counter(ca1_h)  # n(c)
                counter_cm1_h = counter_c01_h + counter_ca_h  # N(c) + n(c)

                area_r1_h = height * (i + 2)  # Lx * (k + 1) , k = i + 1
                value1 = value2 = value3 = 0
                # 第三项
                for item in counter_cm1_h:
                    temp = counter_cm1_h[item] / area_r1_h
                    value1 += temp * math.log(temp, 2)

                # 第四项
                for item in counter_cm1_h:
                    temp = counter_c01_h[item] / area_r1_h
                    if temp == 0:
                        continue
                    else:
                        value2 += temp * math.log(temp, 2)

                # 第五项
                for item in counter_ca_h:
                    temp = counter_ca_h[item] / area_r1_h
                    value3 += temp * math.log(temp, 2)

                h_c_r1_hori.append((i + 1)/(i + 2) * h_c_r1_hori[i-1] - (i + 1)/(i + 2) * math.log((i + 1)/(i + 2), 2)
                                   - value1 + value2 - value3)

                # 计算H(C,r2')
                c02_h = extract_colors(image[:, -(width - i):, :])  # C0 只属于前一个区域的颜色
                # cm2 = extract_colors(image[:, -(width - 1 - i):, :])  # Cm 原区域和新增区域的公有颜色
                cd_h = extract_colors(image[:, -(width - i): -(width - 1 - i), :])  # Ca 新增区域的特有颜色

                counter_c02_h = Counter(c02_h)  # N(c)
                counter_cd_h = Counter(cd_h)  # n(c)
                counter_cm2_h = counter_c02_h + counter_cd_h

                counter_update_h = counter_c02_h
                counter_update_h.subtract(counter_cd_h)  # N(c) - n(c)

                area_r2_h = height * (width - (i + 1))  # Lx *（Ly - (k + 1))
                value4 = value5 = value6 = 0
                # 第三项
                for item in counter_cm2_h:
                    temp = counter_update_h[item] / area_r2_h
                    if temp == 0:
                        continue
                    else:
                        value4 += temp * math.log(temp, 2)

                # 第四项
                for item in counter_cm2_h:
                    temp = counter_c02_h[item] / area_r2_h
                    if temp == 0:
                        continue
                    else:
                        value5 += temp * math.log(temp, 2)

                # 第五项
                for item in counter_cd_h:
                    temp = counter_cd_h[item] / area_r2_h
                    value6 += temp * math.log(temp, 2)

                h_c_r2_hori.append((width - i) / (width - i - 1) * h_c_r2_hori[i - 1]
                                   - (width - i) / (width - i - 1) * math.log((width - i) / (width - i - 1), 2)
                                   - value4 + value5 + value6)

                info_hori.append(hc - pi_h[0] * h_c_r1_hori[i] - pi_h[1] * h_c_r2_hori[i])

        # 对竖向每一切片(横着切分）计算gain_information 存储在数组info_vert[1, height]中
        info_vert = []
        h_c_r1_vert = h_c_r2_vert = []
        for i in range(height - 1):
            r = []
            r.append(image[: i + 1, ...])
            r.append(image[-(height - 1 - i):, ...])

            pi_v = []
            for item in r:
                p_r = np.size(item, 0) * np.size(item, 1) / s
                pi_v.append(p_r)

            if i == 0:  # 第一个数值直接计算
                h_c_r1_vert.append(regional_entropy(image_colors_list, r[0]))
                h_c_r2_vert.append(regional_entropy(image_colors_list, r[1]))
                info_hori.append(my_entropy(image_colors_list, image) - pi_v[0] * h_c_r1_vert[0] - pi_v[1] * h_c_r2_vert[0])
            else:  # 第二对数值开始用lub算法
                # 计算H(C,r1')
                c01_v = extract_colors(image[: i, ...])  # C0 只属于前一个区域的颜色
                # cm1 = extract_colors(image[:, :i + 1, :])  # Cm 原区域和新增区域的公有颜色
                ca_v = extract_colors(image[i: i + 1, ...])  # Ca 新增区域的特有颜色

                counter_c01_v = Counter(c01_v)
                counter_ca_v = Counter(ca_v)
                counter_cm1_v = counter_c01_v + counter_ca_v

                area_r1_v = width * (i + 1)  # Lx * (k + 1)
                value11 = value22 = value33 = 0
                # 第三项
                for item in counter_cm1_v:
                    temp = counter_cm1_v[item] / area_r1_v
                    value11 += temp * math.log(temp, 2)

                # 第四项
                for item in counter_cm1_v:
                    temp = counter_c01_v[item] / area_r1_v
                    if temp == 0:
                        continue
                    else:
                        value22 += temp * math.log(temp, 2)

                # 第五项
                for item in counter_ca_v:
                    temp = counter_ca_v[item] / area_r1_v
                    value33 += temp * math.log(temp, 2)

                h_c_r1_vert.append((i + 1) / (i + 2) * h_c_r1_vert[i - 1]
                                   - (i + 1) / (i + 2) * math.log((i + 1) / (i + 2), 2)
                                   - value11 + value22 - value33)

                # 计算H(C,r2')
                c02_v = extract_colors(image[-(height - i):, ...])  # C0 只属于前一个区域的颜色
                # cm2 = extract_colors(image[-(height - 1 - i):, ...])  # Cm 原区域和新增区域的公有颜色
                cd_v = extract_colors(image[-(height - i): -(height - 1 - i), ...])  # Ca 新增区域的特有颜色

                counter_c02_v = Counter(c02_v)
                counter_cd_v = Counter(cd_v)
                counter_cm2_v = counter_c02_v + counter_cd_v
                counter_update_v = counter_c02_v
                counter_update_v.subtract(counter_cd_v)  # N(c) - n(c)

                area_r2_v = width * (height - (i + 1))  # Lx *（Ly - (k + 1)）
                value44 = value55 = value66 = 0
                # 第三项
                for item in counter_cm2_v:
                    temp = counter_update_v[item] / area_r2_v
                    if temp == 0:
                        continue
                    else:
                        value44 += temp * math.log(temp, 2)

                # 第四项
                for item in counter_cm2_v:
                    temp = counter_c02_v[item] / area_r2_v
                    if temp == 0:
                        continue
                    else:
                        value55 += temp * math.log(temp, 2)

                # 第五项
                for item in counter_cd_v:
                    temp = counter_cd_v[item] / area_r2_v
                    value66 += temp * math.log(temp, 2)

                h_c_r2_vert.append((height - i) / (height - i - 1) * h_c_r2_vert[i - 1]
                                   - (height - i) / (height - i - 1) * math.log((height - i) / (height - i - 1), 2)
                                   - value44 + value55 - value66)

                info_vert.append(hc - pi_v[0] * h_c_r1_vert[i] - pi_v[1] * h_c_r2_vert[i])

        # 如果至少有一组所有information都相等 直接退出
        print('info_hori:', info_hori)
        print('info_vert:', info_vert)
        max_info_hori = max(info_hori)
        max_info_hori_index = info_hori.index(max(info_hori))
        max_info_vert = max(info_vert)
        max_info_vert_index = info_vert.index(max(info_vert))
        flag_hori = flag_vert = 0

        if (len(np.unique(info_hori)) == 1) and (len(info_hori) != 1):  # 所有值都相等
            flag_hori = 1
        if (len(np.unique(info_vert)) == 1) and (len(info_vert) != 1):
            flag_vert = 1

        if flag_hori and flag_vert:  # 分割失败
            print("return2")
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

    print("return3")
    return num_blocks

'''
if __name__ == "__main__":
    st = time.time()
    num_processes = mp.cpu_count() #8
    path = './seconds1'
    file_num = len([lists for lists in os.listdir(path) if os.path.isfile(os.path.join(path, lists))]) #79
    image_jump_unit = file_num // num_processes #9

    manager = Manager()
    # return_list = manager.list() 也可以使用列表list
    return_dict = manager.dict()
    jobs = []
    for i in range(8):
        p = mp.Process(target = process_image, args=(i, return_dict))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    values = return_dict.values()
    # 以key为关键词对value排序

    et = time.time()

    print("total time", et - st)
    '''

