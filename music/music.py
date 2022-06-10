import pygame, sys
from main import *
from settings import *
import time


def background_music():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(BACKGROUND_SONG)
    pygame.mixer.music.set_volume(0.4) # Now plays at 50% of full volume. 0.4
    pygame.mixer.music.play(-1)


def boss_music():
    pygame.mixer.music.fadeout(2)
    pygame.mixer.music.stop()
    pygame.mixer.music.load(BOSS_FIGHT_SONG)
    pygame.mixer.music.set_volume(0.3) # Now plays at 50% of full volume.  0.3
    pygame.mixer.music.play(-1)


def delve_music():
    pygame.mixer.music.fadeout(2)
    pygame.mixer.music.stop()
    pygame.mixer.music.load(DELVE)
    pygame.mixer.music.set_volume(0.3) # Now plays at 50% of full volume.  0.3
    pygame.mixer.music.fadeout(2)
    pygame.mixer.music.stop()
    pygame.mixer.music.play(-1)


def player_attack_sound():
    time.sleep(0.2)
    # playsound(PLAYER_ATTACK)
    p_a_s = pygame.mixer.Sound(PLAYER_ATTACK)
    p_a_s.set_volume(0.5) # Now plays at 50% of full volume.
    p_a_s.play(0)
    time.sleep(0.3)


def enemy_attack_sound():
    time.sleep(0.2)
    # playsound(ENEMY_ATTACK)
    e_a_s = pygame.mixer.Sound(ENEMY_ATTACK)
    e_a_s.set_volume(0.5) # Now plays at 50% of full volume.
    e_a_s.play(0)
    time.sleep(0.3)


def critical_attack_sound():
    time.sleep(0.2)
    # playsound(CRITICAL_ATTACK)
    c_s = pygame.mixer.Sound(CRITICAL_ATTACK)
    c_s.set_volume(0.6)  # Now plays at 50% of full volume.
    c_s.play(0)
    time.sleep(0.3)


def game_over_sound():
    pygame.mixer.music.fadeout(2)
    pygame.mixer.music.stop()
    time.sleep(1)
    pygame.mixer.music.load(GAME_OVER)
    pygame.mixer.music.set_volume(0.5) # Now plays at 50% of full volume.
    pygame.mixer.music.play()