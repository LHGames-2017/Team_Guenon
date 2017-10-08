import structs
import sys
import math
from structs import *

class POIChooser:

    def __init__(self):
        self.elements_dict = {
            structs.TileContent.Empty : [],
            structs.TileContent.Resource : [],
            structs.TileContent.House : [],
            structs.TileContent.Player : [],
            structs.TileContent.Wall : [],
            structs.TileContent.Lava : [],
            structs.TileContent.Shop : []
        }
        self.deserialized_map = None
        self.player = None
        self.other_players = None
        self.displacement_stack = []

    def deserialize_data(self, serialized_map, player, other_players):
        """
        Fonction utilitaire pour comprendre la map
        """
        self.player = player
        self.elements_dict[structs.TileContent.Empty] = []
        self.elements_dict[structs.TileContent.Resource] = []
        self.elements_dict[structs.TileContent.Player] = []
        serialized_map = serialized_map[1:]
        rows = serialized_map.split('[')
        column = rows[0].split('{')
        self.deserialized_map = [[structs.Tile() for x in range(40)] for y in range(40)]
        for i in range(len(rows) - 1):
            column = rows[i + 1].split('{')

            for j in range(len(column) - 1):
                infos = column[j + 1].split(',')
                end_index = infos[2].find('}')
                content = int(infos[0])
                x = int(infos[1])
                y = int(infos[2][:end_index])
                self.deserialized_map[i][j] = structs.Tile(content, x, y)

                self.elements_dict[content].append((x,y))

        self.other_players = []

        for players in other_players:
            player_info = players["Value"]
            p_pos = player_info["Position"]
            player_info = PlayerInfo(player_info["Health"],
                                     player_info["MaxHealth"],
                                     Point(p_pos["X"], p_pos["Y"]))

            self.other_players.append(player_info)
                
        return self.deserialized_map

    def compute_cartesian_distance(self, point1, point2):
        return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])

    def compute_coordinate_distance(self, point1, point2):
        return (point2[0] - point1[0], point2[1] - point1[1])

    def compute_next_target(self):
        next_target = (0,0)
        min_distance = sys.maxint
        for resource in self.elements_dict[structs.TileContent.Resource]:
            distance = self.compute_cartesian_distance((self.player.Position.X,self.player.Position.Y), resource)
            if distance < min_distance:
                min_distance = distance
                next_target = resource

        return next_target

    def compute_displacement(self, next_target):
        # self.displacement_stack.clear()
        del self.displacement_stack[:]
        displacement = self.compute_coordinate_distance((self.player.Position.X,self.player.Position.Y), next_target)

        if displacement[1]:

            direction_y = displacement[1] / abs(displacement[1])
            for y in range(1, abs(displacement[1]) + 1):
                self.displacement_stack.append((self.player.Position.X, self.player.Position.Y + direction_y * y))

        if displacement[0]:
            direction_x = displacement[0] / abs(displacement[0])
            for x in range(1, abs(displacement[0]) + 1):
                if len(self.displacement_stack) == 0:
                    self.displacement_stack.append((self.player.Position.X + direction_x * x, self.player.Position.Y))
                else:
                    self.displacement_stack.append((self.player.Position.X + direction_x * x, self.displacement_stack[-1][1]))

        if len(self.displacement_stack) == 0:
            return self.player.Position

        return Point(self.displacement_stack[0][0], self.displacement_stack[0][1])



