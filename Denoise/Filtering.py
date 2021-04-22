import numpy as np
import math
import cv2

class Filtering:

    def __init__(self, image, filter_name, filter_size, var=None):
        """initializes the variables of spatial filtering on an input image
        takes as input:
        image: the noisy input image
        filter_name: the name of the filter to use
        filter_size: integer value of the size of the fitler
        global_var: noise variance to be used in the Local noise reduction filter
        S_max: Maximum allowed size of the window that is used in adaptive median filter
        """

        self.image = image

        if filter_name == 'arithmetic_mean':
            self.filter = self.get_arithmetic_mean
        elif filter_name == 'geometric_mean':
            self.filter = self.get_geometric_mean
        if filter_name == 'local_noise':
            self.filter = self.get_local_noise
        elif filter_name == 'median':
            self.filter = self.get_median
        elif filter_name == 'adaptive_median':
            self.filter = self.get_adaptive_median

        self.filter_size = filter_size
        self.global_var = var
        self.S_max = 15

    def get_arithmetic_mean(self, roi):
        """Computes the arithmetic mean of the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the arithmetic mean value of the roi"""
        summation = 0
        for index in range(len(roi)):
            summation += roi[index]

        return summation / (len(roi))

    def get_geometric_mean(self, roi):
        """Computes the geometric mean for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the geometric mean value of the roi"""
        g_st = 1
        for index in range(len(roi)):
            g_st = g_st * roi[index]

        return g_st ** (1.0 / len(roi))

    def get_local_noise(self, roi):
        """Computes the local noise reduction value
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the local noise reduction value of the roi"""
        local_mean = self.get_arithmetic_mean(roi)
        local_variance = 0

        for x in range(len(roi)):
            local_variance += pow(roi[x] - local_mean, 2)
        local_variance /= len(roi) - 1

        roi.sort()

        if len(roi) % 2 == 1:
            index = (len(roi) + 1) / 2
            g = roi[int(index)]
        else:
            g = roi[int(len(roi) / 2)] + roi[int((len(roi) + 1) / 2)]
            g /= 2

        variance_frac = self.global_var / local_variance
        adjustment = g - local_mean


        return g - (variance_frac * adjustment)

    def get_median(self, roi):
        """Computes the median for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the median value of the roi"""
        roi.sort()
        if len(roi) % 2 == 1:
            index = (len(roi) + 1) / 2
            median = roi[int(index)]
        else:
            median = roi[int(len(roi) / 2)] + roi[int((len(roi) + 1) / 2)]
            median /= 2
        return median


    def get_adaptive_median_stage_B(self, Zxy, Zmin, Zmax, Zmed):

        B1 = Zxy - Zmin
        B2 = Zxy - Zmax

        if B1 > 0 and B2 < 0 :
            return Zxy
        else:
            return Zmed

    def get_adaptive_median(self, roi):
        """Computes the harmonic filter
                        takes as input:
        kernel: a list/array of intensity values
        order: order paramter for the
        returns the harmonic mean value in the current kernel"""
        size = self.filter_size
        Zxy = self.get_median(roi)
        while size < self.S_max:
            roi.sort()
            Zmin = roi[0]
            Zmax = roi[len(roi)-1]
            Zmed = self.get_median(roi)
            A1 = Zmed - Zmin
            A2 = Zmed - Zmax

            if A1 > 0 and A2 < 0:
                return self.get_adaptive_median_stage_B(Zxy, Zmin, Zmax, Zmed)
            else:
                roi = []
                size += 1
                for x in range(size + 1):
                    for y in range(size + 1):
                        roi.append(self.image[x, y])

    def filtering(self):
        """performs filtering on an image containing gaussian or salt & pepper noise
        returns the denoised image
        ----------------------------------------------------------
        Note: Here when we perform filtering we are not doing convolution.
        For every pixel in the image, we select a neighborhood of values defined by the kernal and apply a mathematical
        operation for all the elements with in the kernel. For example, mean, median and etc.

        Steps:
        1. add the necesssary zero padding to the noisy image, that way we have sufficient values to perform the operati
        ons on the pixels at the image corners. The number of rows and columns of zero padding is defined by the kernel size
        2. Iterate through the image and every pixel (i,j) gather the neighbors defined by the kernel into a list (or any data structure)
        3. Pass these values to one of the filters that will compute the necessary mathematical operations (mean, median, etc.)
        4. Save the results at (i,j) in the ouput image.
        5. return the output image

        Note: You can create extra functions as needed. For example if you feel that it is easier to create a new function for
        the adaptive median filter as it has two stages, you are welcome to do that.
        For the adaptive median filter assume that S_max (maximum allowed size of the window) is 15
        """

        padding = int(self.filter_size / 2)
        padded_image = np.zeros((len(self.image) + padding * 2, len(self.image) + padding * 2))

        output_image = np.zeros((len(self.image), len(self.image[0])))

        for x in range(1, len(self.image)):
            for y in range(1, len(self.image[0])):
                padded_image[x, y] = self.image[x, y]
        out_x = -1
        for row in range(padding, len(padded_image) - padding):
            out_x += 1
            out_y = -1
            for col in range(padding, len(padded_image[0]) - padding):
                out_y += 1
                roi_window_start_row = row - padding
                roi_window_end_row = row + padding + 1

                roi_window_start_col = col - padding
                roi_window_end_col = col + padding + 1
                roi = []

                for px in range(roi_window_start_row, roi_window_end_row - 1):
                    for py in range(roi_window_start_col, roi_window_end_col - 1):
                        roi.append(padded_image[px, py])
                output_image[out_x, out_y] = self.filter(roi)

        return output_image
