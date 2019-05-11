"""Module defines the TimeBoxImage class. """


class TimeBoxImage:
    """ An image to be display on the TimeBox """
    width = 11
    height = 11
    image = 0

    gamma_value = None
    gamma_table = None

    def __init__(self, height=11, width=11):
        self.height = height
        self.width = width
        self.image = \
            [[[0 for c in range(3)] for x in range(self.width)] for y in range(self.height)]

    def _gamma_correction(self, k):
        """ Determine the pixel value for pixel with brightness k, 0<=k<256, considering gamma."""

        return int(256.0*pow((k/256.0), 1.0 / self.gamma_value)) >> 4

    def set_gamma(self, new_gamma):
        """ Change the gamma value. Reocomputa the table."""
        if self.gamma_value != new_gamma:
            self.gamma_value = new_gamma
            self.gamma_table = dict()
            for k in range(256):
                self.gamma_table[k] = self._gamma_correction(k)

    def get_pixel_data(self, xix, yix, cix):
        """ return value of pixel (xix, yix) nd color c (0..2) """
        return self.image[yix][xix][cix]

    def put_pixel(self, xix, yix, rval, gval, bval):
        """Set a pixel in the image."""
        self.image[yix][xix][0] = rval
        self.image[yix][xix][1] = gval
        self.image[yix][xix][2] = bval

    def put_pixel_gamma(self, xix, yix, rval, gval, bval):
        """Set a pixel in the image, applying gamma correction.
        Values between 0 and 255."""
        self.image[yix][xix][0] = self.gamma_table[rval]
        self.image[yix][xix][1] = self.gamma_table[gval]
        self.image[yix][xix][2] = self.gamma_table[bval]
