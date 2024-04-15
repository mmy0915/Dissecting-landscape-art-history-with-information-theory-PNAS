import time
from process import process
from img_to_colormatrix import img_to_colormatrix
from rc_calculation import rc_calculation
from rc_cal_lub import rc_cal_lub
import pandas as pd
import os
import csv

if __name__ == "__main__":
    path = './Love is a Lunatic City/'
    path_list = os.listdir(path)
    path_list.sort()
    path_list_tt = path_list[60:62]

    with open("./rc_Love is a Lunatic City.csv", "a", newline='', encoding='GBK') as f:
        writer = csv.writer(f, delimiter=',')
        for item in path_list_tt:
            list = []
            st = time.time()
            matrix = img_to_colormatrix('./Love is a Lunatic City/' + item)
            rc = rc_calculation(matrix)
            et = time.time()
            time_used = et - st

            list.append(item)
            list.append(rc)
            list.append(time_used)
            writer.writerow(list)

    '''st = time.time()
    matrix = img_to_colormatrix('./红气球/frame_000118.jpg')
    print("rc:", rc_cal_lub(matrix))
    et = time.time()
    print("total time", et - st)'''
