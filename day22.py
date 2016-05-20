#!python
from pprint import pprint as pp
from adventlib import input_path

class Game(object):

    def __init__(self, player, boss):
        player.game = self
        self.player = player

        self.boss = boss
        self.spells = []

    def effects(self):
        for spell in self.spells:
            spell.update(self.boss)

    def info(self):
        s = '- Player has %s hit points, %s armor, %s mana\n' % (
                self.player.hitpoints, self.player.armor, self.player.mana)
        s += '- Boss has %s hit points' % (self.boss.hitpoints, )
        return s

    def get_winner(self):
        if self.boss.hitpoints <= 0:
            return self.player

        if self.player.hitpoints <= 0:
            return self.boss

    def run(self):
        while True:

            print
            print '-- Player turn --'
            print self.info()

            self.effects()
            winner = self.get_winner()
            if winner:
                return winner

            self.player.attack(self.boss)
            winner = self.get_winner()
            if winner:
                return winner

            print
            print '-- Boss turn --'
            print self.info()

            self.effects()
            winner = self.get_winner()
            if winner:
                return winner

            self.boss.attack(self.player)
            winner = self.get_winner()
            if winner:
                return winner


class Player(object):

    def __init__(self, hitpoints, mana, armor, plan=None):
        self.hitpoints = hitpoints
        self.mana = mana
        self.armor = armor
        self.plan = plan[::-1] if plan is not None else []

    def cast(self, spellclass):
        print 'Player casts %s' % (spellclass, )
        self.game.spells.append(spellclass(self))

    def nextspell(self):
        return self.plan.pop()

    def attack(self, other):
        self.cast(self.nextspell())


class Boss(object):

    def __init__(self, hitpoints, damage):
        self.hitpoints = hitpoints
        self.damage = damage

    def attack(self, other):
        damage = max(1, self.damage) - other.armor
        other.hitpoints -= damage
        print 'Boss attacks for %s damage' % (damage, )


class Spell(object):

    cost = None
    turns = None

    def __init__(self, player):
        self.player = player
        player.mana -= self.cost
        self.turns = self.turns
        if self.turns is None:
            self.effect(self.player.game.boss)

    def effect(self, boss):
        pass

    def update(self, boss):
        if self.turns is not None:
            if self.turns > 0:
                self.effect(boss)
            self.turns -= 1


class MagicMissle(Spell):

    cost = 53

    def effect(self, boss):
        print 'Magic Missle deals 4 damage'
        boss.hitpoints -= 4


class Drain(Spell):

    cost = 73

    def effect(self, boss):
        self.player.hitpoints += 2
        boss.hitpoints -= 2


class Shield(Spell):

    cost = 113
    turns = 6

    def effect(self, boss):
        self.player.armor += 7

    def die(self):
        self.player.armor -= 7


class Poison(Spell):

    cost = 173
    turns = 6

    def effect(self, boss):
        boss.hitpoints -= 3
        print 'Poison deals 3 damage; its timer is now %s.' % (self.turns - 1, )


class Recharge(Spell):

    cost = 229
    turns = 5

    def effect(self, boss):
        print 'Recharge provides 101 mana; its timer is now %s.' % (self.turns - 1, )
        self.player.mana += 101


def get_boss():
    text = open(input_path(__file__, 1)).read()
    stats = {}
    for line in text.splitlines():
        k, v = line.split(':')
        stats[k.replace(' ', '').lower()] = int(v)
    return Boss(**stats)

def init():
    player = Player(50, 500, 0)
    boss = get_boss()
    game = Game(player, boss)
    return game

def tests():
    player = Player(10, 250, 0, [Poison, MagicMissle])
    boss = Boss(13, 8)
    game = Game(player, boss)
    winner = game.run()
    print winner

    # add check for stats

    print '=='
    player = Player(10, 250, 0, [Recharge, Shield, Drain, Poison, MagicMissle])
    boss = Boss(14, 8)
    game = Game(player, boss)
    winner = game.run()
    print winner

def main():
    pass

if __name__ == '__main__':
    tests()
    main()
