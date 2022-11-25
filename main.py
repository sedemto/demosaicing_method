import PIL
import numpy as np
from matplotlib import pyplot as plt
from functions import *
from Malvar import Malvar
from skimage.metrics import peak_signal_noise_ratio


if __name__ == '__main__':
    # getting the original and the bayer image
    bayer_array, original = add_bayer_filter()
    w, h, c = bayer_array.shape
    r_Malvar = bayer_array.copy()
    r_bi = bayer_array.copy()
    # plotting the individual images (original, bayer, bilinear interpolation, Malvar interpolation)
    fig = plt.figure()
    ax = fig.add_subplot(1, 4, 1)
    img_plot = plt.imshow(original)
    ax = fig.add_subplot(1, 4, 2)
    img_plot = plt.imshow(bayer_array)
    result_bi = bilinear_interpolation(r_bi)  # comment this out for just the original, bayer and malvar image
    ax = fig.add_subplot(1, 4, 3)             # for it to work change the middle number to 3
    img_plot = plt.imshow(result_bi)
    result_Malvar = Malvar(r_Malvar, w, h)
    ax = fig.add_subplot(1, 4, 4)
    img_plot = plt.imshow(result_Malvar)
    # comment/uncomment these to show PSNR values of the interpolations

    print(peak_signal_noise_ratio(original, result_bi))
    print(peak_signal_noise_ratio(original, result_Malvar))

    plt.show()
    # plot for the absolute difference of the original and the Malvar image multiplied three times
    absdiff = 3*np.abs(original.astype(np.int8) - result_Malvar.astype(np.int8))
    fig = plt.imshow(absdiff)
    plt.show()
