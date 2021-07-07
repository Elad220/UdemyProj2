import random
import sys

from Classes.game import Person,bcolors
from Classes.magic import Spell
from Classes.inventory import Item

# Damaging Moves
fire = Spell("Fire", 20, 400, "damaging")
thunder = Spell("Thunder", 15, 200, "damaging")
blizzard = Spell("Blizzard", 10, 150, "damaging")
grass = Spell("Grass", 5, 100, "damaging")
water = Spell("Water", 15, 250, "damaging")

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
enemy_magic = [fire, blizzard, cure]
player_items = [{"item": potion, "quantity": 10}, {"item": superPotion, "quantity": 5},
                {"item": hyperPotion, "quantity": 3}, {"item": elixir, "quantity": 3},
                {"item": superElixir, "quantity": 1}, {"item": grenade, "quantity": 1}]
# Instantiate People
player1 = Person("Bardock:", 3000, 130, 200, 36, player_magic, player_items)
player2 = Person("Brock  :", 2000, 140, 175, 40, player_magic, player_items)
player3 = Person("Zero   :", 4000, 120, 150, 30, player_magic, player_items)

enemy1 = Person("Troll   ", 2500, 100, 300, 200, enemy_magic, [])
enemy2 = Person("Magnus  ", 4000, 300, 700, 33, enemy_magic, [])
enemy3 = Person("Troll   ", 2500, 100, 300, 200, enemy_magic, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY CHALLENGES YOU TO A BATTLE!" + bcolors.ENDC)

while running:
    print("========================")
    print("NAME                  HP                                   MP")
    for player in players:
        player.get_stats()

    for enemy in enemies:
        enemy.get_enemies_stats()

    for player in players:
        if player.get_hp() > 0:
            player.choose_action()
            choice = input("    Choose action:")
            index = int(choice)-1
        else:
            continue
        # Regular Attack
        if index == 0:
            dmg = player.generate_damage()
            enemy_index = player.choose_target(enemies)
            enemies[enemy_index].take_damage(dmg)
            print("The opponent " + enemies[enemy_index].name.replace(" ", "") + " was hit for", dmg, "points of damage")

            if enemies[enemy_index].get_hp() == 0:
                print(bcolors.OKGREEN + enemies[enemy_index].name.replace(" ", "") + " has been defeated!" + bcolors.ENDC)
                del enemies[enemy_index]
                if len(enemies) == 0:
                    print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                    running = False

        # Chosen Magic
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic:")) - 1
            if magic_choice == -1 or magic_choice > (len(player.magic) - 1):
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
                enemy_index = player.choose_target(enemies)
                enemies[enemy_index].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals " + enemies[enemy_index].name.replace(" ", "") + " " + str(magic_dmg), "points of damage" + bcolors.ENDC)

                if enemies[enemy_index].get_hp() == 0:
                    print(bcolors.OKGREEN + enemies[enemy_index].name.replace(" ", "") + " has been defeated!" + bcolors.ENDC)
                    del enemies[enemy_index]
                    if len(enemies) == 0:
                        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                        running = False
                        sys.exit(2)

        # Chosen Items
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1
            if item_choice <= -1 or item_choice >= len(player.items) - 1:
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
                if item.name == "Super Elixir":
                    for character in players:
                        character.hp = character.maxhp
                        character.mp = character.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy_index = player.choose_target(enemies)
                enemies[enemy_index].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals " + enemies[enemy_index].name + " " + str(item.prop) + " points of damage" + bcolors.ENDC)
        else:
            continue
    # Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    players_alive = len(players) - defeated_players
    enemies_alive = len(enemies) - defeated_enemies
    # Check if player won
    if enemies_alive == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    # Check if player lost
    if players_alive == 0:
        print(bcolors.FAIL + "You lose..." + bcolors.ENDC)
        running = False

    # Enemy attack phase
    print("\n")
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0 and players_alive > 0:
            target = random.randrange(0, players_alive)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "").replace(":", "") + " for", enemy_dmg, "points of HP")
        elif enemy_choice == 1 and players_alive > 0:
            spell, magic_dmg = enemy.choose_enemy_spell()
            if spell != "nothing":
                enemy.reduce_mp(spell.cost)

                if spell.type == "healing":
                    enemy.heal(magic_dmg)
                    print(bcolors.OKBLUE + spell.name + " heals" + enemy.name + " for", str(magic_dmg), "HP." + bcolors.ENDC)

                elif spell.type == "damaging":
                    target_index = random.randrange(0, players_alive)
                    players[target_index].take_damage(magic_dmg)
                    print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals " + players[target_index].name.replace(" ", "").replace(":", "") + " " + str(magic_dmg), "points of damage" + bcolors.ENDC)

                    if players[target_index].get_hp() == 0:
                        print(bcolors.FAIL + players[target_index].name.replace(" ", "") + " was knocked out!" + bcolors.ENDC)
                        del players[target_index]
                        if len(players) == 0:
                            print(bcolors.FAIL + bcolors.BOLD + "You lose..." + bcolors.ENDC)
                            running = False


