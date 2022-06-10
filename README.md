# FFTacticsMeetsPoe

## Introduction

This is an ongoing project I started last week and have been "literally" playing around it. It consists of a terminal-based game that have characters from the Final Fantasy Tactics series, only with some Path of Exile mechanics.

It's quite simple: a progression rpg where the player has to face increasingly stronger enemies. Most of these mobs were taken out from the Final Fantasy Tactics series. I've got the battle system idea from another game, which is available at Play Store, named The Simplest RPG, then added to it with other mechanics inspired from Path of Exile, a game I've always been a huge fan.

The "story mode"  is pretty straightforward: you start at level 1 and goes till level 20. Among the regular mobs, you also face some stronger bosses.

Enemies have a change of dropping gear or consumable items. There are 9 different types of gear, and each type have various different options. All of them have several attributes that help increase player's own (in addition to the level up bonuses). Whereas consumable items helps restore player life and have other use as well.

After killing the last boss at level 20, you reach the endgame, where several other mechanics and systems are opened. The main one is Delve, which, similarly to poe's mechanic, the aim to go do deeper into it by killing all monsters. After killing a pack of monster in ther first depth, you move onto the second one, and so on. There's a multiplier applied each depth you conquer, so mobs gets all their statuses increased gradually, therefore, delve's levels are limiteless as long as the player manages to kill all the mobs of that depth.

Another endgame mechanics is Fossils, which are dropped by delve mobs and allow players to reforge their gear beyound the attribute limits (with also a small chance of destroying such item instead.)

So as to guarantee playability and progression, all the progress, as well as player's inventory, is saved into a database to be accessed later.

## How To Install/Run
- Just run main.py at your terminal
- The player choices are made throgh terminal input requests, most of the time by pressing any key or numbers 1 or 2.

## Requirements / Libraries
- Pygame (to enable game music/sound)
- Playsound (to enable game music/sound)
- SQL (from the cs50 package)

## Printscreens
- Main Menu
 
![main_menu](https://user-images.githubusercontent.com/52802728/173128968-2c79e0c6-5af3-4e3c-bf44-bc869390fa28.png)

- Battle System
 
![battle_system](https://user-images.githubusercontent.com/52802728/173129457-64e9cb5b-2cb3-4913-8581-43de19174db1.png)

- Player's Inventory

![inventory](https://user-images.githubusercontent.com/52802728/173129764-e5c9523f-573c-4622-a81a-8e8cb6626d09.png)

- Consumables

![consumables](https://user-images.githubusercontent.com/52802728/173129897-4a23ea24-fae0-4c34-b676-3c23deb719ac.png)

- Delve

![consumables](https://user-images.githubusercontent.com/52802728/173130345-aacb65b2-3116-4a2b-a279-3f185f9a4dc2.png)


