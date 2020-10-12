class Enemy:
    def __init__(self):
        raise NotImplementedError("Do not create raw Enemy objects.")
    
    def __str__(self):
        return self.name
    
    def is_alive(self):
        return self.hp > 0


class Goblin(Enemy):
    def __init__(self):
        self.name = "Green Goblin"
        self.hp = 10
        self.damage = 2
        self.alive_text = """
        A small goblin has noticed you as you step into the cave.
        He ready his weapon and charged at you with a spiky club!
        """
        self.dead_text = """
        A mere goblin is nothing to be feared.
        You continue moving forward pass the decapitated body.
        """


class Orge(Enemy):
    def __init__(self):
        self.name = "Giant Orge"
        self.hp = 30
        self.damage = 8
        self.alive_text = """
        A giant orge is blocking your path!
        You have no choice but to battle the giant monster!
        """
        self.dead_text = """
        The Giant Orge stand no chance againt you!
        It's dead body reminds you of your triumph as you move forward!
        """


class GiantSpider(Enemy):
    def __init__(self):
        self.name = "Goliath Giant Spider"
        self.hp = 50
        self.damage = 10
        self.alive_text = """
        A quiet hissing can be heard as you walked into the room.
        ... suddenly a giant spider jumps onto you from the ceiling!
        """
        self.dead_text = """
        The rotten body just show it is nothing but an insect.
        """

class Werewolf(Enemy):
    def __init__(self):
        self.name = "Werewolf of the dark"
        self.hp = 80
        self.damage = 10
        self.alive_text = """
        A loud howl, enough to break your eardrum, echo throughout the
        room as you step in.
        It seem you have walked into the home of the dark werewolf!
        """
        self.dead_text = """
        Although it was quite agile, it was nothing to be feared!
        You took the fang of the wolf as a trophy.
        """


class RockGolem(Enemy):
    def __init__(self):
        self.name = "Rock Golem the guadian of the tomb"
        self.hp = 120
        self.damage = 10
        self.alive_text = """
        There were giant rocks patched together as if it to resembled a human body.
        As you walk passed it, the rock started to move!
        You've disturbed the rock golem from it chamber!
        """
        self.dead_text = """
        Defeated, the rock golem fall apart, only to become ordinary rocks.
        The core of the golem seem to resembled a rare magic stone...
        """

class Dragon(Enemy):
    def __init__(self):
        self.name = "Dragon of the death"
        self.hp = 200
        self.damage = 20
        self.alive_text = """
        As you walked into the cave chamber, you noticed that this is the largest cave chamber
        among all the cave you have entered.
        Laying in the middle of the room was a black dragon.
        It has noticed your presence.
        The dragon is now on four feet prepared to battle with the 
        """
        self.dead_text = """
        Bathe in blood, on top of the black dragon corpse.
        There stand, the champion of this malevolence battle.
        """
