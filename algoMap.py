from __future__ import print_function
from implementationPath import *

def GetAstarPath(fromA, toB, content):
    diagram = GridWithWeights(len(content[0]), len(content))
    for y in range(0, len(content)):
        for x in range(0, len(content[y])):
            if (content[x][y] == '_' or (toB[0] == x and toB[1] == y)):
                diagram.weights[(x,y)] = 1
            elif (content[x][y] == 'W' or content[x][y] == 'H' or content[x][y] == 'L' or content[x][y] == 'S'
                  or content[x][y] == 'P' or content[x][y] == 'X' or content[x][y] == 'R'):
                diagram.walls.append((x,y))

    came_from, cost_so_far = a_star_search(diagram, fromA, toB)
    try:
        return reconstruct_path(came_from, start=fromA, goal=toB)
    except:
        return None

# fileName = "texts\map"

def MakeAndPrintPath(origine):
    for y in range(0, len(origine) - 1):
        for x in range(0, len(origine[y]) - 1):
            print(origine[y][x], end='')
        print()

# def MakeAndPrintPath(path, origine):
#     for t in path:
#         origine[t[1]][t[0]] = '@'

#     with open(fileName + "Out.txt", 'w') as f:
#         for y in range(0, len(origine)):
#             for x in range(0, len(origine[y])):
#                 f.write(origine[y][x])
#             f.write('\n')

#     os.system("start " + fileName + "Out.txt")

# with open(fileName + ".txt") as f:
#     content = [list(x.strip('\n').replace(' ', '')) for x in f.readlines()]

# contentCopy = copy.deepcopy(content)
# diagram = GridWithWeights(len(content[0]), len(content))

# print('Dijkstra')
# print()
# start_time = time.time()
# came_from, cost_so_far = dijkstra_search(diagram, fromA, toB)
# path = reconstruct_path(came_from, start=fromA, goal=toB)
# MakeAndPrintPath(path, content)
# print("Path:",len(path))
# print("%s seconds" % (time.time() - start_time))

# print()
# print('A*')
# print()

# start_time = time.time()
# came_from, cost_so_far = a_star_search(diagram, fromA, toB)
# path = reconstruct_path(came_from, start=fromA, goal=toB)
# MakeAndPrintPath(path, contentCopy)
# print("Path:",len(path))
# print("%s seconds" % (time.time() - start_time))