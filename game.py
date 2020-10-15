from player import Player
import world
from collections import OrderedDict

def play():
    print("Challenge and beat the legendary Dragon!")
    world.parse_world_dsl()
    player = Player()
    while player.is_alive() and not player.victory:
        room = world.tile_at(player.x, player.y)
        print(room.intro())
        room.modify_player(player)
        if player.is_alive() and not player.victory:
            choose_action(room, player)
        elif not player.is_alive():
            print("Your journey has come to an early end!")
        
def choose_action(room, player):
    action = None
    while not action:
        available_actions = get_available_actions(room, player)
        action_input = input("Action: ")
        print("==================================")
        action = available_actions.get(action_input)
        if action:
            action()
        else:
            print("Invalid action!")

def get_available_actions(room, player):
    actions = OrderedDict()
    print("Choose an action: ")
    if player.inventory:
        action_adder(actions, 'i', player.print_invetory, "Print inventory")
    if isinstance(room, world.TraderTile):
        action_adder(actions, 't', player.trade, "Trade")    
    if isinstance(room, world.EnemyTile or world.BossTile) and room.enemy.is_alive():
        action_adder(actions, 'e', player.attack, "Attack")
    else:
        if world.tile_at(room.x, room.y - 1):
            action_adder(actions, 'w', player.move_up, "Go Up")
        if world.tile_at(room.x, room.y + 1):
            action_adder(actions, 's', player.move_down, "Go Down")
        if world.tile_at(room.x + 1, room.y):
            action_adder(actions, 'd', player.move_right, "Go Right")
        if world.tile_at(room.x - 1, room.y):
            action_adder(actions, 'a', player.move_left, "Go Left")
    if player.hp < 100:
        action_adder(actions, 'h', player.heal, "Heal")
    
    return actions

def action_adder(action_dict, hotkey, action, name):
    action_dict[hotkey.lower()] = action
    action_dict[hotkey.upper()] = action
    print(f"{hotkey}: {name}")
    
play()