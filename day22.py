#!python
from itertools import permutations
from pprint import pprint as pp
from adventlib import input_path

DEBUG = False

class Game(object):

    def __init__(self, player, boss):
        player.game = self
        self.player = player

        self.boss = boss
        self.spells = []

    def effects(self):
        for spell in self.spells:
            spell.update(self.boss)
        self.spells = [ spell for spell in self.spells if spell.turns > 0 ]

    def info(self):
        s = '- Player has %s hit points, %s armor, %s mana\n' % (
                self.player.hitpoints, self.player.armor, self.player.mana)
        s += '- Boss has %s hit points' % (self.boss.hitpoints, )
        return s

    def get_winner(self):
        if self.boss.hitpoints <= 0:
            return self.player

        if ((len(self.spells) == 0 and len(self.player.plan) == 0)
                or self.player.mana == 0 or self.player.hitpoints <= 0):
            return self.boss

    def run(self):
        while True:

            #if DEBUG:
            #    print
            #    print '-- Player turn --'
            #    print self.info()

            self.effects()
            winner = self.get_winner()
            if winner:
                return winner

            self.player.attack(self.boss)
            winner = self.get_winner()
            if winner:
                return winner

            #if DEBUG:
            #    print
            #    print '-- Boss turn --'
            #    print self.info()

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
        self.plan = list(plan[::-1]) if plan is not None else []
        self.casted = []

    def cast(self, spellclass):
        #if DEBUG:
        #    print 'Player casts %s' % (spellclass, )
        spell = spellclass(self)
        self.casted.append(spell)
        self.game.spells.append(spell)

    def nextspell(self):
        return self.plan.pop() if self.plan else None

    def attack(self, other):
        spell = self.nextspell()
        if spell:
            self.cast(spell)


class Boss(object):

    def __init__(self, hitpoints, damage):
        self.hitpoints = hitpoints
        self.damage = damage

    def attack(self, other):
        damage = max(1, self.damage) - other.armor
        other.hitpoints -= damage
        #if DEBUG:
        #    print 'Boss attacks for %s damage' % (damage, )


class Spell(object):

    cost = None
    turns = None

    def __init__(self, player):
        self.player = player
        player.mana -= self.cost
        self.turns = self.turns
        if self.turns is None:
            self.apply(self.player.game.boss)

    def apply(self, boss):
        pass

    def remove(self):
        pass

    def update(self, boss):
        if self.turns is not None:
            if self.turns > 0:
                self.apply(boss)
            self.turns -= 1
            #if DEBUG:
            #    print '%s timer is now %s' % (self, self.turns)
            if self.turns == 0:
                self.remove()


class MagicMissle(Spell):

    cost = 53

    def apply(self, boss):
        #if DEBUG:
        #    print 'Magic Missle deals 4 damage'
        boss.hitpoints -= 4


class Drain(Spell):

    cost = 73

    def apply(self, boss):
        self.player.hitpoints += 2
        boss.hitpoints -= 2


class Shield(Spell):

    cost = 113
    turns = 6

    def __init__(self, *args):
        super(Shield, self).__init__(*args)
        self.player.armor += 7

    def remove(self):
        self.player.armor -= 7


class Poison(Spell):

    cost = 173
    turns = 6

    def apply(self, boss):
        boss.hitpoints -= 3
        #if DEBUG:
        #    print 'Poison deals 3 damage; its timer is now %s.' % (self.turns - 1, )


class Recharge(Spell):

    cost = 229
    turns = 5

    def apply(self, boss):
        #if DEBUG:
        #    print 'Recharge provides 101 mana; its timer is now %s.' % (self.turns - 1, )
        self.player.mana += 101


SPELLS = [MagicMissle, Drain, Shield, Poison, Recharge]

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

def test1():
    if DEBUG:
        print '== Test 1=='
    player = Player(10, 250, 0, [Poison, MagicMissle])
    boss = Boss(13, 8)
    game = Game(player, boss)
    winner = game.run()
    assert (winner == player and game.player.hitpoints == 2 and
            game.player.armor == 0 and game.player.mana == 24)
    if DEBUG:
        print winner

def cost(spells):
    return sum(spell.cost for spell in spells)

def test2():
    # add check for stats
    if DEBUG:
        print '== Test 2 =='
    player = Player(10, 250, 0, [Recharge, Shield, Drain, Poison, MagicMissle])
    boss = Boss(14, 8)
    game = Game(player, boss)
    winner = game.run()
    assert (winner == player and game.player.hitpoints == 1 and
            game.player.armor == 0 and game.player.mana == 114)
    if DEBUG:
        print winner

def test3():
    raise RuntimeError('Make test for casting same spell on the turn the previous ends.')

def get_spellplans(n):
    pspells = SPELLS[:]
    while len(pspells) < n:
        pspells += pspells
    return permutations(pspells, n)

# XXX:
# Need a way to go through picking spells that meet the criteria
#

def part1():
    n = len(SPELLS)
    while True:
        spellplans = list(get_spellplans(n))
        winningplans = []
        print 'n: %s, # plans: %s' % (n, len(spellplans))
        if DEBUG:
            print spellplans
        for spellplan in spellplans:
            if DEBUG:
                print spellplan
            player = Player(50, 500, 0, spellplan)
            boss = get_boss()
            game = Game(player, boss)
            winner = game.run()
            if winner == player:
                winningplans.append(game.player.casted)
        n += 1
        if winningplans:
            break

    bestspellplan = min(winningplans, key=lambda plan: cost(plan))
    print 'Part 1: least amount of mana to win: %s' % (bestspellplan, )

def main():
    test1()
    test2()
    test3()
    part1()

if __name__ == '__main__':
    main()
