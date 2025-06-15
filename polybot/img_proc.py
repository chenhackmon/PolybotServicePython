from pathlib import Path
from matplotlib.image import imread, imsave
import numpy as np
import random


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        self.path = Path(path)
        img = imread(path)
        self.data = rgb2gray(img)  # numpy array float64

    def save_img(self):
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        imsave(new_path, self.data, cmap='gray')
        return new_path

    def blur(self, blur_level=16):
        height, width = self.data.shape
        filter_size = blur_level ** 2

        result = []
        for i in range(height - blur_level + 1):
            row_result = []
            for j in range(width - blur_level + 1):
                sub_matrix = self.data[i:i + blur_level, j:j + blur_level]
                average = np.sum(sub_matrix) / filter_size
                row_result.append(average)
            result.append(row_result)

        self.data = np.array(result)

    def contour(self):
        # compute abs diff horizontally
        self.data = np.abs(np.diff(self.data, axis=1))

    def rotate(self):
        # Rotate 90 degrees clockwise
        self.data = np.rot90(self.data, k=3)

    def salt_n_pepper(self):
        height, width = self.data.shape
        total_pixels = height * width
        salt_amount = int(0.15 * total_pixels)
        pepper_amount = int(0.15 * total_pixels)

        # Salt (white pixels)
        for _ in range(salt_amount):
            i = random.randint(0, height - 1)
            j = random.randint(0, width - 1)
            self.data[i, j] = 1.0

        # Pepper (black pixels)
        for _ in range(pepper_amount):
            i = random.randint(0, height - 1)
            j = random.randint(0, width - 1)
            self.data[i, j] = 0.0

        # בדיקה - כמה פיקסלים לבנים יש בפועל
        white_pixels = np.sum(self.data > 0.99)
        white_percentage = white_pixels / total_pixels
        print(f"White pixels added: {white_pixels} out of {total_pixels} ({white_percentage:.2%})")

    def concat(self, other_img, direction='horizontal'):
        if direction == 'horizontal':
            min_height = min(self.data.shape[0], other_img.data.shape[0])
            new_data = np.hstack((self.data[:min_height, :], other_img.data[:min_height, :]))
        else:
            min_width = min(self.data.shape[1], other_img.data.shape[1])
            new_data = np.vstack((self.data[:, :min_width], other_img.data[:, :min_width]))

        self.data = new_data

    def segment(self):
        threshold = 0.5
        self.data = np.where(self.data > threshold, 1.0, 0.0)
