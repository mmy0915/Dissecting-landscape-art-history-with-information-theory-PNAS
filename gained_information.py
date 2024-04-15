from entropy import my_entropy
from conditional_entropy import conditional_entropy


def gained_information(s, r, c):
    return my_entropy(c, s)-conditional_entropy(r, c, s)