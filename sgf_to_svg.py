from math import sin, cos, pi, sqrt
import goban

# filename = "../GoExplainer/review-1133622.sgf"
# filename = "../GoExplainer/markers.sgf"

alphabet = "abcdefghijklmnopqrstuvwxyz"
TRI = 4
SQUARE = 2 * 4
CIRCLE = 3 * 4
CROSS = 5 * 4
TEXT = 6 * 4

SHOW_COORDINATES = False
BACKGROUND = True
BACKGROUNDSMALL = False

filename = input("path to sgf: ")


wholestring = ""
properties = []
readproperty = True
p = ""
prop = ""
arg = ""
parent = -1
stack = []
children = {-1: []}
with open(filename, 'r') as file:
    for line in file.readlines():
        for c in line.strip():
            if c != ";":
                if c == "[":
                    readproperty = False
                    if p != "":
                        prop = p
                    p = ""
                elif c == "]":
                    readproperty = True
                    arg = p
                    p = ""
                    properties += [(prop, arg, parent)]
                    children[parent] += [len(properties) - 1]
                    children[len(properties) - 1] = []
                    parent = len(properties) - 1
                elif c == "(":
                    stack += [parent]
                elif c == ")":
                    parent = stack[-1]
                    stack.pop()
                else:
                    p += str(c)

pathstoleafes = []
for i in range(len(properties)):
    node = i
    if len(children[node]) == 0:
        invpath = [node]
        while properties[node][2] != -1:
            invpath += [properties[node][2]]
            node = properties[node][2]
            # print(node)
        path = [invpath[len(invpath) - 1 - i] for i in range(len(invpath))]
        pathstoleafes += [path]


# while len(children[node]) > 0:
#     if len(children[node]) == 1:
#         node = children[node][0]
#     else:
#         # for n in range(len(children[node])):
#         #     prop, arg, _ = properties[children[node][n]]
#         #     print(f"{n}: {prop}[{arg}]")
#         # nextnode = input()
#         node = children[node][nextnode]
#         varcount += 1

varcount = 0
for path in pathstoleafes:
    size = 0
    board = [[]]
    actualboard = None
    texts = {}
    for node in path:
        prop, arg, _ = properties[node]
        if prop == "SZ":
            size = int(arg)
            board = [[0 for i in range(size)] for i in range(size)]
            actualboard = goban.goban(size)
        if (prop == "W" and len(arg) == 2):
            coords = (alphabet.index(arg[0]), alphabet.index(arg[1]))
            board[coords[0]][coords[1]] = 2
            actualboard.makemove(2, coords[0], coords[1])
            texts = {}
        if prop == "AW":
            coords = (alphabet.index(arg[0]), alphabet.index(arg[1]))
            board[coords[0]][coords[1]] = 2
            actualboard.makemove(2, coords[0], coords[1], False)
            texts = {}
        if (prop == "B" and len(arg) == 2):
            coords = (alphabet.index(arg[0]), alphabet.index(arg[1]))
            board[coords[0]][coords[1]] = 1
            actualboard.makemove(1, coords[0], coords[1])
            texts = {}
        if prop == "AB":
            coords = (alphabet.index(arg[0]), alphabet.index(arg[1]))
            board[coords[0]][coords[1]] = 1
            actualboard.makemove(1, coords[0], coords[1],False)
            texts = {}
        if prop == "AE":
            coords = (alphabet.index(arg[0]), alphabet.index(arg[1]))
            board[coords[0]][coords[1]] = 0
            actualboard.remove(coords[0],coords[1])
            texts = {}
        if prop == "TR":
            coords = (alphabet.index(arg[0]), alphabet.index(arg[1]))
            board[coords[0]][coords[1]] &= 3
            board[coords[0]][coords[1]] |= TRI
        if prop == "SQ":
            coords = (alphabet.index(arg[0]), alphabet.index(arg[1]))
            board[coords[0]][coords[1]] &= 3
            board[coords[0]][coords[1]] |= SQUARE
        if prop == "CR":
            coords = (alphabet.index(arg[0]), alphabet.index(arg[1]))
            board[coords[0]][coords[1]] &= 3
            board[coords[0]][coords[1]] |= CIRCLE
            # print(coords)
        if prop == "MA":
            coords = (alphabet.index(arg[0]), alphabet.index(arg[1]))
            board[coords[0]][coords[1]] &= 3
            board[coords[0]][coords[1]] |= CROSS
            # print(coords)
        if prop == "LB":
            coords = (alphabet.index(arg[0]), alphabet.index(arg[1]))
            board[coords[0]][coords[1]] &= 3
            board[coords[0]][coords[1]] |= TEXT
            texts[(coords[0], coords[1])] = arg.split(":")[1]
            print(coords)
        # print(
        #     f"{node} : {properties[node][0]} : {properties[node][1]} Children: {children[node]}")

    # print(f"size = {size}")

    outfile = filename[:-4] + "_" + f"{varcount}" + ".svg"

    svg = open(outfile, 'w')
    svg.write(f'<svg height="{50 * size}" width="{50 * size}"  version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">\n')
    svg.write('<defs> <filter id="f1" x="-0.1212" y="-0.1212" width="1.2424" height="1.2424" xmlns="http://www.w3.org/2000/svg"><feGaussianBlur in="SourceGraphic" stdDeviation="6.8730779" /> </filter> </defs>\n')
    if BACKGROUND:
        if BACKGROUNDSMALL:
            svg.write(
            f'<polygon points="{25},{25}, {25}, {50 * (size) - 25},{50 * (size) - 25},{50 * (size) - 25},{50 * (size) - 25},{25}" style="fill:burlywood;stroke:none" />\n')
        else:
            svg.write(
            f'<polygon points="{0},{0}, {0}, {50 * (size)},{50 * (size)},{50 * (size)},{50 * (size)},{0}" style="fill:burlywood;stroke:none" />\n')
    for i in range(1, size - 1):
        stroke = 2
        svg.write(
            f'<line x1="{50 * (i + 0.5)}" y1="{25}" x2="{50 * (i + 0.5)}" y2="{size * 50 - 25}" style="stroke:black;stroke-width:{stroke}" />\n')
        svg.write(
            f'<line x1="{25}" y1="{50 * (i + 0.5)}" x2="{size * 50 - 25}" y2="{50 * (i + 0.5)}" style="stroke:black;stroke-width:{stroke}" />\n')

    svg.write(
        f'<polygon points="{25},{25}, {25}, {50 * (size - 0.5)},{50 * (size - 0.5)},{50 * (size - 0.5)},{50 * (size - 0.5)},{25}" style="fill:none;stroke:black;stroke-width:4" />\n')
    for row in range(size):
        for col in range(size):
            x = 50 * (row + 0.5)
            y = 50 * (col + 0.5)
            stone = actualboard.GetBoard(row,col)#board[row][col] & 3
            color = "black"
            if stone == 1:
                color = "black"
            if stone == 2:
                color = "white"
            if stone != 0:
                svg.write(
                    f'<circle r="{24}" cx="{x}" cy="{y}" fill="{color}" stroke="black" stroke-width="2"/>\n')
            marker = board[row][col] & (255 * 4)
            if marker != 0 and stone == 0:
                xs = [x + 30 * sin(2 * pi * (i + 0.5)/4) for i in range(4)]
                ys = [y + 30 * cos(2 * pi * (i + 0.5)/4) for i in range(4)]
                if BACKGROUND:
                    svg.write(
                    f'<polygon points="{xs[0]},{ys[0]}, {xs[1]},{ys[1]},{xs[2]},{ys[2]},{xs[3]},{ys[3]}" style="fill:burlywood;stroke:none;opacity:0.75" filter="url(#f1)"/>\n')
                else:
                    svg.write(
                    f'<polygon points="{xs[0]},{ys[0]}, {xs[1]},{ys[1]},{xs[2]},{ys[2]},{xs[3]},{ys[3]}" style="fill:white;stroke:none;opacity:0.75" filter="url(#f1)"/>\n')
            if marker == TRI:
                color = "black"
                if stone == 1:
                    color = "white"
                xs = [x + 15 * sin(2 * pi * i/3) for i in range(3)]
                ys = [y + 15 * cos(2 * pi * i/3) for i in range(3)]
                svg.write(
                    f'<polygon points="{xs[0]},{ys[0]}, {xs[1]},{ys[1]},{xs[2]},{ys[2]}" style="fill:none;stroke:{color};stroke-width:3" />\n')
            if marker == SQUARE:
                color = "black"
                if stone == 1:
                    color = "white"
                xs = [x + 15 * sin(2 * pi * (i + 0.5)/4) for i in range(4)]
                ys = [y + 15 * cos(2 * pi * (i + 0.5)/4) for i in range(4)]
                svg.write(
                    f'<polygon points="{xs[0]},{ys[0]}, {xs[1]},{ys[1]},{xs[2]},{ys[2]},{xs[3]},{ys[3]}" style="fill:none;stroke:{color};stroke-width:3" />\n')
            if marker == CIRCLE:
                color = "black"
                if stone == 1:
                    color = "white"
                svg.write(
                    f'<circle r="{15}" cx="{x}" cy="{y}" fill="none" stroke="{color}" stroke-width="3"/>\n')
            if marker == CROSS:
                color = "black"
                if stone == 1:
                    color = "white"
                svg.write(
                    f'<line x1="{x - 15/sqrt(2)}" y1="{y -15/sqrt(2)}" x2="{x + 15/sqrt(2)}" y2="{y + 15/sqrt(2)}" style="stroke:{color};stroke-width:3" />\n')
                svg.write(
                    f'<line x1="{x - 15/sqrt(2)}" y1="{y + 15/sqrt(2)}" x2="{x + 15/sqrt(2)}" y2="{y - 15/sqrt(2)}" style="stroke:{color};stroke-width:3" />\n')
            if marker == TEXT:
                color = "black"
                if stone == 1:
                    color = "white"
                svg.write(
                    f' <text x="{x - 10}" y="{y + 10}" fill="{color}" stroke="none" font-size="30">{texts[(row, col)]}</text>\n')

    svg.write(f'</svg>')
    varcount += 1
    svg.close()
