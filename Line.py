class Line:
    def __init__(self, length, blocks, ln):
        self.length = length  # אורך השורה
        self.line = [0 for _ in range(length)]
        self.lineNumber = ln
        self.blocks = blocks  # הבלוקים
        self.numOfBlocks = len(blocks)  # מספר הבלוקים
        self.delta = length - (sum(self.blocks) + self.numOfBlocks - 1)  # ההפרש בין אורך השורה למילוי הבלוקים
        self.pos = self.__getPos()
        self.blocksLimits = self.__getBlocksLimits()
        # [print(self.pos[i]) for i in range(self.length)]

    def __getPos(self):
        pos = [[] for _ in range(self.length)]
        for i in range(self.numOfBlocks):
            for j in range(sum(self.blocks[:i]) + i, self.length - (sum(self.blocks[i + 1:]) + self.numOfBlocks - i - 1)):
                pos[j].append(i)
        return pos

    def __getBlocksLimits(self):
        arr = []
        for i in range(self.numOfBlocks):
            arr.append((sum(self.blocks[:i]) + i, self.length - (sum(self.blocks[i + 1:]) + self.numOfBlocks - i)))
        return arr
    def trivial(self):
        arr=[]
        if self.blocks == [0]:
            arr+= [(i, 2) for i in range(self.length)]
        if self.delta == 0:
            for i in range(self.length):
                if len(self.pos[i]) == 1:
                    arr.append((i,1))
                else:
                    arr.append((i,2))
        return arr

    def overlap(self):
        arr = []
        for i in range(self.numOfBlocks):
            stend = self.blocksLimits[i]
            curBlock = self.blocks[i]
            # print((stend-curBlock,stend+curBlock))
            for j in range(stend[1]-curBlock+1,stend[0]+curBlock):
                arr.append((j,1))
        return arr

    def improve(self):
        whatChanged = []
        # whatChanged += self.trivial()
        whatChanged += self.overlap()
        #דחוף: לעדכן את pos
        return whatChanged
