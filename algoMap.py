from implementationPath import *
import time
import copy
import os

fileName = "texts\map"

def MakeAndPrintPath(path, origine):
    for t in path:
        origine[t[1]][t[0]] = '@'

    with open(fileName + "Out.txt", 'w') as f:
        for y in range(0, len(origine)):
            for x in range(0, len(origine[y])):
                f.write(origine[y][x])
            f.write('\n')

    os.system("start " + fileName + "Out.txt")

with open(fileName + ".txt") as f:
    content = [list(x.strip('\n').replace(' ', '')) for x in f.readlines()]

contentCopy = copy.deepcopy(content)
diagram = GridWithWeights(len(content[0]), len(content))

for y in range(0, len(content)):
    for x in range(0, len(content[y])):
        if (content[y][x] == '.'):
            diagram.weights[(x,y)] = 1
        elif (content[y][x] == '*'):
            diagram.weights[(x,y)] = 5
        elif (content[y][x] == '#'):
            diagram.walls.append((x,y))
        elif (content[y][x] == 'A'):
            diagram.weights[(x,y)] = 0
            fromA = (x,y)
        elif (content[y][x] == 'B'):
            diagram.weights[(x,y)] = 0
            toB = (x,y)
        else:
            allo = content[y][x]
            print(allo)

print('Dijkstra')
print()
start_time = time.time()
came_from, cost_so_far = dijkstra_search(diagram, fromA, toB)
path = reconstruct_path(came_from, start=fromA, goal=toB)
MakeAndPrintPath(path, content)
print("Path:",len(path))
print("%s seconds" % (time.time() - start_time))

print()
print('A*')
print()

start_time = time.time()
came_from, cost_so_far = a_star_search(diagram, fromA, toB)
path = reconstruct_path(came_from, start=fromA, goal=toB)
MakeAndPrintPath(path, contentCopy)
print("Path:",len(path))
print("%s seconds" % (time.time() - start_time))