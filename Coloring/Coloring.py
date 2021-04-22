import numpy as np
import cv2
import math
import random


class Coloring:

    def get_slice(self, grey_scale_magnitude, slices):
        for range_min, range_max in slices.keys():
            if grey_scale_magnitude >= range_min and grey_scale_magnitude <= range_max:
                return slices[range_min, range_max]

    def intensity_slicing(self, image, n_slices):
        # Convert greyscale image to color image using color slicing technique.
        # takes as input:
        # image: the grayscale input image
        # n_slices: number of slices

        # Steps:

        # 1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
        # 2. Randomly assign a color to each interval
        # 3. Create and output color image
        # 4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to

        # returns colored image
        slices = dict()
        slice_value = 255 / (n_slices + 1)
        prev_end = 0
        for slice in range(1, n_slices + 1):
            slices[prev_end, prev_end + slice_value] = [random.randint(0, 255), random.randint(0, 255),
                                                        random.randint(0, 255)]
            prev_end = prev_end + slice_value

        slices[prev_end, 255] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

        output_image = np.zeros((len(image), len(image[0]), 3))

        for x in range(len(image)):
            for y in range(len(image[0])):
                output_image[x, y] = self.get_slice(image[x, y], slices)

        return output_image

    def color_transformation(self, image, n_slices, theta):
        # Convert greyscale image to color image using color transformation technique.
        # takes as input:
        # image:  grayscale input image
        # colors: color array containing RGB values

        # Steps:
        # 1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
        # 2. create red values for each slice using 255*sin(slice + theta[0])
        #    similarly create green and blue using 255*sin(slice + theta[1]), 255*sin(slice + theta[2])
        # 3. Create and output color image
        # 4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to

        # returns colored image
        slices = dict()
        slice_value = 255 / (n_slices + 1)
        prev_end = 0
        for slice in range(1, n_slices + 1):
            center = (prev_end + prev_end + slice_value) / 2
            slices[prev_end, prev_end + slice_value] = [255 * math.sin(center + theta[0]),
                                                        255 * math.sin(center + theta[1]),
                                                        255 * math.sin(center + theta[2])]
            prev_end = prev_end + slice_value

        center = (prev_end + 255) / 2
        slices[prev_end, 255] = [255 * math.sin(center + theta[0]), 255 * math.sin(center + theta[1]),
                                 255 * math.sin(center + theta[2])]

        output_image = np.zeros((len(image), len(image[0]), 3))
        for x in range(len(image)):
            for y in range(len(image[0])):
                output_image[x, y] = self.get_slice(image[x, y], slices)
        return output_image
