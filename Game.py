from Board import Logic
from Row import Row
from Col import Col

if __name__ == '__main__':
    # logic = Logic(20,20)
    # logic.solve()
    # print(logic.board)
    r = Row(20, [6, 3, 1, 4], 0)
    print(r.improve())