from __future__ import print_function
import os
clear = lambda: os.system('cls')

def WriteMap(deserialized_map, overwritte):
    sizeX = len(deserialized_map)
    sizeY  = len(deserialized_map[0])
    tab = [['X' for x in range(sizeX - 1)] for y in range(sizeY - 1)]

    for y in deserialized_map:
        for x in y:
            content = x.Content
            X = x.X
            Y = x.Y
            try:
                if content is not None:
                    if content == 0:
                        tab[X][Y] = '_'
                    elif content == 1:
                        tab[X][Y] = 'W'
                    elif content == 2:
                        tab[X][Y] = 'H'
                    elif content == 3:
                        tab[X][Y] = 'L'
                    elif content == 4:
                        tab[X][Y] = 'R'
                    elif content == 5:
                        tab[X][Y] = 'S'
                    elif content == 6:
                        tab[X][Y] = 'P'
            except:
                pass
        # for y in range(0, sizeY - 1):
        #     for x in range(0, sizeX - 1):
        #         print(" " + tab[x][y] + " ", end="")
        #     print()
    # if overwritte: open("test" + "Out.txt", "w")
    # with open("test" + "Out.txt", "a") as f:
    #     for y in range(0, sizeY - 1):
    #         for x in range(0, sizeX - 1):
    #             print(" " + tab[x][y] + " ", end="")
    #             f.write(" " + tab[x][y] + " ")
    #         print()
    #         f.write('\n')
    #     print()
    #     print()
    #     f.write('\n')
    #     f.write('\n')
    
    return tab
