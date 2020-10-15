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
    The dungeon of the Mythical Beast. It is said that the Black Dragon, the beast that once ruled the continent,
    had lay its nest deep inside a dungeon rooted within the tallest mountain existed on this continent,
    according to the tale of Black Beast that has been passed down for centuries.
    The tale told, that treasure worth a million gold is residing deep within the lair.
    Many challenger had entered the dungeon. Only to never return home.
    This time, you had decided to challenge the dungeon...
    Whether you will be able to step out victorious, or you will never return home
    The tale of a new hero began.
    """


class VictoryTile(MapTile):
    def modify_player(self, player):
        player.victory = True
    
    def intro(self):
        return """
    You see a bright shining light in the distance...
    ... as you entered the room, A giant opening from the ceiling direct the sunlight into the room
    Directly under the sunlight, a hoard of treasure could be seen.
    
    Victory is your!!!
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
        while True:
            for i, item in enumerate(seller.inventory, 1):
                print(f"{i}. {item.name} - {item.value} gold")
            user_input = input("Choose an item or press Q to exit: ")
            if user_input in ['q', 'Q']:
                return
            else:
                try:
                    choice = int(user_input)
                    to_swap = seller.inventory[choice - 1]
                    self.swap(seller, buyer, to_swap)
                except ValueError or IndexError:
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
        print("==================================")

    def check_if_trade(self, player):
        while True:
            print("Would you like to (B)uy, (S)ell, or (Q)uit?")
            user_input = input()
            if user_input in ['q', 'Q']:
                return
            elif user_input in ['b', 'B']:
                print(f"You have {player.gold} gold in your pocket.")
                print("Available items to buy: ")
                self.trade(player, self.trader)
            elif user_input in ['s', 'S']:
                print(f"You have {player.gold} gold in your pocket.")
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
        if r < 0.40:
            self.item = items.Rock()
        elif r < 0.65:
            self.item = items.WaterPouch()
        elif r < 0.80:
            self.item = items.CrustyBread()
        elif r < 0.90:
            self.item = items.Dagger()
        elif r < 0.96:
            self.item = items.HealingPotion()
        else:
            self.item = items.RustySword()
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


class EmptyTile(MapTile):
    def intro(self):
        return """
    The cave chamber seem empty, not anything to notice. You must continue onward.
    """


class WarningBossTile(MapTile):
    def intro(self):
        return """
    There is a giant door made out of steel in this chamber.
    It appeared to be just like the tale, the door to Mythical Beast.
    The legendary Black Dragon.
    Once enter, one will never get back
    """


world_dsl = """
|VT|BT|WB|ET|FG|TT|FI|ET|
|  |WB|FG|FI|EN|EN|  |EN|
|EN|FG|EN|FI|  |FG|FI|ET|
|TT|FI|FG|EN|FI|  |ET|  |
|EN|  |ET|FG|ET|FG|EN|FG|
|FI|EN|EN|TT|EN|ET|FI|  |
|FG|  |FG|ET|FI|FG|EN|ET|
|ET|FI|EN|  |EN|ET|FG|ST|
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
                  "ET": EmptyTile,
                  "WB": WarningBossTile,
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
