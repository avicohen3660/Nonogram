from Row import Row
from Col import Col


class Logic:
    def __init__(self, height, width, blocks=None):
        self.blocks = blocks
        self.blocks = {"rows": [[3],[2,2],[1,1],[2,2],[3]], "cols": [[3],[2,2],[1,1],[2,2],[3]]}
        # self.blocks = {"rows": [[6,3,1,4]], "cols": [[0 for i in range(20)]]}
        self.height = height
        self.width = width
        self.rows = [Row(width, self.blocks["rows"][i], i) for i in range(self.height)]
        self.cols = [Col(height, self.blocks["cols"][i], i) for i in range(self.width)]
        self.board = [[0 for _ in range(height)] for _ in range(width)]
        # print(len(self.board))
        # print(len(self.board[0]))
        self.queue = self.rows + self.cols

    def solve(self):
        while len(self.queue) != 0:
            current = self.queue.pop(0)
            result = current.improve()
            typeof = Row if isinstance(current, Row) else Col
            lineNumber = current.lineNumber
            for item in result:
                if typeof == Row:
                    self.board[lineNumber][item[0]] = item[1]
                    self.cols[item[0]].line[lineNumber] = item[1]
                if typeof == Col:
                    self.board[item[0]][lineNumber] = item[1]
                    self.rows[item[0]].line[lineNumber] = item[1]
