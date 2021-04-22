"""dip_hw5_color.py: Starter file to run howework 5"""

#Example Usage: ./dip_hw_color -i image -n n_slices _c colors
#Example Usage: python dip_hw_color.py -i image -n n_slices _c colors


import cv2
import sys
from Coloring.Coloring import Coloring
from datetime import datetime
import numpy as np


def display_image(window_name, image):
    """A function to display image"""
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, image)
    cv2.waitKey(0)


def main():
    """ The main funtion that parses input arguments, calls the approrpiate
      method and writes the output image"""

    #Parse input arguments
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument("-i", "--image", dest="image",
                        help="specify the name of the image", metavar="IMAGE")
    parser.add_argument("-n", "--n_slices", dest="n_slices",
                        help="specify the number of slices to use", metavar="SLICES")
    parser.add_argument("-t1", "--theta1", dest="theta1",
                        help="specify theta1", metavar="THETA1", type=int)
    parser.add_argument("-t2", "--theta2", dest="theta2",
                        help="specify theta2", metavar="THETA2", type=int)
    parser.add_argument("-t3", "--theta3", dest="theta3",
                        help="specify theta3", metavar="THETA3", type=int)
    args = parser.parse_args()

    #Load image
    if args.image is None:
        print("Please specify the name of image")
        print("use the -h option to see usage information")
        sys.exit(2)
    else:
        image_name = args.image.split(".")[0]
        input_image = cv2.imread(args.image, 0)


    if args.n_slices is None:
        print("Number of slicing planes not specified using default (3)")
        print("use the -h option to see usage information")
        n_slices = '3'
    else:
        n_slices = int(args.n_slices)

    if  args.theta1 is None or args.theta2 is None or args.theta3 is None:
        theta = (10, 50, 170)
        print("All there phase value have to be specified, not specified using default - ", theta)
        print("use the -h option to see usage information")
    else:
        theta = (args.theta1, args.theta2, args.theta3)

    theta_name = "%s_%s_%s" % theta
    input_image = cv2.GaussianBlur(input_image,(3,3),cv2.BORDER_DEFAULT)
 
    Color_obj = Coloring()
    color_slicing_output = Color_obj.intensity_slicing(input_image, n_slices)


    color_transforming_output=Color_obj.color_transformation(input_image, n_slices, theta)

    #Write output file
    output_dir = 'output/'

    output_image_name = output_dir+image_name+"_"+str(n_slices)+"_sliced_image"+".jpg"
    cv2.imwrite(output_image_name, color_slicing_output)
    output_image_name_t = output_dir + image_name + "_color_transformed_image_"+ theta_name + ".jpg"
    cv2.imwrite(output_image_name_t, color_transforming_output)


if __name__ == "__main__":
    main()







