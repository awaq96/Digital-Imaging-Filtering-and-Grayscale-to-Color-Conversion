"""dip_hw4_filter.py: Starter file to run howework 4"""

#Example Usage: ./dip_hw_filter -i Lenna.png
#Example Usage: python dip_hw_filter.py -i Lenna.png


__author__  = "Pranav Mantini"
__email__ = "pmantini@uh.edu"
__version__ = "1.0.0"

import cv2
import sys
from Denoise.Filtering import Filtering
import numpy as np


def display_image(window_name, image):
    """A function to display image"""
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, image)
    cv2.waitKey(0)

def get_bipolar_noise( image, noise_proba, noise_probb):
    """ Adds bipolar noise to the image
       takes as input:
       image: the input image
       noise_proba: probability of a pixel to be noisy
       returns a noisy image"""
    noisy_image = image.copy()
    rows, cols = image.shape

    for i in range(rows):
        for j in range(cols):
            n = np.random.random()
            if n < 0.5:
                n = np.random.random()
                if n < noise_proba:
                    noisy_image[i][j] = 0
                else:
                    noisy_image[i][j] = image[i][j]
            else:
                n = np.random.random()
                if n < noise_probb:
                    noisy_image[i][j] = 255
                else:
                    noisy_image[i][j] = image[i][j]

    var = np.var(image - noisy_image)

    return noisy_image, var

def get_gaussian_noise(image, mean, var):
    """ Adds gaussian noise to the image
               takes as input:
               image: the input image
               mean: gaussian distribution mean
               var: gaussian distribution variance
               returns a noisy image"""
    x, y = image.shape[0], image.shape[1]
    sigma = var ** 0.5
    gaussian = np.random.normal(mean, sigma, (x, y))
    noisy_image = image + gaussian
    return noisy_image


def main():
    """ The main funtion that parses input arguments, calls the approrpiate
     fitlering method and writes the output image"""

    #Parse input arguments
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument("-i", "--image", dest="image",
                        help="specify the name of the image", metavar="IMAGE")
    parser.add_argument("-n", "--noise", dest="noise",
                        help="specify type of the noise to be added (gaussian, bipolar)", metavar="NOISE")
    parser.add_argument("-f", "--filter", dest="filter",
                        help="specify name of the filter (median, arithmetic_mean, local_noise, geometric_mean, adaptive_median)", metavar="FILTER")
    parser.add_argument("-s", "--filter_size", dest="filter_size",
                        help="specify the size of the filter", metavar="FILTER SIZE")
    parser.add_argument("-npa", "--noise_proba", dest="noise_proba",
                        help="specify the probability of pepper (a) noise", metavar="NRA")
    parser.add_argument("-npb", "--noise_probb", dest="noise_probb",
                        help="specify the probability of salt (b) noise", metavar="NRB")
    parser.add_argument("-mean", "--mean", dest="mean",
                        help="specify the mean parameter for th gaussian noise", metavar="MEAN")
    parser.add_argument("-v", "--var", dest="var",
                        help="specify the variance parameter for th gaussian noise", metavar="VAR")

    args = parser.parse_args()

    # Load image
    if args.image is None:
        print("Please specify the name of image")
        print("use the -h option to see usage information")
        sys.exit(2)
    else:
        image_name = args.image.split(".")[0]
        input_image = cv2.imread(args.image, 0)

    # Set noise type
    if args.noise is None:
        print("Noise not specified using default (gaussian)")
        print("use the -h option to see usage information")
        noise = 'gaussian'
    else:
        noise = args.noise

    # Set filter type
    if args.filter is None:
        print("Filter not specified using default (median)")
        print("use the -h option to see usage information")
        filter = 'median'
    elif args.filter not in ['arithmetic_mean', 'geometric_mean', 'local_noise', 'median', 'adaptive_median']:
        print("Unknown filter, using default (median)")
        print("use the -h option to see usage information")
        filter = 'median'
    else:
        filter = args.filter

    if args.filter_size is None:
        print("Filter size not specified using default (3)")
        print("use the -h option to see usage information")
        filter_size = 3
    else:
        filter_size = int(args.filter_size)
    filter_name = "%s_%s" % (filter, filter_size)
    noisy_image = input_image.copy()

    if noise == 'bipolar':
        if args.noise_proba is None:
            print("Probability of pepper noise not specified, using default (0.01)")
            print("use the -h option to see usage information")
            noise_proba = 0.01
        else:
            noise_proba = float(args.noise_proba)


        if args.noise_probb is None:
            print("Probability of salt noise not specified, using default (0.01)")
            print("use the -h option to see usage information")
            noise_probb = 0.01
        else:
            noise_probb = float(args.noise_probb)
        noise_name = "%s_%s_%s" % (noise, noise_proba, noise_probb)
        noisy_image, var = get_bipolar_noise(input_image, noise_proba, noise_probb)

    if noise == 'gaussian':
        if args.mean is None:
            print("the mean for gaussian noise is not specified, using default mean=0")
            print("use the -h option to see usage information")
            mean = 0
        else:
            mean = float(args.mean)
        if args.var is None:
            print("the var for gaussian noise is not specified, using default var=100")
            print("use the -h option to see usage information")
            var = 100
        else:
            var = float(args.var)
        noise_name = "%s_%s_%s" % (noise, mean, var)
        noisy_image = get_gaussian_noise(input_image, mean, var)

    # Clipping pixels out of bounds
    noisy_image[noisy_image > 255] = 255
    noisy_image[noisy_image < 0] = 0

    if filter == 'local_noise':
        Filter_obj = Filtering(np.array(noisy_image), filter, filter_size, var = var)
        output = Filter_obj.filtering()
    else:
        Filter_obj = Filtering(np.array(noisy_image), filter, filter_size)
        output = Filter_obj.filtering()

    # Write output file
    output_dir = 'output/'

    # Combine images
    noisy_image = np.uint8(noisy_image)
    output = np.uint8(output)
    combined_image = cv2.hconcat([noisy_image, output])
    combined_image_name = output_dir + image_name + "_" + filter_name + "_" + noise_name + ".jpg"
    cv2.imwrite(combined_image_name, combined_image)


if __name__ == "__main__":
    main()







