import numpy as np


class File:
    def __init__(self, data):
        self.data = np.array(data)

    def split(self, d, p):
        left_data = []
        right_data = []

        for x in self.data:
            if x[d] <= p:
                left_data.append(x)
            else:
                right_data.append(x)

        return File(left_data), File(right_data)

    def __str__(self):
        return str(self.data)
