class Weapon:
    def __init__(self):
        raise NotImplementedError("Do not create raw weapon object")
    
    def __str__(self):
        return self.name
    

class Rock(Weapon):
    def __init__(self):
        self.name = "Rock"
        self.description = "A fist-sized rock, suitable for bludgeoning."
        self.damage = 5
        self.value = 2


class Dagger(Weapon):
    def __init__(self):
        self.name = "Dagger"
        self.description = "A small rusty dagger, somewhat dangerous than a rock."
        self.damage = 10
        self.value = 30


class RustySword(Weapon):
    def __init__(self):
        self.name = "Rusty sword"
        self.description = "This sword is showing it ages, but still has some fight in it."
        self.damage = 18
        self.value = 70


class SilverSword(Weapon):
    def __init__(self):
        self.name = "Silver sword"
        self.description = "Show no rust, the sword shine as if it full of power."
        self.damage = 35
        self.value = 150


class HolySword(Weapon):
    def __init__(self):
        self.name = "Holy sword"
        self.description = "A holy sword, once belong to one of the strongests in the kingdom."
        self.damage = 50
        self.value = 300


###############################


class Consumable:
    def __init__(self):
        raise NotImplementedError("Do not create raw Consumable objects.")
    
    def __str__(self):
        return f"{self.name} (+{self.healing_value} HP)"


class CrustyBread(Consumable):
    def __init__(self):
        self.name = "Crusty Bread"
        self.healing_value = 15
        self.value = 15


class WaterPouch(Consumable):
    def __init__(self):
        self.name = "Water Pouch"
        self.healing_value = 10
        self.value = 10


class HealingPotion(Consumable):
    def __init__(self):
        self.name = "Healing potion"
        self.healing_value = 30
        self.value = 25
