from Row import Row
from Col import Col


class Board:
    def __init__(self, width, height):
        instances = [[[6,3,1,4]], [[1]]]
        self.height = height
        self.width = width
        self.rows = [Row(width, instances[0][i]) for i in range(self.height)]
        # self.cols = [Col(height, instances[1][i]) for i in range(self.width)]
