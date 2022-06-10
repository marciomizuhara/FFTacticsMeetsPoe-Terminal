import random
import time
import threading
import pygame, sys
from cs50 import SQL
from itertools import groupby
from operator import itemgetter
from playsound import playsound
from enemies.characters import *
from enemies.enemy_type import *
from enemies.monsters import *
from enemies.humans import *
from levels_xp import *
from items.amulets import *
from items.armors import *
from items.boots import *
from items.consumables import *
from items.gear_type import *
from items.gloves import *
from items.helmets import *
from items.legs import *
from items.rings import *
from items.second_hands import *
from items.gear_type import *
from items.uniques import *
from items.weapons import *
from music.music import *
from settings import *

GEAR_DROP_RATE = 35
CONSUMABLE_DROP_RATE = 50
DELVE_DROP_RATE = 35
UNIQUE_DROP_RATE = 7

db = SQL("sqlite:///database.db")
inventory = []
consumable_list = []
uniques_list = []


class Item:

    def __init__(self, type, name, level, life, attack, defense, crit_chance, crit_damage, item_quantity):
        self.type = type
        self.name = name
        self.level = level
        self.life = life
        self.attack = attack
        self.defense = defense
        self.crit_chance = crit_chance
        self.crit_damage = crit_damage
        self.item_quantity = item_quantity


class Player:

    def __init__(self, name, total_life, life, attack, defense, level, xp, shaman, crit_chance, crit_damage,
                 item_quantity):
        self.name = name
        self.total_life = total_life
        self.life = life
        self.attack = attack
        self.defense = defense
        self.level = level
        self.xp = xp
        self.shaman = shaman
        self.crit_chance = crit_chance
        self.crit_damage = crit_damage
        self.item_quantity = item_quantity


class PlayerSlot:

    def __init__(self, amulet, armor, gloves, helmet, legs, ring1, ring2, second_hand, weapon, boots):
        self.amulet = amulet
        self.armor = armor
        self.gloves = gloves
        self.helmet = helmet
        self.legs = legs
        self.ring1 = ring1
        self.ring2 = ring2
        self.second_hand = second_hand
        self.weapon = weapon
        self.boots = boots


class ConsumableItem:

    def __init__(self, type, name, value, quantity, rarity, code, sound):
        self.type = type
        self.name = name
        self.value = value
        self.quantity = quantity
        self.rarity = rarity
        self.code = code
        self.sound = sound


class Delve:
    depth = 1
    multiplier = 0.005

    def __init__(self, mobs):
        self.mobs = mobs


class Fossil(ConsumableItem):

    def __init__(self, type, name, value, quantity, rarity, code, sound, attribute):
        super().__init__(type, name, value, quantity, rarity, code, sound)
        self.attribute = attribute


class Enemy:

    def __init__(self, name, life, attack, defense, level, xp, crit_chance):
        self.name = name
        self.life = life
        self.attack = attack
        self.defense = defense
        self.level = level
        self.xp = xp
        self.crit_chance = crit_chance


class Character(Enemy):

    def __init__(self, name, life, attack, defense, level, xp, crit_chance, status, quote1, quote2, quote3):
        super().__init__(name, life, attack, defense, level, xp, crit_chance)
        self.status = status
        self.quote1 = quote1
        self.quote2 = quote2
        self.quote3 = quote3


class Monster(Enemy):

    def __init__(self, name, life, attack, defense, level, xp, crit_chance, delve_drop):
        super().__init__(name, life, attack, defense, level, xp, crit_chance)
        self.delve_drop = delve_drop


class Human(Enemy):
    pass


class Unique(Item):
    pass


def show_inventory():

    item_index = 1
    print('-' * DASH)
    sorted_inventory = sorted(inventory, key=lambda x: (x.level, x.type))

    for i in range(0, len(sorted_inventory)):
        print(f"{item_index} — {sorted_inventory[i].__dict__['name']:<25}|\t"
              f"type: {sorted_inventory[i].__dict__['type']}\t|\t"
              f"level: {sorted_inventory[i].__dict__['level']}"
              f"\t|\tlife: {sorted_inventory[i].__dict__['life']}\t|\tattack: {sorted_inventory[i].__dict__['attack']}\t|\t"
              f"defense: {sorted_inventory[i].__dict__['defense']}\t|\t"
              f"crit chance: {sorted_inventory[i].__dict__['crit_chance']}")
        item_index = item_index + 1
    print('-' * DASH)
    item_index = 1
    choice = input('Press 1 to select item or 2 to return to main menu : ')
    if choice == '1':
        equip_item()
        show_inventory()
    elif choice == '2':
        main_menu()
    else:
        print('Wrong option. You must press 1 or 2')
        time.sleep(1)
        show_inventory()


def show_consumable_items():

    print('-' * DASH)
    print('CODE   ITEM\t\t\t\t\tEFFECT\t\t\t\t\t\t\t\t\t\t\t\tQUANTITY')
    if potion.quantity != 0:
        print(
            f' {potion.code} —  {potion.name:<20}Restores {potion.value} life points\t\t\t\t\t\t\t\t\t{potion.quantity}')
    else:
        pass
    if hi_potion.quantity != 0:
        print(
            f' {hi_potion.code} —  {hi_potion.name:<20}Restores {hi_potion.value} life points\t\t\t\t\t\t\t\t\t{hi_potion.quantity}')
    else:
        pass
    if x_potion.quantity != 0:
        print(
            f' {x_potion.code} —  {x_potion.name:<20}Restores {x_potion.value} life points\t\t\t\t\t\t\t\t\t{x_potion.quantity}')
    else:
        pass
    if elixir.quantity != 0:
        print(f' {elixir.code} —  {elixir.name:<20}Restores full life\t\t\t\t\t\t\t\t\t\t{elixir.quantity}')
    else:
        pass
    if chaos_orb.quantity != 0:
        print(
            f" {chaos_orb.code} —  {chaos_orb.name:<20}Permanently adds +1 to player's attack\t\t\t\t\t{chaos_orb.quantity}")
    else:
        pass
    if divine_orb.quantity != 0:
        print(
            f" {divine_orb.code} —  {divine_orb.name:<20}Permanently adds +1 to player's defense\t\t\t\t\t{divine_orb.quantity}")
    else:
        pass
    if exalted_orb.quantity != 0:
        print(
            f" {exalted_orb.code} —  {exalted_orb.name:<20}Permanently adds +100 to player's total life\t\t\t\t{exalted_orb.quantity}")
    else:
        pass
    if mirror_of_kalandra.quantity != 0:
        print(
            f" {mirror_of_kalandra.code} —  {mirror_of_kalandra.name:<20}Permanently adds +300 to player's total life,\n"
            f"\t\t\t\t\t\t  +10 to player's attack and + 10 to player's defense\t\t{mirror_of_kalandra.quantity}")
    else:
        pass
    if dense_fossil.quantity != 0:
        print(
            f" {dense_fossil.code} —  {dense_fossil.name:<20}Unpredicably reforges the defense value of an item\n"
            f"\t\t\t\t\t\t  or destroys it (33% success rate)\t\t\t\t\t\t\t{dense_fossil.quantity}")
    else:
        pass
    if serrated_fossil.quantity != 0:
        print(
            f" {serrated_fossil.code} —  {serrated_fossil.name:<20}Unpredicably reforges the attack value of an item\n"
            f"\t\t\t\t\t\t  or destroys it (33% success rate)\t\t\t\t\t\t\t{serrated_fossil.quantity}")
    else:
        pass
    if pristine_fossil.quantity != 0:
        print(
            f" {pristine_fossil.code} —  {pristine_fossil.name:<20}Unpredicably reforges the life value of an item\n"
            f"\t\t\t\t\t\t   or destroys it (33% success rate)\t\t\t\t\t\t\t{pristine_fossil.quantity}")
    else:
        pass
    if deft_fossil.quantity != 0:
        print(
            f" {deft_fossil.code} —  {deft_fossil.name:<20}Unpredicably reforges the critical chance value of an item\n"
            f"\t\t\t\t\t\t   or destroys it (33% success rate)\t\t\t\t\t\t\t{deft_fossil.quantity}")
    else:
        pass
    if fractured_fossil.quantity != 0:
        print(
            f" {fractured_fossil.code} —  {fractured_fossil.name:<20}Unpredicably reforges all values of an item\n"
            f"\t\t\t\t\t\t   or destroys it (33% success rate)\t\t\t\t\t\t\t{fractured_fossil.quantity}")
    else:
        pass
    print('-' * DASH)
    item_index = 1
    choice = input('Press 1 to select item or 2 to return: ')
    if choice == '1':
        use_consumable_item()
    elif choice == '2':
        main_menu()
    else:
        print('Wrong option. You must press 1 or 2')
        time.sleep(1)
        show_consumable_items()


def shaman():

    player.life = player.life + player.shaman
    print(f'Shaman healed you {round(player.shaman)} life points!')
    if player.life > player.total_life:
        player.life = player.total_life
    else:
        pass


def player_level_up():

    next_level = str(player.level + 1)
    if player.xp >= 175000:
        player.xp = 175000
    else:
        player.xp = player.xp + enemy.xp

        if player.xp >= levels.get(next_level):
            player.level = player.level + 1
            print(f"Congratulations! You've moved to level {player.level}!")
            playsound(PLAYER_LEVEL_UP, False)
            time.sleep(1)
            total_life_level_up = player.total_life * 0.1
            shaman_level_up = 1.5
            attack_level_up = player.attack * 0.02
            defense_level_up = player.defense * 0.02
            crit_chance_level_up = 0.5
            crit_damage_level_up = 0.1
            print('-' * DASH)
            print("You've gained:\n\n"
                  f"+{round(total_life_level_up, 1)} to total life points\n"
                  f"+{round(shaman_level_up, 1)} to shaman\n"
                  f"+{round(attack_level_up)} to attack\n"
                  f"+{round(defense_level_up)} to defense\n"
                  f"+{round(crit_chance_level_up, 1)} to critical chance\n"
                  f"+{round(crit_damage_level_up, 1)} to critical damage"
                  )
            print('-' * DASH)
            player.total_life = round(player.total_life + total_life_level_up)
            player.life = player.total_life
            player.shaman = player.shaman + shaman_level_up
            player.attack = round(player.attack + attack_level_up)
            player.defense = round(player.defense + defense_level_up)
            player.crit_chance = player.crit_chance + crit_chance_level_up
            player.crit_damage = player.crit_damage + crit_damage_level_up
            time.sleep(1)
            input('Press any key to continue...')
            print('-' * DASH)
        else:
            pass

    print(f'Your xp points: {player.xp}/{levels.get(next_level)}')
    print(f'Your life points: {round(player.life)}/{player.total_life}')
    time.sleep(1)


def check_player_life():

    if player.life <= 0:
        game_over_sound()
        print('You have been slain!')
        time.sleep(3.5)
        print('G A M E   O V E R !')
        input('Press any key...')
        login_menu()


def gear_drop_rate():

    drop_rate_value = random.randint(0, 100)
    if drop_rate_value <= GEAR_DROP_RATE + (GEAR_DROP_RATE * player.item_quantity):
        enemy_gear_drop()
        time.sleep(0.3)
    else:
        pass


def enemy_gear_drop():

    drop = random.choice(gear_type)
    item_type = []
    if drop == 'weapon':
        item_drop = item_level_random_setter(weapon_type)
        item_type.append(item_drop)
    elif drop == 'amulet':
        item_drop = item_level_random_setter(amulet_type)
        item_type.append(item_drop)
    elif drop == 'armor':
        item_drop = item_level_random_setter(armor_type)
        item_type.append(item_drop)
    elif drop == 'boots':
        item_drop = item_level_random_setter(boots_type)
        item_type.append(item_drop)
    elif drop == 'gloves':
        item_drop = item_level_random_setter(gloves_type)
        item_type.append(item_drop)
    elif drop == 'helmet':
        item_drop = item_level_random_setter(helmet_type)
        item_type.append(item_drop)
    elif drop == 'legs':
        item_drop = item_level_random_setter(legs_type)
        item_type.append(item_drop)
    elif drop == 'ring':
        item_drop = item_level_random_setter(ring_type)
        item_type.append(item_drop)
    elif drop == 'second_hand':
        item_drop = item_level_random_setter(second_hand_type)
        item_type.append(item_drop)
    else:
        pass
    new_item = Item(item_type[0]['type'],
                    item_type[0]['name'],
                    item_type[0]['level'],
                    item_type[0]['life'],
                    item_type[0]['attack'],
                    item_type[0]['defense'],
                    item_type[0]['crit_chance'],
                    item_type[0]['crit_damage'],
                    item_type[0]['item_quantity']
                    )
    inventory.append(new_item)
    print('-' * DASH)
    print(f"{inventory[-1].__dict__['name']} level {inventory[-1].__dict__['level']} dropped!")
    inventory_update(player.name, new_item)
    time.sleep(0.3)
    playsound(DROP_1, False)
    time.sleep(0.1)


def consumable_drop_rate():

    consumable_drop_rate_value = random.randint(0, 100)
    if consumable_drop_rate_value <= CONSUMABLE_DROP_RATE + (CONSUMABLE_DROP_RATE * player.item_quantity):
        enemy_consumable_drop()
        print(input('Press any key to continue...'))
    else:
        pass


def enemy_consumable_drop():

    drop = random.randint(0, 100)
    if 0 <= drop < 70:
        if 10 < player.level < 15:
            hi_potion.quantity = hi_potion.quantity + 1
            consumable_list.append(hi_potion)
        elif 15 <= player.level < 20:
            x_potion.quantity = x_potion.quantity + 1
            consumable_list.append(x_potion)
        elif player.level == 20:
            elixir.quantity = elixir.quantity + 1
            consumable_list.append(elixir)
        else:
            potion.quantity = potion.quantity + 1
            consumable_list.append(potion)
    elif 70 <= drop < 79:
        hi_potion.quantity = hi_potion.quantity + 1
        consumable_list.append(hi_potion)
    elif 79 <= drop < 89:
        x_potion.quantity = x_potion.quantity + 1
        consumable_list.append(x_potion)
    elif 89 <= drop < 94:
        elixir.quantity = elixir.quantity + 1
        consumable_list.append(elixir)
    elif 94 <= drop < 96:
        chaos_orb.quantity = chaos_orb.quantity + 1
        consumable_list.append(chaos_orb)
    elif 96 <= drop < 98:
        divine_orb.quantity = divine_orb.quantity + 1
        consumable_list.append(divine_orb)
    elif 98 <= drop <= 99:
        exalted_orb.quantity = exalted_orb.quantity + 1
        consumable_list.append(exalted_orb)
    else:
        random2 = random.randint(0, 100)
        if random2 <= 80:
            exalted_orb.quantity = exalted_orb.quantity + 1
            consumable_list.append(exalted_orb)
        else:
            mirror_of_kalandra.quantity = mirror_of_kalandra.quantity + 1
            consumable_list.append(mirror_of_kalandra)
    print('-' * DASH)
    print(f"{consumable_list[0].__dict__['name']} dropped!")
    print('-' * DASH)
    playsound(consumable_list[0].__dict__['sound'], False)
    time.sleep(0.2)
    consumable_list.clear()


def unique_drop_rate():

    drop_rate_value = random.randint(0, 100)
    if len(list(set(uniques_list))) >= 9:
        pass
    else:
        if drop_rate_value <= UNIQUE_DROP_RATE + (UNIQUE_DROP_RATE * player.item_quantity):
            time.sleep(0.3)
            drop = random.choice(uniques)
            inventory_uniques = [value for elem in inventory for value in elem.__dict__.values()]
            if drop['name'] in inventory_uniques:
                if drop['name'] in uniques_list:
                    pass
                else:
                    uniques_list.append(drop['name'])
                unique_drop_rate()
            elif drop['name'] == player_slot.amulet['name'] or drop['name'] == player_slot.armor['name'] or drop[
                'name'] == \
                    player_slot.boots['name'] or drop['name'] == player_slot.gloves['name'] or drop['name'] == \
                    player_slot.helmet['name'] or drop['name'] == player_slot.legs['name'] or drop['name'] == \
                    player_slot.ring1['name'] or drop['name'] == player_slot.ring2['name'] or drop['name'] == \
                    player_slot.second_hand['name'] or drop['name'] == player_slot.weapon['name']:
                if drop['name'] in uniques_list:
                    pass
                else:
                    uniques_list.append(drop['name'])
                unique_drop_rate()
            else:
                new_item = Unique(drop['type'],
                                  drop['name'],
                                  drop['level'],
                                  drop['life'],
                                  drop['attack'],
                                  drop['defense'],
                                  drop['crit_chance'],
                                  drop['crit_damage'],
                                  drop['item_quantity']
                                  )
                if drop['name'] in uniques_list:
                    pass
                else:
                    uniques_list.append(drop['name'])
                inventory.append(new_item)
                print('-' * DASH)
                print(f"{inventory[-1].__dict__['name']} level {inventory[-1].__dict__['level']} dropped!")
                db.execute("INSERT INTO uniques_list (username, name) VALUES (:username, :name)",
                           username=player.name, name=drop['name'])
                inventory_update(player.name, new_item)
                time.sleep(0.3)
                playsound(DROP_1, False)
                time.sleep(0.1)


def item_level_random_setter(gear_type):

    filtered_dict = (
        [x for x in gear_type if x['level'] > player.level - 2 and x['level'] < player.level + 2 and x['level'] > 1])
    filtered_drop = random.choice(filtered_dict)
    if filtered_drop['level'] > 25:
        filtered_drop['level'] = 25
    elif filtered_drop['level'] <= 1:
        filtered_drop['level'] = 2
    elif filtered_drop['level'] is None:
        filtered_drop['level'] = player.level
    return filtered_drop


def equip_item():

    item_pos = input('Type the number of the item you want to equip: ')
    item_pos = int(item_pos) - 1
    if item_pos + 1 > len(inventory):
        print('Wrong number! Please choose an existing item number.')
        time.sleep(0.5)
        show_inventory()
    item_choice = sorted_inventory = sorted_inventory = sorted(inventory, key=lambda x: (x.level, x.type))[item_pos]
    item_type = str(item_choice.__dict__['type'])
    if item_type == 'ring':
        ring_pos = input("To which RING SLOT do you want to equip it, type '1' or '2' ? ")
        if ring_pos == '1':
            to_inventory = getattr(player_slot, item_type + '1')
            new_item = Item(to_inventory['type'],
                            to_inventory['name'],
                            to_inventory['level'],
                            to_inventory['life'],
                            to_inventory['attack'],
                            to_inventory['defense'],
                            to_inventory['crit_chance'],
                            to_inventory['crit_damage'],
                            to_inventory['item_quantity']
                            )
            inventory.append(new_item)
            unequip_update_status(new_item)
            inventory.remove(item_choice)
            inventory_removal(player.name, item_choice)
            player_slot.ring1 = item_choice.__dict__
            equip_update_status(item_choice)
            print('-' * DASH)
            print(f"{item_choice.__dict__['name']} level {item_choice.__dict__['level']} equipped!")
            time.sleep(1)
        elif ring_pos == '2':
            to_inventory = getattr(player_slot, item_type + '2')
            new_item = Item(to_inventory['type'],
                            to_inventory['name'],
                            to_inventory['level'],
                            to_inventory['life'],
                            to_inventory['attack'],
                            to_inventory['defense'],
                            to_inventory['crit_chance'],
                            to_inventory['crit_damage'],
                            to_inventory['item_quantity']
                            )
            inventory.append(new_item)
            inventory_update(player.name, new_item)
            unequip_update_status(new_item)
            inventory.remove(item_choice)
            inventory_removal(player.name, item_choice)
            player_slot.ring2 = item_choice.__dict__
            equip_update_status(item_choice)
            print('-' * DASH)
            print(f"{item_choice.__dict__['name']} level {item_choice.__dict__['level']} equipped!")
            time.sleep(1)
        else:
            pass
    else:
        item = getattr(player_slot, item_type)

        # Equipping item
        if item is None:
            setattr(player_slot, item_type, item_choice)
            inventory.remove(item_choice)
            inventory_removal(player.name, item_choice)
            item = getattr(player_slot, item_type)
            print('-' * DASH)
            print(f"{item.name} level {item.level} equipped!")
            time.sleep(1)
        else:
            to_inventory = getattr(player_slot, item_type)
            new_item = Item(to_inventory['type'],
                            to_inventory['name'],
                            to_inventory['level'],
                            to_inventory['life'],
                            to_inventory['attack'],
                            to_inventory['defense'],
                            to_inventory['crit_chance'],
                            to_inventory['crit_damage'],
                            to_inventory['item_quantity']
                            )
            inventory.append(new_item)
            inventory_update(player.name, new_item)
            unequip_update_status(new_item)
            setattr(player_slot, item_type, item_choice.__dict__)
            print('-' * DASH)
            print(f"{item_choice.__dict__['name']} level {item_choice.__dict__['level']} equipped!")
            time.sleep(1)
            equip_update_status(item_choice)
            inventory.remove(item_choice)
            inventory_removal(player.name, item_choice)
    save_state()


def use_consumable_item():

    code = input('Type the code of the item you want to use: ')
    if code == '1' and potion.quantity > 0:
        choice = input(f'Press 1 to confirm use {potion.name} or 2 to cancel: ')
        if choice == '1':
            player.life = player.life + potion.value
            potion.quantity = potion.quantity - 1
            if player.life > player.total_life:
                player.life = player.total_life
            print('-' * DASH)
            print(f'You restored {potion.value} life points!')
            time.sleep(1)
        save_state()
        show_consumable_items()
    elif code == '2' and hi_potion.quantity > 0:
        choice = input(f"Are you sure to use {hi_potion.name}? Press 1 to confirm or 2 to cancel: ")
        if choice == '1':
            player.life = player.life + hi_potion.value
            hi_potion.quantity = hi_potion.quantity - 1
            if player.life > player.total_life:
                player.life = player.total_life
            print('-' * DASH)
            print(f'You restored {hi_potion.value} life points!')
            time.sleep(1)
        save_state()
        show_consumable_items()
    elif code == '3' and x_potion.quantity > 0:
        choice = input(f"Are you sure to use {x_potion.name}? Press 1 to confirm or 2 to cancel: ")
        if choice == '1':
            player.life = player.life + x_potion.value
            x_potion.quantity = x_potion.quantity - 1
            if player.life > player.total_life:
                player.life = player.total_life
            print('-' * DASH)
            print(f'You restored {x_potion.value} life points!')
            time.sleep(1)
        save_state()
        show_consumable_items()
    elif code == '4' and elixir.quantity > 0:
        choice = input(f"Are you sure to use {elixir.name}? Press 1 to confirm or 2 to cancel: ")
        if choice == '1':
            player.life = player.total_life
            elixir.quantity = elixir.quantity - 1
            print('-' * DASH)
            print('Your life points were fully restored!')
            time.sleep(1)
        save_state()
        show_consumable_items()
    elif code == '5' and chaos_orb.quantity > 0:
        choice = input(f"Are you sure to use {chaos_orb.name}? Press 1 to confirm or 2 to cancel: ")
        if choice == '1':
            player.attack = player.attack + 1
            chaos_orb.quantity = chaos_orb.quantity - 1
            print('-' * DASH)
            print('Your permanently added +1 to your attack')
            time.sleep(1)
        save_state()
        show_consumable_items()
    elif code == '6' and divine_orb.quantity > 0:
        choice = input(f"Are you sure to use {divine_orb.name}? Press 1 to confirm or 2 to cancel: ")
        if choice == '1':
            player.defense = player.defense + 1
            divine_orb.quantity = divine_orb.quantity - 1
            print('-' * DASH)
            print('Your permanently added +1 to your defense')
            time.sleep(1)
        save_state()
        show_consumable_items()
    elif code == '7' and exalted_orb.quantity > 0:
        choice = input(f"Are you sure to use {exalted_orb.name}? Press 1 to confirm or 2 to cancel: ")
        if choice == '1':
            player.total_life = player.total_life + exalted_orb.value
            exalted_orb.quantity = exalted_orb.quantity - 1
            print('-' * DASH)
            print(f'Your permanently added +{exalted_orb.value} to your total life points')
            time.sleep(1)
        save_state()
        show_consumable_items()
    elif code == '8' and mirror_of_kalandra.quantity > 0:
        choice = input(f"Are you sure to use {mirror_of_kalandra.name}? Press 1 to confirm or 2 to cancel: ")
        if choice == '1':
            player.total_life = player.total_life + mirror_of_kalandra.value['life']
            player.attack = player.attack + mirror_of_kalandra.value['attack']
            player.defense = player.defense + mirror_of_kalandra.value['defense']
            mirror_of_kalandra.quantity = mirror_of_kalandra.quantity - 1
            print('-' * DASH)
            print('Your permanently added +300 to your total life points, +10 to your attack and +10 to your defense!')
            time.sleep(1)
        save_state()
        show_consumable_items()
    elif code == '9' and dense_fossil.quantity > 0:
        use_fossil(dense_fossil)
    elif code == '10' and serrated_fossil.quantity > 0:
        use_fossil(serrated_fossil)
    elif code == '11' and pristine_fossil.quantity > 0:
        use_fossil(pristine_fossil)
    elif code == '12' and deft_fossil.quantity > 0:
        use_fossil(deft_fossil)
    elif code == '13' and fractured_fossil.quantity > 0:
        use_fossil(fractured_fossil)
    show_consumable_items()


def use_fossil(fossil):

    item_index = 1
    sorted_inventory = sorted(inventory, key=lambda x: (x.level, x.type))
    print('-' * DASH)
    for i in range(0, len(sorted_inventory)):
        print(f"{item_index} — {sorted_inventory[i].__dict__['name']:<25}|\t"
              f"type: {sorted_inventory[i].__dict__['type']}\t|\t"
              f"level: {sorted_inventory[i].__dict__['level']}"
              f"\t|\tlife: {sorted_inventory[i].__dict__['life']}\t|\tattack: {sorted_inventory[i].__dict__['attack']}\t|\t"
              f"defense: {sorted_inventory[i].__dict__['defense']}\t|\t"
              f"crit chance: {sorted_inventory[i].__dict__['crit_chance']}")
        item_index = item_index + 1
    print('-' * DASH)
    item_pos = input(f'Type the number of the item you want to use {fossil.name} on: ')
    item_pos = int(item_pos) - 1
    if item_pos + 1 > len(inventory):
        print('Wrong number! Please choose an existing item number.')
        time.sleep(0.5)
        use_fossil(fossil)
    item_choice = sorted_inventory = sorted(inventory, key=lambda x: (x.level, x.type))[item_pos]
    item_index = 1
    confirm = input(
        f"Are you sure you want to try to reforge {item_choice.__dict__['name']} level {item_choice.__dict__['level']} with {fossil.name}?\n"
        f"Press 1 to confirm or 2 to cancel: ")
    if confirm == '1':
        old_name = item_choice.__dict__['name']
        old_type = item_choice.__dict__['type']
        old_level = item_choice.__dict__['level']
        old_attr = item_choice.__dict__[fossil.attribute]
        new = fossil_reforge(fossil, item_choice)
        if new:
            print('-' * DASH)
            print(
                f"Your {item_choice.__dict__['name']} level {item_choice.__dict__['level']} was reforged!")
            print('-' * DASH)

            row = db.execute("SELECT * FROM inventory WHERE username = :username AND name = :name AND level = :level",
                             username=player.name, name=old_name, level=old_level)
            id = (row[0]['id'])
            db.execute("DELETE FROM inventory WHERE id = :id",
                       id=id)
            db.execute("INSERT INTO inventory (username, name, type, level, life, attack, defense, crit_chance, crit_damage, item_quantity)"
                       "VALUES (:username, :name, :type, :level, :life, :attack, :defense, :crit_chance, :crit_damage, :item_quantity)",
                       username=player.name,
                       name=item_choice.__dict__['name'],
                       type=item_choice.__dict__['type'],
                       level=item_choice.__dict__['level'],
                       life=item_choice.__dict__['life'],
                       attack=item_choice.__dict__['attack'],
                       defense=item_choice.__dict__['defense'],
                       crit_chance=item_choice.__dict__['crit_chance'],
                       crit_damage=item_choice.__dict__['crit_damage'],
                       item_quantity=item_choice.__dict__['item_quantity'])

            time.sleep(1)
            print(f"previous item {fossil.attribute} value:\t{old_attr}\n"
                  f"new item {fossil.attribute} value:\t\t\t{new.__dict__[fossil.attribute]}")
            print('-' * DASH)
            time.sleep(1)
            input('Press any key to continue..')
            show_consumable_items()
    elif confirm == '2':
        show_consumable_items()
    else:
        print('Wrong option..')
        time.sleep(0.5)
        use_fossil(fossil)


def fossil_reforge(fossil, item_to_reforge):

    choice = random.randint(0, 100)
    fossil.quantity = fossil.quantity - 1
    if choice <= 90:
        if fossil.name == 'Dense Fossil':
            number = random.randint(1, dense_fossil.value)
            item_to_reforge.__dict__['defense'] = item_to_reforge.__dict__['defense'] + number
            item_to_reforge.__dict__['level'] = item_to_reforge.__dict__['level'] + 1
            return item_to_reforge
        elif fossil.name == 'Serrated Fossil':
            number = random.randint(1, serrated_fossil.value)
            item_to_reforge.__dict__['attack'] = item_to_reforge.__dict__['attack'] + number
            item_to_reforge.__dict__['level'] = item_to_reforge.__dict__['level'] + 1
            return item_to_reforge
        elif fossil.name == 'Pristine Fossil':
            number = random.randint(1, pristine_fossil.value)
            item_to_reforge.__dict__['life'] = item_to_reforge.__dict__['life'] + number
            item_to_reforge.__dict__['level'] = item_to_reforge.__dict__['level'] + 1
            return item_to_reforge
        elif fossil.name == 'Deft Fossil':
            number = random.randint(1, deft_fossil.value)
            item_to_reforge.__dict__['crit_chance'] = item_to_reforge.__dict__['crit_chance'] + number
            item_to_reforge.__dict__['level'] = item_to_reforge.__dict__['level'] + 1
            return item_to_reforge
        elif fossil.name == 'Fractured Fossil':
            number = random.randint(1, fractured_fossil.value)
            item_to_reforge.__dict__['crit_chance'] = item_to_reforge.__dict__['crit_chance'] + number
            item_to_reforge.__dict__['level'] = item_to_reforge.__dict__['level'] + 1
            return item_to_reforge
        else:
            print('wrong fossil type')
            input('aqui 10')
    else:
        print(f"{item_to_reforge.__dict__['name']} {item_to_reforge.__dict__['level']} was destroyed!")

        row = db.execute("SELECT * FROM inventory WHERE username = :username AND name = :name AND level = :level",
                         username=player.name,
                         name=item_to_reforge.__dict__['name'],
                         level=item_to_reforge.__dict__['level'])
        id = (row[0]['id'])
        db.execute("DELETE FROM inventory WHERE id = :id",
                   id=id)

        save_state()
        time.sleep(1)
        input('Press any key yo return...')
        show_consumable_items()


def equip_update_status(item):

    player.total_life = player.total_life + int(item.life)
    player.attack = player.attack + int(item.attack)
    player.defense = player.defense + int(item.defense)
    player.crit_chance = player.crit_chance + int(item.crit_chance)
    player.crit_damage = player.crit_damage + int(item.crit_damage)
    player.item_quantity = player.item_quantity + item.item_quantity


def unequip_update_status(item):

    player.total_life = player.total_life - int(item.life)
    player.attack = player.attack - int(item.attack)
    player.defense = player.defense - int(item.defense)
    player.crit_chance = player.crit_chance - int(item.crit_chance)
    player.crit_damage = player.crit_damage - int(item.crit_damage)
    player.item_quantity = player.item_quantity - item.item_quantity


def crit_chance(character_crit_chance, character_attack, character_critdamage):

    crit_chance_random = random.randint(1, 100)
    if crit_chance_random <= character_crit_chance:
        random2 = random.randint(10, 30)
        crit_damage = int((character_attack + random2) * character_critdamage)
        return crit_damage
    else:
        return character_attack


def battle():

    while enemy.life > 0:
        if enemy.attack <= player.defense:
            player_damage = 0
            a = crit_chance(player.crit_chance, player.attack, player.crit_damage)
            if a > player.attack:
                enemy_damage = a - enemy.defense
                enemy.life = enemy.life - enemy_damage
                player.life = player.life - player_damage
                print(f"- CRITICAL HIT! You've attacked {enemy.name} and dealt {enemy_damage} damage!")
                critical_attack_sound()
                time.sleep(0.5)
                print(f"- {enemy.name} attacked you and dealt {player_damage} damage!")
                enemy_attack_sound()
                time.sleep(0.5)
            else:
                enemy_damage = player.attack - enemy.defense
                enemy.life = enemy.life - enemy_damage
                player.life = player.life - player_damage
                print(f"- You've attacked {enemy.name} and dealt {enemy_damage} damage!")
                player_attack_sound()
                print(f"- {enemy.name} attacked you and dealt {player_damage} damage!")
                enemy_attack_sound()
                time.sleep(0.5)
        else:
            a = crit_chance(player.crit_chance, player.attack, player.crit_damage)
            b = crit_chance(enemy.crit_chance, enemy.attack, 1.4)

            if a > player.attack and b == enemy.attack:
                enemy_damage = a - enemy.defense
                player_damage = enemy.attack - player.defense
                enemy.life = enemy.life - enemy_damage
                player.life = player.life - player_damage
                print(f"- CRITICAL HIT! You've attacked {enemy.name} and dealt {enemy_damage} damage!")
                critical_attack_sound()
                print(f"- {enemy.name} attacked you and dealt {player_damage} damage!")
                enemy_attack_sound()
                time.sleep(0.5)
            elif a > player.attack and b > enemy.attack:
                enemy_damage = a - enemy.defense
                player_damage = b - player.defense
                enemy.life = enemy.life - enemy_damage
                player.life = player.life - player_damage
                print(f"- CRITICAL HIT! You've attacked {enemy.name} and dealt {enemy_damage} damage!")
                critical_attack_sound()
                print(f"- CRITICAL HIT! {enemy.name} attacked you and dealt {player_damage} damage!")
                critical_attack_sound()
            elif a == player.attack and b > enemy.attack:
                enemy_damage = player.attack - enemy.defense
                player_damage = b - player.defense
                enemy.life = enemy.life - enemy_damage
                player.life = player.life - player_damage
                print(f"- You've attacked {enemy.name} and dealt {enemy_damage} damage!")
                player_attack_sound()
                print(f"- CRITICAL HIT! {enemy.name} attacked you and dealt {player_damage} damage!")
                critical_attack_sound()
                time.sleep(0.5)
            else:
                enemy_damage = player.attack - enemy.defense
                player_damage = enemy.attack - player.defense
                enemy.life = enemy.life - enemy_damage
                player.life = player.life - player_damage
                print(f"- You've attacked {enemy.name} and dealt {enemy_damage} damage!")
                player_attack_sound()
                print(f"- {enemy.name} attacked you and dealt {player_damage} damage!")
                enemy_attack_sound()
                time.sleep(0.5)
    if enemy.life < 0:
        enemy.life = 0


def battle_finish():

    print('-' * DASH)
    check_player_life()
    print(f'You have defeated {enemy.name} and gained {enemy.xp} xp points!')
    if enemy.name == 'Wiegraf':
        wiegraf1.status = False
    elif enemy.name == 'Dycedarg':
        dycedarg1.status = False
    elif enemy.name == 'Wiegraf, Corpse Brigade Head':
        wiegraf2.status = False
    elif enemy.name == 'Dycedarg, the Betrayer God':
        dycedarg2.status = False
    else:
        pass
    input('Press any key to continue...')
    print('-' * DASH)
    shaman()
    time.sleep(1)
    print('-' * DASH)
    player_level_up()
    gear_drop_rate()
    unique_drop_rate()
    consumable_drop_rate()
    save_state()
    encounter()


def boss_batle(boss_instance):

    boss_music()
    print('-' * DASH)
    print('A  P O W E R F U L  E N E M Y  I S  A P P R O A C H I N G . . . ')
    time.sleep(2)
    print('-' * DASH)
    input(f'{boss_instance.name}: {boss_instance.quote1}')
    while boss_instance.life > 0:
        if boss_instance.attack <= player.defense:
            player_damage = 0
            a = crit_chance(player.crit_chance, player.attack, player.crit_damage)
            if a > player.attack:
                enemy_damage = a - boss_instance.defense
                boss_instance.life = boss_instance.life - enemy_damage
                player.life = player.life - player_damage
                print(f"- CRITICAL HIT! You've attacked {boss_instance.name} and dealt {enemy_damage} damage!")
                critical_attack_sound()
                time.sleep(0.5)
                print(f"- {boss_instance.name} attacked you and dealt {player_damage} damage!")
                enemy_attack_sound()
                time.sleep(0.5)
            else:
                enemy_damage = player.attack - boss_instance.defense
                boss_instance.life = boss_instance.life - enemy_damage
                player.life = player.life - player_damage
                print(f"- You've attacked {boss_instance.name} and dealt {enemy_damage} damage!")
                player_attack_sound()
                print(f"- {boss_instance.name} attacked you and dealt {player_damage} damage!")
                enemy_attack_sound()
                time.sleep(0.5)
        else:
            a = crit_chance(player.crit_chance, player.attack, player.crit_damage)
            b = crit_chance(boss_instance.crit_chance, boss_instance.attack, 1.4)
            if a > player.attack and b == boss_instance.attack:
                enemy_damage = a - boss_instance.defense
                player_damage = boss_instance.attack - player.defense
                boss_instance.life = boss_instance.life - enemy_damage
                player.life = player.life - player_damage
                print(f"- CRITICAL HIT! You've attacked {boss_instance.name} and dealt {enemy_damage} damage!")
                critical_attack_sound()
                print(f"- {boss_instance.name} attacked you and dealt {player_damage} damage!")
                enemy_attack_sound()
                time.sleep(0.5)
            elif a > player.attack and b > boss_instance.attack:
                enemy_damage = a - boss_instance.defense
                player_damage = b - player.defense
                boss_instance.life = boss_instance.life - enemy_damage
                player.life = player.life - player_damage
                print(f"- CRITICAL HIT! You've attacked {boss_instance.name} and dealt {enemy_damage} damage!")
                critical_attack_sound()
                print(f"- CRITICAL HIT! {boss_instance.name} attacked you and dealt {player_damage} damage!")
                critical_attack_sound()
            elif a == player.attack and b > boss_instance.attack:
                enemy_damage = player.attack - boss_instance.defense
                player_damage = b - player.defense
                boss_instance.life = boss_instance.life - enemy_damage
                player.life = player.life - player_damage
                print(f"- You've attacked {boss_instance.name} and dealt {enemy_damage} damage!")
                player_attack_sound()
                print(f"- CRITICAL HIT! {boss_instance.name} attacked you and dealt {player_damage} damage!")
                critical_attack_sound()
                time.sleep(0.5)
            else:
                enemy_damage = player.attack - boss_instance.defense
                player_damage = boss_instance.attack - player.defense
                boss_instance.life = boss_instance.life - enemy_damage
                player.life = player.life - player_damage
                print(f"- You've attacked {boss_instance.name} and dealt {enemy_damage} damage!")
                player_attack_sound()
                print(f"- {boss_instance.name} attacked you and dealt {player_damage} damage!")
                enemy_attack_sound()
                time.sleep(0.5)
    if boss_instance.life < 0:
        boss_instance.life = 0
    print('-' * DASH)
    check_player_life()
    input(f'{boss_instance.name}: {boss_instance.quote2}\n')
    if boss_instance.name == dycedarg2.name:
        print(
            f"Congratulations! You've defeated {dycedarg2.name} and reached the endgame of Final Fantasy Tactics—The Idle Game.\n"
            f"Please check the Help menu for more information")
        print('-' * DASH)
    else:
        print(f'You have defeated {boss_instance.name} and gained {boss_instance.xp} xp points!')
    boss_instance.status = False
    username = player.name
    if boss_instance.name == 'Wiegraf':
        db.execute("UPDATE boss_instance SET wiegraf1 = :wiegraf1 WHERE username = :username", wiegraf1=0,
                   username=username)
    elif boss_instance.name == 'Dycedarg':
        db.execute("UPDATE boss_instance SET dycedarg1 = :dycedarg1 WHERE username = :username", dycedarg1=0,
                   username=username)
    elif boss_instance.name == 'Wiegraf, Corpse Brigade Head':
        db.execute("UPDATE boss_instance SET wiegraf2 = :wiegraf2 WHERE username = :username", wiegraf2=0,
                   username=username)
    elif boss_instance.name == 'Dycedarg, the Betrayer God':
        db.execute("UPDATE boss_instance SET dycedarg2 = :dycedarg2 WHERE username = :username", dycedarg2=0,
                   username=username)
    else:
        pass
    pygame.mixer.music.fadeout(3)
    pygame.mixer.music.stop()
    background_music()
    input('Press any key to continue...')
    print('-' * DASH)
    shaman()
    time.sleep(1)
    player_level_up()
    gear_drop_rate()
    unique_drop_rate()
    consumable_drop_rate()
    save_state()
    encounter()


def encounter():

    enemy_choice = random.choice(enemy_type)
    if enemy_choice == 'monster':
        enemy_type_choice = random.choice(list(monster_type))
        enemy_dict = monster_type[enemy_type_choice]
        global enemy
        enemy = Monster(enemy_dict['name'],
                        enemy_dict['life'],
                        enemy_dict['attack'],
                        enemy_dict['defense'],
                        enemy_dict['level'],
                        enemy_dict['xp'],
                        enemy_dict['crit_chance'],
                        enemy_dict['delve_drop']
                        )
    elif enemy_choice == 'human':
        enemy_type_choice = random.choice(list(human_type))
        enemy_dict = human_type[enemy_type_choice]
        enemy = Human(enemy_dict['name'],
                      enemy_dict['life'],
                      enemy_dict['attack'],
                      enemy_dict['defense'],
                      enemy_dict['level'],
                      enemy_dict['xp'],
                      enemy_dict['crit_chance'],
                      )

    # level setter
    if enemy.level > player.level + 2:
        encounter()
    elif enemy.level < player.level - 1:
        encounter()
    else:
        if player.level == 5 and wiegraf1.status is True:
            boss_batle(wiegraf1)
        elif player.level == 10 and dycedarg1.status is True:
            boss_batle(dycedarg1)
        elif player.level == 15 and wiegraf2.status is True:
            boss_batle(wiegraf2)
        elif player.level == 20 and dycedarg2.status is True:
            boss_batle(dycedarg2)
        else:
            pass
        print('-' * DASH)
        print(f"You've encountered a level {enemy.level} {enemy.name}!")
        choice = (input('Press 1 to attack or 2 to enter menu:\n'))
        print('-' * DASH)
        if choice == '1':
            time.sleep(0.5)
            battle()
            battle_finish()
        elif choice == '2':
            main_menu()
        else:
            print('-' * DASH)
            print("Wrong option!")
            print('-' * DASH)
            time.sleep(0.5)
            encounter()
        battle()
        battle_finish()


def player_status():

    next_level = str(player.level + 1)
    if int(next_level) > 20:
        next_level = str(20)
    print('-' * DASH)
    print(f"Name: {player.name}\t\t\t\t| Weapon: {player_slot.weapon['name']:<35} level {player_slot.weapon['level']}\n"
          f"Level: {player.level}\t\t\t\t\t| Helmet: {player_slot.helmet['name']:<35} level {player_slot.helmet['level']}\n"
          f"Experience: {player.xp}/{levels.get(next_level)}\t\t\t| Second-hand: {player_slot.second_hand['name']:<35} level {player_slot.second_hand['level']}\n"
          f"HP: {player.life}/{player.total_life}\t\t\t\t\t| Armor: {player_slot.armor['name']:<35} level {player_slot.armor['level']}\n"
          f"Attack: {player.attack}\t\t\t\t\t| Gloves: {player_slot.gloves['name']:<35} level {player_slot.gloves['level']}\n"
          f"Defense: {player.defense}\t\t\t\t| Legs: {player_slot.legs['name']:<35} level {player_slot.legs['level']}\n"
          f"Critical Chance: {player.crit_chance}%\t\t| Ring 1: {player_slot.ring1['name']:<35} level {player_slot.ring1['level']}\n"
          f"Critical Damage: {round(player.crit_damage, 1)}%\t\t| Ring 2: {player_slot.ring2['name']:<35} level {player_slot.ring2['level']}\n"
          f"Item Quantity: {round((player.item_quantity * 100), 1)}%\t\t\t| Amulet: {player_slot.amulet['name']:<35} level {player_slot.amulet['level']}\n"
          f"Delve Depth: {Delve.depth}\t\t\t\t| Boots: {player_slot.boots['name']:<35} level {player_slot.boots['level']}"
          )
    print('-' * DASH)
    input('Press any key to continue...')
    main_menu()


def inventory_update(username, item):

    if len(inventory) == 0:
        pass
    else:

        db.execute(
            "INSERT INTO inventory (username, name, type, level, life, attack, defense, crit_chance,"
            "crit_damage, item_quantity) VALUES (:username, :name, :type, :level, :life, :attack, :defense,"
            ":crit_chance, :crit_damage, :item_quantity)",
            username=username, name=item.name, type=item.type,
            level=item.level, life=item.life,
            attack=item.attack, defense=item.defense,
            crit_chance=item.crit_chance, crit_damage=item.crit_damage, item_quantity=item.item_quantity)


def inventory_removal(username, item):

    if len(inventory) == 0:
        pass
    else:

        db.execute(
            "DELETE FROM inventory WHERE username= :username and name = :name",
            username=username, name=item.name)


def save_state():

    username = player.name
    # Player status
    db.execute(
        "UPDATE user_data SET level = :level, experience = :experience, total_life = :total_life, life = :life, attack = :attack, defense = :defense, shaman = :shaman, crit_chance = :crit_chance, crit_damage = :crit_damage, item_quantity = :item_quantity  WHERE username = :username",
        level=player.level, experience=player.xp, total_life=player.total_life, life=player.life,
        attack=player.attack, defense=player.defense, shaman=player.shaman,
        crit_chance=player.crit_chance, crit_damage=player.crit_damage, item_quantity=player.item_quantity,
        username=username)

    # Player_Slot
    db.execute("DELETE FROM amulet WHERE username = :username",
               username=username)
    db.execute(
        "INSERT INTO amulet (username, name, type, level, life, attack, defense, crit_chance, crit_damage, item_quantity) VALUES (:username, :name, :type, :level, :life, :attack, :defense, :crit_chance, :crit_damage, :item_quantity)",
        username=player.name, name=player_slot.amulet['name'], type=player_slot.amulet['type'],
        level=player_slot.amulet['level'], life=player_slot.amulet['life'],
        attack=player_slot.amulet['attack'], defense=player_slot.amulet['defense'],
        crit_chance=player_slot.amulet['crit_chance'], crit_damage=player_slot.amulet['crit_damage'],
        item_quantity=player_slot.amulet['item_quantity'])
    db.execute("DELETE FROM armor WHERE username = :username",
               username=username)
    db.execute(
        "INSERT INTO armor (username, name, type, level, life, attack, defense, crit_chance, crit_damage, item_quantity) VALUES (:username, :name, :type, :level, :life, :attack, :defense, :crit_chance, :crit_damage, :item_quantity)",
        username=player.name, name=player_slot.armor['name'], type=player_slot.armor['type'],
        level=player_slot.armor['level'], life=player_slot.armor['life'],
        attack=player_slot.armor['attack'], defense=player_slot.armor['defense'],
        crit_chance=player_slot.armor['crit_chance'], crit_damage=player_slot.armor['crit_damage'],
        item_quantity=player_slot.armor['item_quantity'])
    db.execute("DELETE FROM gloves WHERE username = :username",
               username=username)
    db.execute(
        "INSERT INTO gloves (username, name, type, level, life, attack, defense, crit_chance, crit_damage, item_quantity) VALUES (:username, :name, :type, :level, :life, :attack, :defense, :crit_chance, :crit_damage, :item_quantity)",
        username=player.name, name=player_slot.gloves['name'], type=player_slot.gloves['type'],
        level=player_slot.gloves['level'], life=player_slot.gloves['life'],
        attack=player_slot.gloves['attack'], defense=player_slot.gloves['defense'],
        crit_chance=player_slot.gloves['crit_chance'], crit_damage=player_slot.gloves['crit_damage'],
        item_quantity=player_slot.gloves['item_quantity'])
    db.execute("DELETE FROM helmet WHERE username = :username",
               username=username)
    db.execute(
        "INSERT INTO helmet (username, name, type, level, life, attack, defense, crit_chance, crit_damage, item_quantity) VALUES (:username, :name, :type, :level, :life, :attack, :defense, :crit_chance, :crit_damage, :item_quantity)",
        username=player.name, name=player_slot.helmet['name'], type=player_slot.helmet['type'],
        level=player_slot.helmet['level'], life=player_slot.helmet['life'],
        attack=player_slot.helmet['attack'], defense=player_slot.helmet['defense'],
        crit_chance=player_slot.helmet['crit_chance'], crit_damage=player_slot.helmet['crit_damage'],
        item_quantity=player_slot.helmet['item_quantity'])
    db.execute("DELETE FROM legs WHERE username = :username",
               username=username)
    db.execute(
        "INSERT INTO legs (username, name, type, level, life, attack, defense, crit_chance, crit_damage, item_quantity) VALUES (:username, :name, :type, :level, :life, :attack, :defense, :crit_chance, :crit_damage, :item_quantity)",
        username=player.name, name=player_slot.legs['name'], type=player_slot.legs['type'],
        level=player_slot.legs['level'], life=player_slot.legs['life'],
        attack=player_slot.legs['attack'], defense=player_slot.legs['defense'],
        crit_chance=player_slot.legs['crit_chance'], crit_damage=player_slot.legs['crit_damage'],
        item_quantity=player_slot.legs['item_quantity'])
    db.execute("DELETE FROM ring1 WHERE username = :username",
               username=username)
    db.execute(
        "INSERT INTO ring1 (username, name, type, level, life, attack, defense, crit_chance, crit_damage, item_quantity) VALUES (:username, :name, :type, :level, :life, :attack, :defense, :crit_chance, :crit_damage, :item_quantity)",
        username=player.name, name=player_slot.ring1['name'], type=player_slot.ring1['type'],
        level=player_slot.ring1['level'], life=player_slot.ring1['life'],
        attack=player_slot.ring1['attack'], defense=player_slot.ring1['defense'],
        crit_chance=player_slot.ring1['crit_chance'], crit_damage=player_slot.ring1['crit_damage'],
        item_quantity=player_slot.ring1['item_quantity'])
    db.execute("DELETE FROM ring2 WHERE username = :username",
               username=username)
    db.execute(
        "INSERT INTO ring2 (username, name, type, level, life, attack, defense, crit_chance, crit_damage, item_quantity) VALUES (:username, :name, :type, :level, :life, :attack, :defense, :crit_chance, :crit_damage, :item_quantity)",
        username=player.name, name=player_slot.ring2['name'], type=player_slot.ring2['type'],
        level=player_slot.ring2['level'], life=player_slot.ring2['life'],
        attack=player_slot.ring2['attack'], defense=player_slot.ring2['defense'],
        crit_chance=player_slot.ring2['crit_chance'], crit_damage=player_slot.ring2['crit_damage'],
        item_quantity=player_slot.ring2['item_quantity'])
    db.execute("DELETE FROM second_hand WHERE username = :username",
               username=username)
    db.execute(
        "INSERT INTO second_hand (username, name, type, level, life, attack, defense, crit_chance, crit_damage, item_quantity) VALUES (:username, :name, :type, :level, :life, :attack, :defense, :crit_chance, :crit_damage, :item_quantity)",
        username=player.name, name=player_slot.second_hand['name'], type=player_slot.second_hand['type'],
        level=player_slot.second_hand['level'], life=player_slot.second_hand['life'],
        attack=player_slot.second_hand['attack'], defense=player_slot.second_hand['defense'],
        crit_chance=player_slot.second_hand['crit_chance'], crit_damage=player_slot.second_hand['crit_damage'],
        item_quantity=player_slot.second_hand['item_quantity'])
    db.execute("DELETE FROM weapon WHERE username = :username",
               username=username)
    db.execute(
        "INSERT INTO weapon (username, name, type, level, life, attack, defense, crit_chance, crit_damage, item_quantity) VALUES (:username, :name, :type, :level, :life, :attack, :defense, :crit_chance, :crit_damage, :item_quantity)",
        username=player.name, name=player_slot.weapon['name'], type=player_slot.weapon['type'],
        level=player_slot.weapon['level'], life=player_slot.weapon['life'],
        attack=player_slot.weapon['attack'], defense=player_slot.weapon['defense'],
        crit_chance=player_slot.weapon['crit_chance'], crit_damage=player_slot.weapon['crit_damage'],
        item_quantity=player_slot.weapon['item_quantity'])
    db.execute("DELETE FROM boots WHERE username = :username",
               username=username)
    db.execute(
        "INSERT INTO boots (username, name, type, level, life, attack, defense, crit_chance, crit_damage, item_quantity) VALUES (:username, :name, :type, :level, :life, :attack, :defense, :crit_chance, :crit_damage, :item_quantity)",
        username=player.name, name=player_slot.boots['name'], type=player_slot.boots['type'],
        level=player_slot.boots['level'], life=player_slot.boots['life'],
        attack=player_slot.boots['attack'], defense=player_slot.boots['defense'],
        crit_chance=player_slot.boots['crit_chance'], crit_damage=player_slot.boots['crit_damage'],
        item_quantity=player_slot.boots['item_quantity'])

    # Consumables
    db.execute("UPDATE potion SET quantity = :quantity WHERE username = :username", quantity=potion.quantity,
               username=username)
    db.execute("UPDATE x_potion SET quantity = :quantity WHERE username = :username", quantity=x_potion.quantity,
               username=username)
    db.execute("UPDATE elixir SET quantity = :quantity WHERE username = :username", quantity=elixir.quantity,
               username=username)
    db.execute("UPDATE chaos_orb SET quantity = :quantity WHERE username = :username", quantity=chaos_orb.quantity,
               username=username)
    db.execute("UPDATE divine_orb SET quantity = :quantity WHERE username = :username", quantity=divine_orb.quantity,
               username=username)
    db.execute("UPDATE exalted_orb SET quantity = :quantity WHERE username = :username", quantity=exalted_orb.quantity,
               username=username)
    db.execute("UPDATE mirror_of_kalandra SET quantity = :quantity WHERE username = :username",
               quantity=mirror_of_kalandra.quantity, username=username)
    db.execute("UPDATE dense_fossil SET quantity = :quantity WHERE username = :username",
               quantity=dense_fossil.quantity, username=username)
    db.execute("UPDATE serrated_fossil SET quantity = :quantity WHERE username = :username",
               quantity=serrated_fossil.quantity, username=username)
    db.execute("UPDATE pristine_fossil SET quantity = :quantity WHERE username = :username",
               quantity=pristine_fossil.quantity, username=username)
    db.execute("UPDATE deft_fossil SET quantity = :quantity WHERE username = :username",
               quantity=deft_fossil.quantity, username=username)
    db.execute("UPDATE fractured_fossil SET quantity = :quantity WHERE username = :username",
               quantity=fractured_fossil.quantity, username=username)


# def quantity_checker(row_name, instance_attribute, row_zero_attribute):
#
#     if len(row_name) == 0:
#         pass
#     else:
#         instance_attribute = row_zero_attribute


def delve_drop_rate(hoard):

    choice = random.randint(0, 100)
    if choice <= DELVE_DROP_RATE + (DELVE_DROP_RATE * player.item_quantity):
        pass
    else:
        monster = random.choice(hoard)

        if monster.delve_drop['name'] == 'Dense Fossil':
            dense_fossil.quantity = dense_fossil.quantity + 1
        elif monster.delve_drop['name'] == 'Serrated Fossil':
            serrated_fossil.quantity = serrated_fossil.quantity + 1
        elif monster.delve_drop['name'] == 'Pristine Fossil':
            pristine_fossil.quantity = pristine_fossil.quantity + 1
        elif monster.delve_drop['name'] == 'Pristine Fossil':
            pristine_fossil.quantity = pristine_fossil.quantity + 1
        elif monster.delve_drop['name'] == 'Deft Fossil':
            deft_fossil.quantity = deft_fossil.quantity + 1
        elif monster.delve_drop['name'] == 'Fractured Fossil':
            fractured_fossil.quantity = fractured_fossil.quantity + 1
        else:
            print('Erro 1')
            input('aguardar 1')
        print('-' * DASH)
        print(f"{monster.delve_drop['name']} dropped!")
        print('-' * DASH)
        time.sleep(0.3)
        playsound(DROP_1, False)
        time.sleep(0.1)


def delve_encounter():

    text = str(Delve.depth)
    depth = ' '.join(text)
    print('-' * DASH)
    print(f'...::: D E P T H   {depth}  :::...')
    print('-' * DASH)
    time.sleep(1)
    choice = random.randint(3, 5)
    hoard = []
    for i in range(0, choice):
        enemy_type_choice = random.choice(list(monster_type))
        enemy_dict = monster_type[enemy_type_choice]
        global enemy
        enemy = Monster(enemy_dict['name'],
                        enemy_dict['life'],
                        enemy_dict['attack'],
                        enemy_dict['defense'],
                        enemy_dict['level'],
                        enemy_dict['xp'],
                        enemy_dict['crit_chance'],
                        enemy_dict['delve_drop']
                        )
        hoard.append(enemy)
    for i in range(0, len(hoard)):
        hoard[i].life = hoard[i].life + hoard[i].life * Delve.multiplier
        hoard[i].attack = hoard[i].attack + hoard[i].attack * Delve.multiplier
        hoard[i].defense = hoard[i].defense + hoard[i].defense * Delve.multiplier
        hoard[i].crit_chance = hoard[i].crit_chance + hoard[i].crit_chance * Delve.multiplier
    print(f"You've encountered a hoard of {len(hoard)} monsters!")
    print('-' * DASH)
    time.sleep(2)

    # Delve battle
    for i in range(0, len(hoard)):
        while hoard[i].life > 0:
            if hoard[i].attack <= player.defense:
                player_damage = 0
                a = crit_chance(player.crit_chance, player.attack, player.crit_damage)

                if a > player.attack:
                    enemy_damage = a - hoard[i].defense
                    hoard[i].life = hoard[i].life - enemy_damage
                    player.life = player.life - player_damage
                    print(f"- CRITICAL HIT! You've attacked {hoard[i].name} and dealt {round(enemy_damage)} damage!")
                    critical_attack_sound()
                    time.sleep(0.5)
                    print(f"- {hoard[i].name} attacked you and dealt {round(player_damage)} damage!")
                    enemy_attack_sound()
                    time.sleep(0.5)
                else:
                    enemy_damage = player.attack - hoard[i].defense
                    hoard[i].life = hoard[i].life - enemy_damage
                    player.life = player.life - player_damage
                    print(f"- You've attacked {hoard[i].name} and dealt {round(enemy_damage)} damage!")
                    player_attack_sound()
                    print(f"- {hoard[i].name} attacked you and dealt {round(player_damage)} damage!")
                    enemy_attack_sound()
                    time.sleep(0.5)
            else:
                a = crit_chance(player.crit_chance, player.attack, player.crit_damage)
                b = crit_chance(hoard[i].crit_chance, hoard[i].attack, 1.4)

                if a > player.attack and b == hoard[i].attack:
                    enemy_damage = a - hoard[i].defense
                    player_damage = hoard[i].attack - player.defense
                    hoard[i].life = hoard[i].life - enemy_damage
                    player.life = player.life - player_damage
                    print(f"- CRITICAL HIT! You've attacked {hoard[i].name} and dealt {round(enemy_damage)} damage!")
                    critical_attack_sound()
                    print(f"- {hoard[i].name} attacked you and dealt {round(player_damage)} damage!")
                    enemy_attack_sound()
                    time.sleep(0.5)
                elif a > player.attack and b > hoard[i].attack:
                    enemy_damage = a - hoard[i].defense
                    player_damage = b - player.defense
                    hoard[i].life = hoard[i].life - enemy_damage
                    player.life = player.life - player_damage
                    print(f"- CRITICAL HIT! You've attacked {hoard[i].name} and dealt {round(enemy_damage)} damage!")
                    critical_attack_sound()
                    print(f"- CRITICAL HIT! {hoard[i].name} attacked you and dealt {round(player_damage)} damage!")
                    critical_attack_sound()

                elif a == player.attack and b > hoard[i].attack:
                    enemy_damage = player.attack - hoard[i].defense
                    player_damage = b - player.defense
                    hoard[i].life = hoard[i].life - enemy_damage
                    player.life = player.life - player_damage
                    print(f"- You've attacked {hoard[i].name} and dealt {round(enemy_damage)} damage!")
                    player_attack_sound()
                    print(f"- CRITICAL HIT! {hoard[i].name} attacked you and dealt {round(player_damage)} damage!")
                    critical_attack_sound()
                    time.sleep(0.5)
                else:
                    enemy_damage = player.attack - hoard[i].defense
                    player_damage = hoard[i].attack - player.defense
                    hoard[i].life = hoard[i].life - enemy_damage
                    player.life = player.life - player_damage
                    print(f"- You've attacked {hoard[i].name} and dealt {round(enemy_damage)} damage!")
                    player_attack_sound()
                    print(f"- {hoard[i].name} attacked you and dealt {round(player_damage)} damage!")
                    enemy_attack_sound()
                    time.sleep(0.5)
        if hoard[i].life < 0:
            hoard[i].life = 0
        check_player_life()
        print(f'\nYour life points: {round(player.life)}/{player.total_life}')
        print('-' * DASH)
        time.sleep(1)
    print(f'You have defeated all enemies of depth {Delve.depth}!')
    print(f'Your life points were fully restored!')
    print('-' * DASH)
    time.sleep(2)
    delve_drop_rate(hoard)
    player.life = player.total_life
    Delve.depth = Delve.depth + 1
    Delve.multiplier = Delve.multiplier + 0.01
    delve_save_state()
    save_state()
    choice = input('Press 1 to continue delving or 2 to return to delve menu: ')
    if choice == '1':
        delve_encounter()
    elif choice == '2':
        delve_menu()
    else:
        print('Wrong option..')
        time.sleep(1)
        delve_menu()


def delve_menu():

    if player.life != player.total_life:
        print('You need to have your life points fully restored before entering delve!')
        time.sleep(2)
        input('Press any key to continue... ')
    else:
        print('-' * DASH)
        print('...::: W E L C O M E  T O  D E L V E :::...')
        print('-' * DASH)
        choice = input('Press 1 to start delving or 2 to return to main menu: ')
        if choice == '1':
            delve_encounter()
        elif choice == '2':
            background_music()
            main_menu()
        else:
            print('Wrong option')
            time.sleep(1)
            delve_menu()


def delve_save_state():

    db.execute("UPDATE delve SET depth = :depth, multiplier = :multiplier WHERE username = :username",
               username=player.name, depth=Delve.depth, multiplier=Delve.multiplier)


def load_state():

    # Player Status
    username = input('Please type your username: ')
    rows = db.execute("SELECT * FROM user_data WHERE username = :username",
                      username=username)

    if len(rows) != 1:
        print('Wrong username!')
        time.sleep(0.5)
        login_menu()
    else:
        player.name = rows[0]['username']
        player.level = rows[0]['level']
        player.xp = rows[0]['experience']
        player.total_life = rows[0]['total_life']
        player.life = rows[0]['life']
        player.attack = rows[0]['attack']
        player.defense = rows[0]['defense']
        player.shaman = rows[0]['shaman']
        player.crit_chance = rows[0]['crit_chance']
        player.crit_damage = rows[0]['crit_damage']
        player.item_quantity = rows[0]['item_quantity']

    # Inventory
    rows2 = db.execute("SELECT * FROM inventory WHERE username = :username",
                       username=username)

    if len(rows2) < 1:
        pass

    else:
        for i in range(0, len(rows2)):
            new_item = Item(rows2[i]['type'], rows2[i]['name'], rows2[i]['level'],
                            rows2[i]['life'], rows2[i]['attack'],
                            rows2[i]['defense'], rows2[i]['crit_chance'],
                            rows2[i]['crit_damage'], rows2[i]['item_quantity'])
            inventory.append(new_item)

    # PlayerSlot
    row_amulet = db.execute("SELECT * FROM amulet WHERE username = :username", username=username)
    player_slot.amulet = row_amulet[0]
    row_armor = db.execute("SELECT * FROM armor WHERE username = :username", username=username)
    player_slot.armor = row_armor[0]
    row_gloves = db.execute("SELECT * FROM gloves WHERE username = :username", username=username)
    player_slot.gloves = row_gloves[0]
    row_helmet = db.execute("SELECT * FROM helmet WHERE username = :username", username=username)
    player_slot.helmet = row_helmet[0]
    row_legs = db.execute("SELECT * FROM legs WHERE username = :username", username=username)
    player_slot.legs = row_legs[0]
    row_ring1 = db.execute("SELECT * FROM ring1 WHERE username = :username", username=username)
    player_slot.ring1 = row_ring1[0]
    row_ring2 = db.execute("SELECT * FROM ring2 WHERE username = :username", username=username)
    player_slot.ring2 = row_ring2[0]
    row_second_hand = db.execute("SELECT * FROM second_hand WHERE username = :username", username=username)
    player_slot.second_hand = row_second_hand[0]
    row_weapon = db.execute("SELECT * FROM weapon WHERE username = :username", username=username)
    player_slot.weapon = row_weapon[0]
    row_boots = db.execute("SELECT * FROM boots WHERE username = :username", username=username)
    player_slot.boots = row_boots[0]

    # Consumables
    row_potion = db.execute("SELECT * FROM potion WHERE username = :username", username=username)
    potion.quantity = row_potion[0]['quantity']
    row_x_potion = db.execute("SELECT * FROM x_potion WHERE username = :username", username=username)
    x_potion.quantity = row_x_potion[0]['quantity']
    row_elixir = db.execute("SELECT * FROM elixir WHERE username = :username", username=username)
    elixir.quantity = row_elixir[0]['quantity']
    row_chaos_orb = db.execute("SELECT * FROM chaos_orb WHERE username = :username", username=username)
    chaos_orb.quantity = row_chaos_orb[0]['quantity']
    row_divine_orb = db.execute("SELECT * FROM divine_orb WHERE username = :username", username=username)
    divine_orb.quantity = row_divine_orb[0]['quantity']
    row_exalted_orb = db.execute("SELECT * FROM exalted_orb WHERE username = :username", username=username)
    exalted_orb.quantity = row_exalted_orb[0]['quantity']
    row_mirror_of_kalandra = db.execute("SELECT * FROM mirror_of_kalandra WHERE username = :username",
                                        username=username)
    mirror_of_kalandra.quantity = row_mirror_of_kalandra[0]['quantity']
    row_dense_fossil = db.execute("SELECT * FROM dense_fossil WHERE username = :username", username=username)
    dense_fossil.quantity = row_dense_fossil[0]['quantity']
    row_serrated_fossil = db.execute("SELECT * FROM serrated_fossil WHERE username = :username", username=username)
    serrated_fossil.quantity = row_serrated_fossil[0]['quantity']
    row_pristine_fossil = db.execute("SELECT * FROM pristine_fossil WHERE username = :username", username=username)
    pristine_fossil.quantity = row_pristine_fossil[0]['quantity']
    row_deft_fossil = db.execute("SELECT * FROM deft_fossil WHERE username = :username", username=username)
    deft_fossil.quantity = row_deft_fossil[0]['quantity']
    row_fractured_fossil = db.execute("SELECT * FROM fractured_fossil WHERE username = :username", username=username)
    fractured_fossil.quantity = row_fractured_fossil[0]['quantity']

    # boss instance
    row_boss_instance = db.execute("SELECT * FROM boss_instance WHERE username = :username", username=username)

    # Uniques_list
    row_uniques_list = db.execute("SELECT * FROM uniques_list WHERE username = :username", username=username)

    for i in range(0, len(row_uniques_list)):
        uniques_list.append(row_uniques_list[i]['name'])

    if row_boss_instance[0]['wiegraf1'] == 0:
        wiegraf1.status = False
    else:
        pass
    if row_boss_instance[0]['dycedarg1'] == 0:
        dycedarg1.status = False
    else:
        pass
    if row_boss_instance[0]['wiegraf2'] == 0:
        wiegraf2.status = False
    else:
        pass
    if row_boss_instance[0]['dycedarg2'] == 0:
        dycedarg2.status = False
    else:
        pass

    # Delve
    delve_rows = db.execute("SELECT * FROM delve WHERE username = :username",
                            username=username)
    Delve.depth = delve_rows[0]['depth']
    Delve.multiplier = delve_rows[0]['multiplier']

    print('-' * DASH)
    print(f"Welcome back, {player.name}")
    print('-' * DASH)
    background_music()
    time.sleep(2)


def register():

    username = input('Please choose and type a username: ')
    try:
        primary_key = db.execute("INSERT INTO users (username) VALUES (:username)",
                                 username=username)
    except:
        print('Username already exists!')
        time.sleep(1)
        register()

    db.execute(
        "INSERT INTO user_data (username, level, experience, total_life, life, attack, defense, shaman, crit_chance, crit_damage, item_quantity) VALUES (:username, :level, :experience, :total_life, :life, :attack, :defense,:shaman, :crit_chance, :crit_damage, :item_quantity)",
        username=username, level=player.level, experience=player.xp, total_life=player.total_life, life=player.life,
        attack=player.attack, defense=player.defense, shaman=player.shaman,
        crit_chance=player.crit_chance, crit_damage=player.crit_damage, item_quantity=player.item_quantity)

    rows = db.execute("SELECT * FROM users WHERE username = :username",
                      username=username)

    player.name = rows[0]['username']

    # Consumables Instance
    db.execute(
        "INSERT INTO potion (username, type, name, value, quantity, rarity, code, sound) VALUES (:username, :type, :name, :value, :quantity, :rarity, :code, :sound)",
        username=player.name, type=potion.type, name=potion.name, value=potion.value, quantity=potion.quantity,
        rarity=potion.rarity, code=potion.code, sound=potion.sound)
    db.execute(
        "INSERT INTO x_potion (username, type, name, value, quantity, rarity, code, sound) VALUES (:username, :type, :name, :value, :quantity, :rarity, :code, :sound)",
        username=player.name, type=x_potion.type, name=x_potion.name, value=x_potion.value, quantity=x_potion.quantity,
        rarity=x_potion.rarity, code=x_potion.code, sound=x_potion.sound)
    db.execute(
        "INSERT INTO elixir (username, type, name, value, quantity, rarity, code, sound) VALUES (:username, :type, :name, :value, :quantity, :rarity, :code, :sound)",
        username=player.name, type=elixir.type, name=elixir.name, value=elixir.value, quantity=elixir.quantity,
        rarity=elixir.rarity, code=elixir.code, sound=elixir.sound)
    db.execute(
        "INSERT INTO chaos_orb (username, type, name, value, quantity, rarity, code, sound) VALUES (:username, :type, :name, :value, :quantity, :rarity, :code, :sound)",
        username=player.name, type=chaos_orb.type, name=chaos_orb.name, value=chaos_orb.value,
        quantity=chaos_orb.quantity,
        rarity=chaos_orb.rarity, code=chaos_orb.code, sound=chaos_orb.sound)
    db.execute(
        "INSERT INTO divine_orb (username, type, name, value, quantity, rarity, code, sound) VALUES (:username, :type, :name, :value, :quantity, :rarity, :code, :sound)",
        username=player.name, type=divine_orb.type, name=divine_orb.name, value=divine_orb.value,
        quantity=divine_orb.quantity,
        rarity=divine_orb.rarity, code=divine_orb.code, sound=divine_orb.sound)
    db.execute(
        "INSERT INTO exalted_orb (username, type, name, value, quantity, rarity, code, sound) VALUES (:username, :type, :name, :value, :quantity, :rarity, :code, :sound)",
        username=player.name, type=exalted_orb.type, name=exalted_orb.name, value=exalted_orb.value,
        quantity=exalted_orb.quantity,
        rarity=exalted_orb.rarity, code=exalted_orb.code, sound=exalted_orb.sound)
    db.execute(
        "INSERT INTO mirror_of_kalandra (username, type, name, value, quantity, rarity, code, sound) VALUES (:username, :type, :name, :value, :quantity, :rarity, :code, :sound)",
        username=player.name, type=mirror_of_kalandra.type, name=mirror_of_kalandra.name,
        value=mirror_of_kalandra.value, quantity=mirror_of_kalandra.quantity,
        rarity=mirror_of_kalandra.rarity, code=mirror_of_kalandra.code, sound=mirror_of_kalandra.sound)
    db.execute(
        "INSERT INTO dense_fossil (username, type, name, value, quantity, rarity, code, sound, attribute) VALUES (:username, :type, :name, :value, :quantity, :rarity, :code, :sound, :attribute)",
        username=player.name, type=dense_fossil.type, name=dense_fossil.name,
        value=dense_fossil.value, quantity=dense_fossil.quantity,
        rarity=dense_fossil.rarity, code=dense_fossil.code, sound=dense_fossil.sound, attribute=dense_fossil.attribute)
    db.execute(
        "INSERT INTO serrated_fossil (username, type, name, value, quantity, rarity, code, sound, attribute) VALUES (:username, :type, :name, :value, :quantity, :rarity, :code, :sound, :attribute)",
        username=player.name, type=serrated_fossil.type, name=serrated_fossil.name,
        value=serrated_fossil.value, quantity=serrated_fossil.quantity,
        rarity=serrated_fossil.rarity, code=serrated_fossil.code, sound=serrated_fossil.sound,
        attribute=serrated_fossil.attribute)
    db.execute(
        "INSERT INTO pristine_fossil (username, type, name, value, quantity, rarity, code, sound, attribute) VALUES (:username, :type, :name, :value, :quantity, :rarity, :code, :sound, :attribute)",
        username=player.name, type=pristine_fossil.type, name=pristine_fossil.name,
        value=pristine_fossil.value, quantity=pristine_fossil.quantity,
        rarity=pristine_fossil.rarity, code=pristine_fossil.code, sound=pristine_fossil.sound,
        attribute=pristine_fossil.attribute)
    db.execute(
        "INSERT INTO deft_fossil (username, type, name, value, quantity, rarity, code, sound, attribute) VALUES (:username, :type, :name, :value, :quantity, :rarity, :code, :sound, :attribute)",
        username=player.name, type=deft_fossil.type, name=deft_fossil.name,
        value=deft_fossil.value, quantity=deft_fossil.quantity,
        rarity=deft_fossil.rarity, code=deft_fossil.code, sound=deft_fossil.sound, attribute=deft_fossil.attribute)
    db.execute(
        "INSERT INTO fractured_fossil (username, type, name, value, quantity, rarity, code, sound, attribute) VALUES (:username, :type, :name, :value, :quantity, :rarity, :code, :sound, :attribute)",
        username=player.name, type=fractured_fossil.type, name=fractured_fossil.name,
        value=fractured_fossil.value, quantity=fractured_fossil.quantity,
        rarity=fractured_fossil.rarity, code=fractured_fossil.code, sound=fractured_fossil.sound,
        attribute=fractured_fossil.attribute)

    # Boss instance
    db.execute(
        "INSERT INTO boss_instance (username, wiegraf1, dycedarg1, wiegraf2, dycedarg2) VALUES (:username, :wiegraf1, :dycedarg1, :wiegraf2, :dycedarg2)",
        username=player.name, wiegraf1=1, dycedarg1=1, wiegraf2=1, dycedarg2=1)

    # Delve instance
    db.execute(
        "INSERT INTO delve (username, depth, multiplier) VALUES (:username, :depth, :multiplier)",
        username=player.name, depth=1, multiplier=0.01)

    print('-' * DASH)
    print(f"You've been registered!, {player.name}. Since usernames are canse-sensitive,"
          f" make sure you write yours down to use it correctly later.")
    print('-' * DASH)
    input('Press any key to continue... ')
    print('-' * DASH)
    print(f'Welcome to the kingdom of Ivalice, {player.name}!')
    print('-' * DASH)
    background_music()
    time.sleep(2)
    main_menu()


def login_menu():

    print('-' * DASH)
    print('1  New Game (register new username)\n'
          '2  Load Game')
    print('-' * DASH)
    choice = input('Select an option: ')
    if choice == '1':
        register()
    elif choice == '2':
        load_state()
        main_menu()
    else:
        print('Wrong option')
        time.sleep(1)
        login_menu()


def main_menu():

    if player.level != 20 and dycedarg2.status is True:
        print('1   Start Battle\n'
              '2   Inventory\n'
              '3   Consumable Items\n'
              '4   Player Status\n'
              '5   Help\n'
              '6   Exit Game\n')
        choice = (input('Select an option: '))
        try:
            if choice == '1':
                encounter()
            elif choice == '2':
                show_inventory()
            elif choice == '3':
                show_consumable_items()
            elif choice == '4':
                player_status()
            elif choice == '5':
                player_status()
            elif choice == '6':
                choice = input('Are you sure you want to exit the game? Press 1 to confirm or 2 to cancel: ')
                if choice == '1':
                    quit()
                elif choice == '2':
                    main_menu()
            else:
                print('Wrong option!')
                time.sleep(1)
                main_menu()
        except ValueError:
            main_menu()
    else:
        choice = (input('Select an option:\n'
                        '1   Start Battle\n'
                        '2   Inventory\n'
                        '3   Consumable Items\n'
                        '4   Player Status\n'
                        '5   Delve\n'
                        '6   Endgame Bosses\n'
                        '7   Help\n'
                        '8   Exit Game\n\n'))
        try:
            if choice == '1':
                encounter()
            elif choice == '2':
                show_inventory()
            elif choice == '3':
                show_consumable_items()
            elif choice == '4':
                player_status()
            elif choice == '5':
                pygame.mixer.music.fadeout(2)
                pygame.mixer.music.stop()
                delve_music()
                delve_menu()
                pygame.mixer.music.fadeout(2)
                pygame.mixer.music.stop()
                background_music()
                main_menu()
            elif choice == '6':
                main_menu()
            elif choice == '7':
                main_menu()
            elif choice == '8':
                choice = input('Are you sure you want to exit the game? Press 1 to confirm or 2 to cancel: ')
                if choice == '1':
                    quit()
                elif choice == '2':
                    main_menu()
            else:
                print('Wrong option!')
                time.sleep(1)
                main_menu()
        except ValueError:
            main_menu()


if __name__ == '__main__':

    # Level 1 player instance
    player = Player('unknown', 500, 500, 100, 100, 1, 0, 1, 15, 1.4, 0)
    player_slot = PlayerSlot(amulet=amulet_type[0],
                             armor=armor_type[0],
                             gloves=gloves_type[0],
                             helmet=helmet_type[0],
                             legs=legs_type[0],
                             ring1=ring_type[0],
                             ring2=ring_type[0],
                             second_hand=second_hand_type[0],
                             weapon=weapon_type[0],
                             boots=boots_type[0])
    # Boss instances:
    wiegraf1 = Character(
        name=characters['Wiegraf 1']['name'],
        life=characters['Wiegraf 1']['life'],
        attack=characters['Wiegraf 1']['attack'],
        defense=characters['Wiegraf 1']['defense'],
        level=characters['Wiegraf 1']['level'],
        xp=characters['Wiegraf 1']['xp'],
        crit_chance=characters['Wiegraf 1']['crit_chance'],
        status=characters['Wiegraf 1']['status'],
        quote1=characters['Wiegraf 1']['quote1'],
        quote2=characters['Wiegraf 1']['quote2'],
        quote3=characters['Wiegraf 1']['quote3'],
    )
    dycedarg1 = Character(
        name=characters['Dycedarg 1']['name'],
        life=characters['Dycedarg 1']['life'],
        attack=characters['Dycedarg 1']['attack'],
        defense=characters['Dycedarg 1']['defense'],
        level=characters['Dycedarg 1']['level'],
        xp=characters['Dycedarg 1']['xp'],
        crit_chance=characters['Dycedarg 1']['crit_chance'],
        status=characters['Dycedarg 1']['status'],
        quote1=characters['Dycedarg 1']['quote1'],
        quote2=characters['Dycedarg 1']['quote2'],
        quote3=characters['Dycedarg 1']['quote3'],
    )
    wiegraf2 = Character(
        name=characters['Wiegraf 2']['name'],
        life=characters['Wiegraf 2']['life'],
        attack=characters['Wiegraf 2']['attack'],
        defense=characters['Wiegraf 2']['defense'],
        level=characters['Wiegraf 2']['level'],
        xp=characters['Wiegraf 2']['xp'],
        crit_chance=characters['Wiegraf 2']['crit_chance'],
        status=characters['Wiegraf 2']['status'],
        quote1=characters['Wiegraf 2']['quote1'],
        quote2=characters['Wiegraf 2']['quote2'],
        quote3=characters['Wiegraf 2']['quote3'],
    )
    dycedarg2 = Character(
        name=characters['Dycedarg 2']['name'],
        life=characters['Dycedarg 2']['life'],
        attack=characters['Dycedarg 2']['attack'],
        defense=characters['Dycedarg 2']['defense'],
        level=characters['Dycedarg 2']['level'],
        xp=characters['Dycedarg 2']['xp'],
        crit_chance=characters['Dycedarg 2']['crit_chance'],
        status=characters['Dycedarg 2']['status'],
        quote1=characters['Dycedarg 2']['quote1'],
        quote2=characters['Dycedarg 2']['quote2'],
        quote3=characters['Dycedarg 2']['quote3'],
    )

    # Consumables intances:
    potion = ConsumableItem(consumables['potion']['type'], consumables['potion']['name'],
                            consumables['potion']['value'], consumables['potion']['quantity'],
                            consumables['potion']['rarity'], consumables['potion']['code'],
                            consumables['potion']['sound'])
    hi_potion = ConsumableItem(consumables['hi-potion']['type'], consumables['hi-potion']['name'],
                               consumables['hi-potion']['value'], consumables['hi-potion']['quantity'],
                               consumables['hi-potion']['rarity'], consumables['hi-potion']['code'],
                               consumables['hi-potion']['sound'])
    x_potion = ConsumableItem(consumables['x-potion']['type'], consumables['x-potion']['name'],
                              consumables['x-potion']['value'], consumables['x-potion']['quantity'],
                              consumables['x-potion']['rarity'], consumables['x-potion']['code'],
                              consumables['x-potion']['sound'])
    elixir = ConsumableItem(consumables['elixir']['type'], consumables['elixir']['name'],
                            consumables['elixir']['value'], consumables['elixir']['quantity'],
                            consumables['elixir']['rarity'], consumables['elixir']['code'],
                            consumables['elixir']['sound'])
    chaos_orb = ConsumableItem(consumables['chaos orb']['type'], consumables['chaos orb']['name'],
                               consumables['chaos orb']['value'], consumables['chaos orb']['quantity'],
                               consumables['chaos orb']['rarity'], consumables['chaos orb']['code'],
                               consumables['chaos orb']['sound'])
    divine_orb = ConsumableItem(consumables['divine orb']['type'], consumables['divine orb']['name'],
                                consumables['divine orb']['value'], consumables['divine orb']['quantity'],
                                consumables['divine orb']['rarity'], consumables['divine orb']['code'],
                                consumables['divine orb']['sound'])
    exalted_orb = ConsumableItem(consumables['exalted orb']['type'], consumables['exalted orb']['name'],
                                 consumables['exalted orb']['value'], consumables['exalted orb']['quantity'],
                                 consumables['exalted orb']['rarity'], consumables['exalted orb']['code'],
                                 consumables['exalted orb']['sound'])
    mirror_of_kalandra = ConsumableItem(consumables['mirror of kalandra']['type'],
                                        consumables['mirror of kalandra']['name'],
                                        consumables['mirror of kalandra']['value'],
                                        consumables['mirror of kalandra']['quantity'],
                                        consumables['mirror of kalandra']['rarity'],
                                        consumables['mirror of kalandra']['code'],
                                        consumables['mirror of kalandra']['sound'])

    # Fossiles
    dense_fossil = Fossil(consumables['dense fossil']['type'],
                          consumables['dense fossil']['name'],
                          consumables['dense fossil']['value'],
                          consumables['dense fossil']['quantity'],
                          consumables['dense fossil']['rarity'],
                          consumables['dense fossil']['code'],
                          consumables['dense fossil']['sound'],
                          consumables['dense fossil']['attribute'])
    serrated_fossil = Fossil(consumables['serrated fossil']['type'],
                             consumables['serrated fossil']['name'],
                             consumables['serrated fossil']['value'],
                             consumables['serrated fossil']['quantity'],
                             consumables['serrated fossil']['rarity'],
                             consumables['serrated fossil']['code'],
                             consumables['serrated fossil']['sound'],
                             consumables['serrated fossil']['attribute'])
    pristine_fossil = Fossil(consumables['pristine fossil']['type'],
                             consumables['pristine fossil']['name'],
                             consumables['pristine fossil']['value'],
                             consumables['pristine fossil']['quantity'],
                             consumables['pristine fossil']['rarity'],
                             consumables['pristine fossil']['code'],
                             consumables['pristine fossil']['sound'],
                             consumables['pristine fossil']['attribute'])
    deft_fossil = Fossil(consumables['deft fossil']['type'],
                         consumables['deft fossil']['name'],
                         consumables['deft fossil']['value'],
                         consumables['deft fossil']['quantity'],
                         consumables['deft fossil']['rarity'],
                         consumables['deft fossil']['code'],
                         consumables['deft fossil']['sound'],
                         consumables['deft fossil']['attribute'])
    fractured_fossil = Fossil(consumables['fractured fossil']['type'],
                              consumables['fractured fossil']['name'],
                              consumables['fractured fossil']['value'],
                              consumables['fractured fossil']['quantity'],
                              consumables['fractured fossil']['rarity'],
                              consumables['fractured fossil']['code'],
                              consumables['fractured fossil']['sound'],
                              consumables['fractured fossil']['attribute'])
    login_menu()
