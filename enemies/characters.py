from main import *
from settings import *
import pygame

# def __init__(self, name, life, attack, defense, level, xp, crit_chance, status, quote1, quote2, quote3):

# --------------------------------------------------------------------------------------------------------------
# wiegraf1 = Character('Wiegraf', 1500, 120, 30, 5, 150, 50)
# --------------------------------------------------------------------------------------------------------------


characters = {
    'Wiegraf 1': {'name': 'Wiegraf',
                  'life': 1000,
                  'attack': 140,
                  'defense': 40,
                  'level': 5,
                  'xp': 150,
                  'crit_chance': 40,
                  'status': True,
                  'quote1': "You'll never know the feeling of the 'Meager'.\n"
                            "You may think you know it, but you've never lived it! Behold my full power!\n",
                  'quote2': "aarrgh.. this cannot be true... ",
                  'quote3': ''},

    'Dycedarg 1': {'name': 'Dycedarg',
                   'life': 1800,
                   'attack': 270,
                   'defense': 65,
                   'level': 10,
                   'xp': 400,
                   'crit_chance': 40,
                   'status': True,
                   'quote1': "Is it not I? I, who have dirtied my hands to keep yours clean?\n"
                             "All that you are you owe to me! You ought be on your knees thanking me,\n"
                             "yet here you stand in judgment!\n",
                   'quote2': 'aaaaaaaargh',
                   'quote3': ''},

    'Wiegraf 2': {'name': 'Wiegraf, Corpse Brigade Head',
                  'life': 2600,
                  'attack': 440,
                  'defense': 100,
                  'level': 15,
                  'xp': 1000,
                  'crit_chance': 40,
                  'status': True,
                  'quote1': "And then we meet again, Ramza\n"
                            "I guess you wasn't expecting this unforeseen turn of events!\n"
                            "You'll regreat crossing my path a second time!\n",
                  'quote2': "AAAARRRRRRRRRGHH",
                  'quote3': ''},

    'Dycedarg 2': {'name': 'Dycedarg, the Betrayer God',
                   'life': 6000,
                   'attack': 850,
                   'defense': 150,
                   'level': 20,
                   'xp': 0,
                   'crit_chance': 40,
                   'status': True,
                   'quote1': "Come! I will show you that common blood makes naught but a common man!\n"
                             "Face the revenge of the Fallen God\n",
                   'quote2': 'AAAAAAAAAAARGH, MY BELOVED REALM OF IVALICE...\n',
                   'quote3': ''}
}
