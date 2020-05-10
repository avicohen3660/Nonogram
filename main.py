from tkinter import *
from tkinter import messagebox
import ctypes
from datetime import datetime as dt
import time

def getInstances():
    file = open("C:/Users/USER/Desktop/Code/nono/nonogram/instances/13.txt", "r").readlines()
    # file = open("C:/Users/USER/Desktop/nono.txt", "r").readlines()
    rows = []
    cols = []
    flag = True
    for line in file:
        if line.strip() == "#":
            flag = False
            continue

        a = line.strip().split(" ")
        a=list(map(int,a))
        if (flag):
            rows.append(a)
        else:
            cols.append(a)
    return(rows,cols)
instances = getInstances()
instances=[[[3],[5],[3,1],[2,1],[3,3,4],[2,2,7],[6,1,1],[4,2,2],[1,1],[3,1],[6],[2,7],[6,3,1],[1,2,2,1,1],[4,1,1,3],[4,2,2],[3,3,1],[3,3],[3],[2,1]],
           [[2],[1,2],[2,3],[2,3],[3,1,1],[2,1,1],[1,1,1,2,2],[1,1,3,1,3],[2,6,4],[3,3,9,1],[5,3,2],[3,1,2,2],[2,1,7],[3,3,2],[2,4],[2,1,2],[2,2,1],[2,2],[1],[1]]]

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
numberSquares = max(len(max(instances[0], key=len)),len(max(instances[1], key=len)))
size = len(instances[0])
# size=45
tSize = min(screensize)-2*40
f1 = (screensize[0]-tSize)/2
f2 = (screensize[1]-tSize)/2
ss = tSize//(numberSquares+size)
gap=ss*numberSquares
start = 0,0
end = 0,0
fillType = 0
direction=None
first = None
startedGood = False
finishedLines = [[],[]]


def round_rectangle(x1, y1, x2, y2, radius=20, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,

              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)


data = []
for i in range(size):
    a = []
    for j in range(size):
        a.append(0)
    data.append(a)


def resize(event):
    canvas.configure(width=event.width - 4, height=event.height - 4)

def close(event):
    if messagebox.askquestion("Exit", "Are you sure?", icon="warning") == "yes":
        root.withdraw()
        sys.exit()


def fillTrivialLines():
    for i in range(len(instances[0])):
        if sum(instances[0][i])+len(instances[0][i])-1==size:
            for j in range(size):
                fillSquare(j, i, 1)
            for j in range(1,len(instances[0][i])):
                fillSquare(sum(instances[0][i][:j])+j-1,i,2)
            finishedLines[0].append(i)

    for i in range(len(instances[1])):
        if sum(instances[1][i])+len(instances[1][i])-1==size:
            for j in range(size):
                fillSquare(i, j, 1)
            for j in range(1,len(instances[1][i])):
                fillSquare(i,sum(instances[1][i][:j])+j-1,2)
            finishedLines[1].append(i)


def fillSquare(x, y, fillType, b=3,xWidth=2):
    if 0 <= x < size and 0 <= y < size:
        if fillType == 1:
            canvas.create_rectangle(f1+gap+ss*(x)+b,f2+gap+ss*(y)+b,f1+gap+ss*(x+1)-b,f2+gap+ss*(y+1)-b,fill="white", outline="white")
            canvas.create_rectangle(f1+gap+ss*(x)+b,f2+gap+ss*(y)+b,f1+gap+ss*(x+1)-b,f2+gap+ss*(y+1)-b,fill="black")

            data[x][y] = 1
        elif fillType == 2:
            # a = b
            canvas.create_rectangle(f1+gap+ss*(x)+b,f2+gap+ss*(y)+b,f1+gap+ss*(x+1)-b,f2+gap+ss*(y+1)-b,fill="white",outline="white")
            canvas.create_line(f1+gap+ss*(x)+b,f2+gap+ss*(y)+b,f1+gap+ss*(x+1)-b,f2+gap+ss*(y+1)-b,width=xWidth)
            canvas.create_line(f1+gap+ss*(x+1)-b,f2+gap+ss*(y)+b,f1+gap+ss*(x)+b,f2+gap+ss*(y+1)-b,width=xWidth)
            data[x][y] = 2
        elif fillType == 0:
            # a = b
            canvas.create_rectangle(f1+gap+ss*(x)+b,f2+gap+ss*(y)+b,f1+gap+ss*(x+1)-b,f2+gap+ss*(y+1)-b,fill="white",outline="white")
            canvas.create_line(f1+gap+ss*(x)+b,f2+gap+ss*(y)+b,f1+gap+ss*(x+1)-b,f2+gap+ss*(y+1)-b,width=xWidth,fill="white")
            canvas.create_line(f1+gap+ss*(x+1)-b,f2+gap+ss*(y)+b,f1+gap+ss*(x)+b,f2+gap+ss*(y+1)-b,width=xWidth,fill="white")
            data[x][y] = 0



def mouse(event):
    fillSquare((event.x - gap - int(f1)) // ss, (event.y - gap - int(f2)) // ss)

def mousePressed(event):
    global start
    global end
    global fillType
    global first
    global startedGood
    a = (event.x - gap - int(f1)) // ss
    b = (event.y - gap - int(f2)) // ss
    if 0<=a<size and 0<=b<size:
        startedGood = True
        start = a, b
        end = start
        fillType = (data[start[0]][start[1]]+1)%3
        first = True
        fillSquare(a,b,fillType)

def mouseDragged(event):
    global end
    global start
    global first
    global direction
    if startedGood:
        a = (event.x-gap-int(f1))//ss
        b = (event.y-gap-int(f2))//ss
        nend = a, b
        if nend != start and first:
            direction = True if start[0]==nend[0] else False
            first = False

        if nend != end and nend != start:
            # print(str(nend)+"--Direction: "+str(direction)+"--First:"+str(first))
            if direction:
                fillSquare(start[0], b, fillType)
            else:
                fillSquare(a, start[1], fillType)
            end=nend

def mouseReleased(event):
    global startedGood
    startedGood = False
def getData(x=None, y=None):
    text=""
    if x is None and y is None:
        for i in range(len(data)):
            for j in range(len(data[0])):
                text+="██ " if data[j][i]==1 else "-- "
            text+="\n"
    else:
        text = data[x][y]
    return text

def setColor(event):
    cur=event.widget.find_closest(event.x, event.y)
    color="red" if canvas.itemcget(cur,"fill")=="black" else "black"
    canvas.itemconfig(cur, fill=color)

def drawTable():
    for y in range(gap, gap+size*ss+1, ss):
        w = 3 if ((y-gap)//ss) % 5 == 0 or ((y-gap)//ss) == size else 1
        canvas.create_line(f1, f2+y, f1+gap+size*ss, f2+y, width=w)
        canvas.create_line(f1+y, f2, f1+y, f2+gap+size*ss, width=w)

    l=0  #מספרים בצד
    for row in (instances[0]):
        d=-ss/2
        for item in reversed(row):
            o=canvas.create_text(f1+gap+d, f2+gap+l, anchor=NE, font=("",int(ss*2/3)), text=str(item))
            canvas.tag_bind(o, "<Button-1>", setColor)

            d-= ss if len(str(item))==1 else 1.5*ss

        l+=ss
    l=ss/2  #מספרים למעלה
    for col in (instances[1]):
        d=-ss*2/3
        for item in reversed(col):
            o=canvas.create_text(f1+gap+l, f2+gap+d, anchor=CENTER, font=("",int(ss/1.6)), text=str(item))
            canvas.tag_bind(o, "<Button-1>", setColor)

            d-=ss
        l+=ss


if __name__ == '__main__':
    root = Tk()
    root.bind('<Configure>', resize)
    canvas = Canvas(root, bg="white")
    canvas.pack()

    # canvas.create_line(0, 0, 100, 100)
    # canvas.create_oval(100, 100, 2, 2)
    # canvas.create_polygon(200, 200, 300, 300, 400, 50, 20, 300, 40, 60)





    drawTable()

    root.bind("<ButtonPress-1>", mousePressed)
    root.bind("<ButtonRelease-1>", mouseReleased)
    root.bind("<B1-Motion>", mouseDragged)
    root.bind('<Escape>', close)
    root.attributes('-fullscreen', True)

    def solve():
        now=dt.now()
        print("solving")
        fillTrivialLines()
        print("finished")

        for i in range(len(data)):  # empty rows
            if instances[0][i][0]==0:
                for k in range(len(data)):
                    fillSquare(k,i,2)
        for i in range(len(data)):  # empty cols
            if instances[1][i][0]==0:
                for k in range(len(data)):
                    fillSquare(i,k,2)
        for i in range(len(data)):  # הצמדה ימינה שמאלה
            rowNums = instances[0][i]
            for j in range(len(rowNums)):
                s=size-(sum(rowNums[j:])+len(rowNums)-j-1)
                e=sum(rowNums[:j+1])+j
                if (s<e):
                    for k in range(s,e):
                        fillSquare(k,i,1)

        for i in range(len(data)):  # הצמדה למעלה למטה
            colNums = instances[1][i]
            for j in range(len(colNums)):
                s=size-(sum(colNums[j:])+len(colNums)-j-1)
                e=sum(colNums[:j+1])+j
                if (s<e):
                    for k in range(s,e):
                        fillSquare(i,k,1)


        for i in range(len(data[0])):  #fill rows in left
            for j in range(instances[0][i][0]):
                if data[j][i] == 1:
                    for k in range(j,instances[0][i][0]):
                        fillSquare(k,i,1)
                    if j == 0:
                        fillSquare(k+1,i,2)
                    break
            # if data[instances[0][i][0]][i] == 1:
            #     fillSquare(0,i,1)
        for i in range(len(data[-1])):  #fill rows in right
            for j in range(instances[0][i][-1]):
                if data[len(data)-j-1][i] == 1:
                    for k in range(len(data)-j-1,len(data)-instances[0][i][-1]-1,-1):
                        fillSquare(k,i,1)
                    if j == 0:
                        fillSquare(k-1,i,2)
                    break
            # if data[len(data)-instances[0][i][-1]-1][i] == 1:
            #     fillSquare(len(data)-1,i,1)
        for i in range(len(data)):  #fill cols למעלה
            for j in range(instances[1][i][0]):
                if data[i][j] == 1:
                    for k in range(j,instances[1][i][0]):
                        fillSquare(i,k,1)
                    if j == 0:
                        fillSquare(i,k+1,2)
                    break

        for i in range(len(data)):  #fill cols למטה
            for j in range(instances[1][i][-1]):
                if data[i][len(data[0])-j-1] == 1:
                    for k in range(len(data[0])-j-1, len(data[0])-instances[1][i][-1]-1,-1):
                        fillSquare(i,k,1)
                    if j == 0:
                        fillSquare(i,k-1,2)
                    break

        def isFinished(nums, line):
            sum=0
            l=[]
            for i in line:
                if i == 1:
                    sum+=1
                else:
                    if sum!=0:
                        l.append(sum)
                        sum=0
            l.append(sum)

            return nums==l

        def improve(row=None, col=None):
            if row != None:
                nums=instances[0][row]
                if row not in finishedLines[0]:
                    if isFinished(nums,[i[row] for i in data]):
                        for k in range(len(data)):
                            if data[k][row] == 0:
                                fillSquare(k,row,2)
                        finishedLines[0].append(row)
                    else: #not finished
                        pass
            if col != None:
                nums=instances[1][col]
                if col not in finishedLines[1]:
                    if isFinished(nums, data[col]):
                        for k in range(len(data[col])):
                            if data[col][k] == 0:
                                fillSquare(col,k,2)
                        finishedLines[1].append(col)
                    else:  # not finished
                        pass

        print(finishedLines)
        for i in range(len(data)):
            improve(col=i)
        for i in range(len(data[0])):
            improve(row=i)


        print(dt.now()-now)
        print(finishedLines)

    root.after(0, solve)
    root.mainloop()



