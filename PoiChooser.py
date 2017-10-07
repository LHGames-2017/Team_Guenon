import structs

class PoiChooser:

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

    def deserialize_data(self, serialized_map, player, other_players):
        """
        Fonction utilitaire pour comprendre la map
        """
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
        for player_dict in other_players:
            for player_name in player_dict.keys():
                player_info = player_dict[player_name]
                p_pos = player_info["Position"]
                player_info = structs.PlayerInfo(player_info["Health"],
                                         player_info["MaxHealth"],
                                         structs.Point(p_pos["X"], p_pos["Y"]))

                self.other_players.append({player_name: player_info})
                
        return self.deserialized_map

    def computeNextTarget(self):
        pass


