import items
import world

class Player:
    def __init__(self):
        self.inventory = [items.Rock(),
                          items.Dagger(),
                          items.CrustyBread()]
        self.x = world.start_tile_location[0]
        self.y = world.start_tile_location[1]
        self.hp = 100
        self.gold = 5
        self.victory = False
    
    def is_alive(self):
        return self.hp > 0
        
    def print_invetory(self):
        print("Inventory:")
        for item in self.inventory:
            print('* ' + str(item))
        print(f"Gold: {self.gold}")

    def most_powerful_weapon(self):
        max_damage = 0
        best_weapon = None
        for item in self.inventory:
            try:
                if item.damage > max_damage:
                    best_weapon = item
                    max_damage = item.damage
            except AttributeError:
                pass
        return best_weapon

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_up(self):
        self.move(0,-1)
    
    def move_down(self):
        self.move(0, 1)
        
    def move_left(self):
        self.move(-1, 0)
        
    def move_right(self):
        self.move(1, 0)
    
    def attack(self):
        best_weapon = self.most_powerful_weapon()
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        print(f"You use {best_weapon} against {enemy.name}. You dealt {best_weapon.damage} damage!")
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print(f"You killed {enemy.name}!")
        else:
            print(f"{enemy.name} has {enemy.hp} HP remaining.")
            
    def heal(self):
        consumables = [item for item in self.inventory
                       if isinstance(item, items.Consumable)]
        if not consumables:
            print("You don't have any healing items!")
            return
        
        for i, item in enumerate(consumables, 1):
            print("Choose an item to use to heal: ")
            print(f"{i}. {item}")

        valid = False
        while not valid:
            choice = input("")
            try:
                to_eat = consumables[int(choice) - 1]
                self.hp = min(100, self.hp + to_eat.healing_value)
                print(f"{to_eat} has been used! + {to_eat.healing_value}HP.")
                self.inventory.remove(to_eat)
                print(f"Current HP: {self.hp}")
                print("==================================")
                valid = True
            except (ValueError, IndexError):
                print("Invalid choice, try again.")
                
    def trade(self):
        room = world.tile_at(self.x, self.y)
        room.check_if_trade(self)