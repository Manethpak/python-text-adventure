import random
import enemies
import items
from npc import Trader

class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def intro(self):
        raise NotImplementedError("Create a subclass instead!")
    
    def modify_player(self, player):
        pass


class StartTile(MapTile):
    def intro(self):
        return """
    You find yourself in a cave with a flickering torch on the wall.
    you can make out four path, each equally as dark and foreboding.
    """


class VictoryTile(MapTile):
    def modify_player(self, player):
        player.victory = True
    
    def intro(self):
        return """
    You see a bright light in the distance...
    ... it grows as you get closer! It's sunlight!
    
    Victory is yours!
    """


class EnemyTile(MapTile):
    def __init__(self, x, y):
        r = random.random()
        if r < 0.50:
            self.enemy = enemies.Goblin()
            self.alive_text = self.enemy.alive_text
            self.dead_text = self.enemy.dead_text
        elif r < 0.70:
            self.enemy = enemies.Orge()
            self.alive_text = self.enemy.alive_text
            self.dead_text = self.enemy.dead_text
        elif r < 0.85:
            self.enemy = enemies.GiantSpider()
            self.alive_text = self.enemy.alive_text
            self.dead_text = self.enemy.dead_text
        elif r < 0.95:
            self.enemy = enemies.Werewolf()
            self.alive_text = self.enemy.alive_text
            self.dead_text = self.enemy.dead_text
        else:
            self.enemy = enemies.RockGolem()
            self.alive_text = self.enemy.alive_text
            self.dead_text = self.enemy.dead_text

        super().__init__(x, y)

    def intro(self):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text
        return text
        
    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp -= self.enemy.damage
            print(f"Enemy does {self.enemy.damage} damage. You have {player.hp} HP remaining.")


class BossTile(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.Dragon()
        self.alive_text = self.enemy.alive_text
        self.dead_text = self.enemy.dead_text
        super().__init__(x, y)

    def intro(self):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text
        return text
        
    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp -= self.enemy.damage
            print(f"Enemy does {self.enemy.damage}. You have {player.hp} HP remaining.")


class TraderTile(MapTile):
    def __init__(self, x, y):
        self.trader = Trader()
        super().__init__(x, y)
    
    def trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print(f"{i}. {item.name} - {item.value} gold")
        while True:
            user_input = input("Choose an item or press Q to exit: ")
            if user_input in ['q', 'Q']:
                return
            else:
                try:
                    choice = int(user_input)
                    to_swap = seller.inventory[choice - 1]
                    self.swap(seller, buyer, to_swap)
                except ValueError:
                    print("Invalid choice!")

    def swap(self, seller, buyer, item):
        if item.value > buyer.gold:
            print("The item is too expensive!")
            return
        seller.inventory.remove(item)
        buyer.inventory.append(item)
        seller.gold += item.value
        buyer.gold -= item.value
        print("Trade complete!")

    def check_if_trade(self, player):
        while True:
            print("Would you like to (B)uy, (S)ell, or (Q)uit?")
            user_input = input()
            if user_input in ['q', 'Q']:
                return
            elif user_input in ['b', 'B']:
                print("Available items to buy: ")
                self.trade(player, self.trader)
            elif user_input in ['s', 'S']:
                print("Available items to sell: ")
                self.trade(self.trader, player)
            else:
                print("Invalid choice!")

    def intro(self):
        return """
    A frail not-quite-human, not-quite-creature hunch in one corner of the room...
    Clinking to his gold coins. He looks willing to make a trade.
    """


class FindGoldTile(MapTile):
    def __init__(self, x, y):
        self.gold = random.randint(1, 50)
        self.gold_claimed = False
        super().__init__(x, y)
    
    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold += self.gold
            print(f"{self.gold} gold added.")

    def intro(self):
        if self.gold_claimed:
            return """
        Just another unremarkable part of the cave. You must forge onwards.
        """
        else:
            return """
        Someone has dropped some gold on the ground. It could be of use.
        """
    

class FindItemTile(MapTile):
    def __init__(self, x, y):
        r = random.random()
        if r < 0.50:
            self.item = items.Rock()
        elif r < 0.72:
            self.item = items.WaterPouch()
        elif r < 0.90:
            self.item = items.CrustyBread()
        elif r < 0.97:
            self.item = items.Dagger()
        else:
            self.item = items.HealingPotion()
        self.item_claimed = False
        super().__init__(x, y)
    
    def modify_player(self, player):
        if not self.item_claimed:
            self.item_claimed = True
            player.inventory.append(self.item)
            print(f"{self.item} has been added to your inventory.")

    def intro(self):
        if self.item_claimed:
            return """
        There exist a skeleton laying on the ground. Nothing seem to be out of place.
        """
        else:
            return """
        There seem to be a skeleton on the ground with some equipment. Must be one of the challenger.
        His equipment could be of use.
        """


world_dsl = """
|VT|BT|EN|  |FG|TT|
|  |  |FG|FG|EN|EN|
|EN|FG|EN|FI|  |FG|
|TT|EN|FG|FI|  |EN|
|EN|  |FG|EN|ST|FI|
|FI|EN|EN|FI|  |TT|
"""

world_map = []

def is_dsl_valid(dsl):
    if dsl.count("|ST|") != 1:
        return False
    if dsl.count("|VT|") == 0:
        return False
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False

    return True

tile_type_dict = {"VT": VictoryTile,
                  "EN": EnemyTile,
                  "ST": StartTile,
                  "TT": TraderTile,
                  "FG": FindGoldTile,
                  "BT": BossTile,
                  "FI": FindItemTile,
                  "  ": None}

start_tile_location = None

def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError("DSL is invalid!")

    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.split("|")
        dsl_cells = [c for c in dsl_cells if c]
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = tile_type_dict[dsl_cell]
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y
            row.append(tile_type(x, y) if tile_type else None)

        world_map.append(row)

def tile_at(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None
