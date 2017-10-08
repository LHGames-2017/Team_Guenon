from flask import Flask, request
from structs import *
import json
import numpy
from helper import *
from algoMap import *
from POIChooser import *

global current_state
current_state = "GO-Mining" #states = GO-Home - GO-Mining - Mining - GO-Buying - Buying

global upgrade_priority #Changer les upgrades/items
upgrade_priority = ['Backpack', 'pick-up-speed-1', 'Defence-1', 'MaximumHealth-1',
                    'Pick-axe', 'Shield', 'Defence-2', 'CarryingCapacity-1',
                    'CarryingCapacity-2']
overwritte = True
app = Flask(__name__)

def create_action(action_type, target):
    actionContent = ActionContent(action_type, target.__dict__)
    return json.dumps(actionContent.__dict__)

def create_move_action(target):
    return create_action("MoveAction", target)

def create_attack_action(target):
    return create_action("AttackAction", target)

def create_collect_action(target, carryingCapacity, carriedResources):
    if carryingCapacity == carriedResources :
        current_state = 'GO-Home'
    else:
        current_state = 'Mining'
        return create_action("CollectAction", target)

def create_steal_action(target):
    return create_action("StealAction", target)

def create_heal_action():
    return create_action("HealAction", "")

def create_purchase_action():
    current_state = 'GO-mining'
    item = upgrade_priority[0]
    upgrade_priority.pop(0)
    return create_action("PurchaseAction", item)

def deserialize_map(serialized_map):
    """
    Fonction utilitaire pour comprendre la map
    """
    serialized_map = serialized_map[1:]
    rows = serialized_map.split('[')
    column = rows[0].split('{')
    deserialized_map = [[Tile() for x in range(40)] for y in range(40)]
    for i in range(len(rows) - 1):
        column = rows[i + 1].split('{')

        for j in range(len(column) - 1):
            infos = column[j + 1].split(',')
            end_index = infos[2].find('}')
            content = int(infos[0])
            x = int(infos[1])
            y = int(infos[2][:end_index])
            deserialized_map[i][j] = Tile(content, x, y)

    return deserialized_map

poiChooser = POIChooser()

def bot():
    """
    Main de votre bot.
    """
    global current_state
    map_json = request.form["map"]

    # Player info

    encoded_map = map_json.encode()
    map_json = json.loads(encoded_map)
    # test = json.dumps(map_json, indent=3, sort_keys=True)
    print(json.dumps(map_json, indent=3, sort_keys=True))
    p = map_json["Player"]
    print "player:{}".format(p)
    pos = p["Position"]
    x = pos["X"]
    y = pos["Y"]
    print(x, y)
    deserialized_house = p["HouseLocation"]
    house = Point(int(deserialized_house['X']), int(deserialized_house['Y']))
    player = Player(p["Health"], p["MaxHealth"], Point(x,y),
                    Point(deserialized_house["X"], deserialized_house["Y"]), p["Score"],
                    p["CarriedResources"], p["CarryingCapacity"])

    # Map
    serialized_map = map_json["CustomSerializedMap"]
    deserialized_map = poiChooser.deserialize_data(serialized_map, player, map_json["OtherPlayers"])
    # print(deserialized_map)

    global overwritte
    mapContent = WriteMap(deserialized_map, overwritte)
    overwritte = False

    target = Point(0,0)
    if player.CarriedRessources == player.CarryingCapacity:
        current_state = "GO-Home"

    if current_state == 'GO-Home':
        position = house  # position de la maison  # mining - fonction de nick et julien
        if not position == player.Position and poiChooser.compute_cartesian_distance((position.X, position.Y), (player.Position.X, player.Position.Y)) != 0:
            path = GetAstarPath((x, y), (position.X, position.Y), mapContent)
            target = Point(path[1][0], path[1][1])
            return create_move_action(target)
        else:
            current_state = 'GO-Mining'
            # check si assez argent pour get items

    elif current_state == 'GO-Mining':
        position = poiChooser.compute_next_target()  # mining - fonction de nick et julien
        if poiChooser.compute_cartesian_distance(position, (player.Position.X, player.Position.Y)) != 1:
            path = GetAstarPath((x, y), position, mapContent)
            target = Point(path[1][0], path[1][1])
            return create_move_action(target)
        else:
            current_state = 'Mining'

    elif current_state == 'GO-Buying':
        position = None  # positon du shop  # mining - fonction de nick et julien
        if not position == player.Position:
            path = GetAstarPath((x, y), position, mapContent)
            target = Point(path[1][0], path[1][1])
            return create_move_action(target)
        else:
            current_state = 'Buying'

    elif current_state == 'Mining':
        target = poiChooser.compute_next_target()
        return create_collect_action(Point(target[0], target[1]), player.CarryingCapacity, player.CarriedRessources)

    if current_state == 'Buying':
        return create_purchase_action()

    # path = GetAstarPath((x,y), target, mapContent)
    # return create_move_action(Point(path[1][0], path[1][1]))

@app.route("/", methods=["POST"])
def reponse():
    """
    Point d'entree appelle par le GameServer
    """
    return bot()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug = True)
