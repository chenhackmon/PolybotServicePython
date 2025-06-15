from pathlib import Path
from matplotlib.image import imread, imsave
import random


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        """
        Do not change the constructor implementation
        """
        self.path = Path(path)
        self.data = rgb2gray(imread(path)).tolist()

    def save_img(self):
        """
        Do not change the below implementation
        """
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        imsave(new_path, self.data, cmap='gray')
        return new_path

    def blur(self, blur_level=16):
        height = len(self.data)
        width = len(self.data[0])
        filter_size = blur_level ** 2

        result = []
        for i in range(height - blur_level + 1):
            row_result = []
            for j in range(width - blur_level + 1):
                sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]
                average = sum(sum(sub_row) for sub_row in sub_matrix) / filter_size  # Changed // to /
                row_result.append(average)
            result.append(row_result)

        self.data = result

    def contour(self):
        for i, row in enumerate(self.data):
            res = []
            for j in range(1, len(row)):
                res.append(abs(row[j - 1] - row[j]))
            self.data[i] = res

    def rotate(self):
        self.data = [list(reversed(col)) for col in zip(*self.data)]

    def salt_n_pepper(self):
        height = len(self.data)
        width = len(self.data[0])
        total_pixels = height * width
        salt_amount = int(0.15 * total_pixels)
        pepper_amount = int(0.15 * total_pixels)

        # הוסף פיקסלים לבנים (salt)
        for _ in range(salt_amount):
            i = random.randint(0, height - 1)
            j = random.randint(0, width - 1)
            self.data[i][j] = 1.0

        # הוסף פיקסלים שחורים (pepper)
        for _ in range(pepper_amount):
            i = random.randint(0, height - 1)
            j = random.randint(0, width - 1)
            self.data[i][j] = 0.0

    def concat(self, other_img, direction='horizontal'):
        if direction == 'horizontal':
            min_height = min(len(self.data), len(other_img.data))
            new_data = [
                self.data[i][:] + other_img.data[i][:]
                for i in range(min_height)
            ]
        else:  # vertical
            min_width = min(len(self.data[0]), len(other_img.data[0]))
            new_data = [
                row[:min_width] for row in self.data
            ] + [
                row[:min_width] for row in other_img.data
            ]
        self.data = new_data

    def segment(self):
        threshold = 0.5
        self.data = [[1.0 if pixel > threshold else 0.0 for pixel in row] for row in self.data]
