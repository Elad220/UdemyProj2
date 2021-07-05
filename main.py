from Classes.game import Person,bcolors
from Classes.magic import Spell
from Classes.inventory import Item


# Damaging Moves
fire = Spell("Fire", 15, 60, "damaging")
thunder = Spell("Thunder", 10, 50, "damaging")
blizzard = Spell("Blizzard", 10, 40, "damaging")
grass = Spell("Grass", 5, 30, "damaging")
water = Spell("Water", 15, 60, "damaging")

# Healing Moves
cure = Spell("Cure", 20, 100, "healing")
hyperCure = Spell("hyperCure", 30, 200, "healing")

# Create some items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
superPotion = Item("Super Potion", "potion", "Heals 100 HP", 100)
hyperPotion = Item("Hyper Potion", "potion", "Heals 200 HP", 200)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
superElixir = Item("Super Elixir", "elixir", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


# Instantiate People
player = Person(400, 100, 30, 36, [fire, thunder, blizzard, grass, water, cure, hyperCure], [])
enemy = Person(300, 100, 40, 45, [], [])

running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY CHALLENGES YOU TO A BATTLE!" + bcolors.ENDC)

while running:
    print("========================")
    player.choose_action()
    choice = input("Choose action:")
    index = int(choice)-1
    # Regular Attack
    if index == 0:
        dmg = player.generate_damage()
        enemy.take_damage(dmg)
        print("The opponent was hit for", dmg, "points of damage")

    # Chosen Magic
    elif index == 1:
        player.choose_magic()
        magic_choice = int(input("Choose magic:")) - 1

        spell = player.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        current_mp = player.get_mp()

        if spell.cost > current_mp:
            print(bcolors.FAIL + "\n Not enough MP\n" + bcolors.ENDC)
            continue
        player.reduce_mp(spell.cost)

        if spell.type == "healing":
            player.heal(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)

        elif spell.type == "damaging":
            enemy.take_damage(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage" + bcolors.ENDC)
    elif index == 2:
        player.choose_item()
    enemy_choice = 1

    enemy_dmg = enemy.generate_damage()
    player.take_damage(enemy_dmg)
    print("The opponent hits you for", enemy_dmg, "points of damage.")

    print("-----------------------------")
    print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_maxhp()) + bcolors.ENDC)

    print("Your HP:" , bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_maxhp()) + bcolors.ENDC)
    print("Your MP:", bcolors.OKBLUE + str(player.get_mp()) + "/" + str(player.get_maxmp()) + bcolors.ENDC)

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "You died..." + bcolors.ENDC)
        running = False
