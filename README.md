README file for bachelor thesis - **RAW image debayerization using deep neural network**

This zip file contains multiple folders:
- **bilinear_result_imgs** = this folder contains the result images obtained using the bilinear interpolation
- **malvar_result_imgs** = this folder contains the result images obtained using the Malvar's method
- **matlab_result_imgs** = this folder contains the result images obtained using the demosaic function in Matlab
- **menon_result_imgs** = this folder contains the result images obtained using the Menon's method
- **kodak_ground_truth** = this folder contains the original images of the Kodak data set
- **dip_bayer_filter_result_imgs** = this folder contains images obtained using the proposed method with the Bayer filter 
- **dip_random_filter_result_imgs** = this folder contains images obtained using the proposed method with the random filter 
- **dip_xtrans_filter_result_imgs** = this folder contains images obtained using the proposed method with X-Trans filter 
- **deep_image_prior_all** = contains the code and all requirements to run it

DIP folders each contain multiple other folders:
- the folder with "2000_epochs" contains the result images that were acquired after 2000 epochs of the optimization process
- the folder with "last2avg" contains the result images after the averaging of the last 2 images of the optimization process
- the folder with "last40avg" contains the result images after the averaging of the last 40 images of the optimization process
- the folder with "last50avg" contains the result images after the averaging of the last 50 images of the optimization process
- the folder with "oracle" contains the best images in terms of PNSR of the last 50 images

Tutorial to start the code in folder **deep_image_prior_all**:
