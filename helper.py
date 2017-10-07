from __future__ import print_function
import os
clear = lambda: os.system('cls')

def WriteMap(deserialized_map, overwritte):
    sizeX = len(deserialized_map)
    sizeY  = len(deserialized_map[0])
    tab = {}
    for x in range(0, sizeX - 1):
        for y in range(0, sizeY - 1):
            content = deserialized_map[x][y].Content
            if content == 0:
                tab[(x, y)] = '_'
            elif content == 1:
                tab[(x, y)] = '$'
            elif content == 2:
                tab[(x, y)] = 'M'
            elif content == 3:
                tab[(x, y)] = 'P'
            elif content == 4:
                tab[(x, y)] = 'W'
            elif content == 5:
                tab[(x, y)] = 'L'
            elif content == 6:
                tab[(x, y)] = 'S'
            else:
                tab[(x, y)] = 'X'
    
    if overwritte: open("test" + "Out.txt", "w")
    with open("test" + "Out.txt", "a") as f:
            for x in range(0, sizeX - 1):
                for y in range(0, sizeY - 1):
                    print (" " + tab[(x,y)] + " ", end="")
                    f.write(" " + tab[(x,y)] + " ")
                print()
                f.write('\n')
            print()
            print()
            f.write('\n')
            f.write('\n')

