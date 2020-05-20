class Line:
    def __init__(self, length, blocks):
        self.length = length  # אורך השורה
        self.line = [0 for _ in range(length)]
        self.blocks = blocks  # הבלוקים
        self.numOfBlocks = len(blocks)  # מספר הבלוקים
        self.delta = length - (sum(self.blocks) + self.numOfBlocks - 1)  # ההפרש בין אורך השורה למילוי הבלוקים
        self.pos = self.getPos()

    def getPos(self):
        pos = [[] for _ in range(self.length)]
        for i in range(self.numOfBlocks):
            for j in range(sum(self.blocks[:i]) + i, self.length - (sum(self.blocks[i + 1:]) + self.numOfBlocks - i - 1)):
                pos[j].append(i)
        return pos
