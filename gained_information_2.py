from entropy import my_entropy
import numpy as np
from regional_entropy import regional_entropy


def gained_information2(s, r, c):
    area = np.size(s, 0) * np.size(s, 1)

    pi = []
    for item in r:
        s_r = np.size(item, 0) * np.size(item, 1) # r区域的面积
        p_r = s_r / area
        pi.append(p_r)

    return my_entropy(s, c) - pi[0] * regional_entropy(c,r[0]) - pi[1] * regional_entropy(c,r[1])