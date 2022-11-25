from PIL import Image
import numpy


# function that makes a bayer array from a given image
def add_bayer_filter():
    image_array = numpy.array(Image.open(r"images/kodim01.png"))  # image array
    w, h, c = image_array.shape
    result_array = numpy.zeros((w, h, c), dtype=numpy.uint8)  # image array with zeros
    '''
    
    Chosen bayer pattern:   
            R  G1
            G2  B
    
    '''
    # Red
    result_array[::2, ::2, 0] = image_array[::2, ::2, 0]  # adds just the red values to the zero array
    # Blue
    result_array[1::2, 1::2, 2] = image_array[1::2, 1::2, 2]  # adds the blue values
    # Green 1
    result_array[::2, 1::2, 1] = image_array[::2, 1::2, 1]  # adds the green 1 values
    # Green 2
    result_array[1::2, ::2, 1] = image_array[1::2, ::2, 1]  # adds the green 2 values
    return result_array, image_array


# function for computing the bilinear interpolation (bi) in 3x3 range
def bilinear_interpolation(bayer_array):
    result_array = bayer_array.copy()
    w, h, c = bayer_array.shape
    # for cycles to iterate through the pixels w = number of rows, h = number of columns
    for i in range(w):
        for j in range(h):
            current = current_pixel(i, j)
            # bi for a red and a blue pixel is equivalent
            if current == "R" or current == "B":
                result_array[i, j] = bi_red_blue_pixel(bayer_array, w, h, i, j, current)
            else:
                result_array[i, j] = bi_green_pixel(bayer_array, w, h, i, j, current)
    return result_array


# function to determine the RGB value of a red or a blue pixel
def bi_red_blue_pixel(bayer_array, w, h, i, j, current):
    # coordinates are the same for both calculations
    G_value_for_RB = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    RB_value_for_RB = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
    g_sum = 0
    rb_sum = 0
    n1 = 0
    n2 = 0
    # calculation of a green value
    for m, n in G_value_for_RB:
        if 0 <= i + m < w and 0 <= j + n < h:
            n1 += 1
            g_sum += bayer_array[i + m, j + n][1]
    # calculation of a red or a blue value depending on the current pixel
    for m, n in RB_value_for_RB:
        if 0 <= i + m < w and 0 <= j + n < h:
            n2 += 1
            if current == "R":
                rb_sum += bayer_array[i + m, j + n][2]
            elif current == "B":
                rb_sum += bayer_array[i + m, j + n][0]
    if current == "R":
        result = [bayer_array[i, j][0], g_sum / n1, rb_sum / n2]
    elif current == "B":
        result = [rb_sum / n2, g_sum / n1, bayer_array[i, j][2]]
    return result


# function to determine the RGB value of a green pixel
def bi_green_pixel(bayer_array, w, h, i, j, current):
    # coordinates for red and blue values also dependent on the current pixel
    R_G1_B_G2 = [(0, -1), (0, 1)]
    B_G1_R_G2 = [(-1, 0), (1, 0)]
    r_sum = 0
    b_sum = 0
    n1 = 0
    n2 = 0
    # computing the red value for a G1 pixel and the blue value for a G2 pixel
    for m, n in R_G1_B_G2:
        if 0 <= i + m < w and 0 <= j + n < h:
            n1 += 1
            if current == "G1":
                r_sum += bayer_array[i + m, j + n][0]
            elif current == "G2":
                b_sum += bayer_array[i + m, j + n][2]
    # computing the red value for a G2 pixel and the  blue value for a G1 pixel
    for m, n in B_G1_R_G2:
        if 0 <= i + m < w and 0 <= j + n < h:
            n2 += 1
            if current == "G1":
                b_sum += bayer_array[i + m, j + n][2]
            elif current == "G2":
                r_sum += bayer_array[i + m, j + n][0]
    if current == "G1":
        result = [r_sum / n1, bayer_array[i, j][1], b_sum / n2]
    elif current == "G2":
        result = [r_sum / n2, bayer_array[i, j][1], b_sum / n1]
    return result


# function to determine the current position
def current_pixel(i, j):
    """
        Chosen bayer pattern:
                R  G1
                G2  B
    """
    # done using modulo (depends on the "Chosen bayer pattern")
    if i % 2 == 0 and j % 2 == 0:
        current = "R"
    elif i % 2 == 1 and j % 2 == 1:
        current = "B"
    elif i % 2 == 0 and j % 2 == 1:
        current = "G1"
    elif i % 2 == 1 and j % 2 == 0:
        current = "G2"
    return current
