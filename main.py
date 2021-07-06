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

grenade = Item("Grenade", "attack", "Deals 250 damage", 250)

player_magic = [fire, thunder, blizzard, grass, water, cure, hyperCure]
player_items = [{"item": potion, "quantity": 10}, {"item": superPotion, "quantity": 5},
                {"item": hyperPotion, "quantity": 3}, {"item": elixir, "quantity": 3},
                {"item": superElixir, "quantity": 1}, {"item": grenade, "quantity": 1}]
# Instantiate People
player1 = Person("Bardock:", 3000, 110, 200, 36, player_magic, player_items)
player2 = Person("Brock  :", 2000, 130, 150, 40, player_magic, player_items)
player3 = Person("Zero   :", 4000, 120, 100, 30, player_magic, player_items)
enemy = Person("Magnus:", 4000, 300, 700, 33, [], [])
players = [player1, player2, player3]
running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY CHALLENGES YOU TO A BATTLE!" + bcolors.ENDC)

while running:
    print("========================")
    print("NAME                  HP                                   MP")
    for player in players:
        player.get_stats()

    for player in players:

        player.choose_action()
        choice = input("    Choose action:")
        index = int(choice)-1
        # Regular Attack
        if index == 0:
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print("The opponent was hit for", dmg, "points of damage")

        # Chosen Magic
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic:")) - 1
            if magic_choice == -1:
                continue

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

        # Chosen Items
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1
            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + bcolors.BOLD + "you ran out of", item.name + "!" + bcolors.ENDC)
                continue
            player.items[item_choice]["quantity"] -= 1
            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixir":
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage" + bcolors.ENDC)

    enemy_choice = 1

    enemy_dmg = enemy.generate_damage()
    player1.take_damage(enemy_dmg)
    print("The opponent hits you for", enemy_dmg, "points of damage.")

    print("-----------------------------")
    print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_maxhp()) + bcolors.ENDC)

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
