import numpy as np
from functions import *

# coefficients from the Malvar demosaicing method
alpha = 1 / 2
beta = 5 / 8
gamma = 3 / 4


# function for the Malvar demosaicing method
def Malvar(bayer_array, w, h):
    result_array = bayer_array.copy()
    # iterating through the pixels of an image (w = num. of rows, h = num. of columns)
    for i in range(w):
        for j in range(h):
            current = current_pixel(i, j)
            # calculates the bilinear interpolation depending on the current pixel
            if current == "R" or current == "B":
                bi_int = bi_red_blue_pixel(bayer_array, w, h, i, j, current)
            else:
                bi_int = bi_green_pixel(bayer_array, w, h, i, j, current)
            # calculates the RGB values using the corresponding corrections
            if current == "R":
                r_correction = correction_R_loc(bayer_array, w, h, i, j)
                r_value = bi_int[0]
                g_value = bi_int[1] + r_correction
                b_value = bi_int[2] + r_correction
            elif current == "B":
                b_correction = correction_B_loc(bayer_array, w, h, i, j)
                bi_int = bi_red_blue_pixel(bayer_array, w, h, i, j, current)
                r_value = bi_int[0] + b_correction
                g_value = bi_int[1] + b_correction
                b_value = bi_int[2]
            else:
                g_correction = correction_G_loc(bayer_array, w, h, i, j)
                r_value = bi_int[0] + g_correction
                g_value = bi_int[1]
                b_value = bi_int[2] + g_correction
            # this stops overflowing of certain values
            r_value = np.clip(r_value, 0, 255)
            g_value = np.clip(g_value, 0, 255)
            b_value = np.clip(b_value, 0, 255)

            result_array[i, j] = [r_value, g_value, b_value]
    return result_array


# function for correcting values at the location of a red pixel
def correction_R_loc(bayer_array, w, h, i, j):
    # corresponding coordinates
    MN_values = [(0, -2), (0, 2), (-2, 0), (2, 0)]

    num_of_val = 0
    r_sum = 0
    # the method is equal to the bilinear interpolation (bi) just different coordinates
    for m, n in MN_values:
        if 0 <= i + m < w and 0 <= j + n < h:
            num_of_val += 1
            r_sum += bayer_array[i + m, j + n][0]
    r_gradient = bayer_array[i, j][0] - r_sum / num_of_val
    return alpha*r_gradient


# function for correcting values at the location of a blue pixel
def correction_B_loc(bayer_array, w, h, i, j):
    # corresponding coordinates
    MN_values = [(0, -2), (0, 2), (-2, 0), (2, 0)]

    num_of_val = 0
    b_sum = 0
    # the method is equal to the bi just different coordinates
    for m, n in MN_values:
        if 0 <= i + m < w and 0 <= j + n < h:
            num_of_val += 1
            b_sum += bayer_array[i + m, j + n][2]
    b_gradient = bayer_array[i, j][2] + -b_sum / num_of_val
    return gamma*b_gradient


# function for correcting values at the location of a green pixel
# we do not need to differentiate the green pixels because they have the same values of coordinates
def correction_G_loc(bayer_array, w, h, i, j):
    # corresponding coordinates
    MN_values_G = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -2), (0, 2), (-2, 0), (2, 0)]

    num_of_val = 0
    g_sum = 0
    # the method is equal to the bi just different coordinates
    for m, n in MN_values_G:
        if 0 <= i + m < w and 0 <= j + n < h:
            num_of_val += 1
            g_sum += bayer_array[i + m, j + n][1]
    g_gradient = bayer_array[i, j][1] + -g_sum / num_of_val
    return beta*g_gradient
