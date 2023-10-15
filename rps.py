import random

def play(move):
    rock = "Rock"
    paper = "Paper"
    scissors = "Scissors"

    if move == 'rock':
        move = rock
    elif move == 'paper':
        move = paper
    elif move == 'scissors':
        move = scissors

    hand = [rock, paper, scissors]
    com_pick = random.choice(hand)
    if move == rock:
        if com_pick == rock:
            match = "draw"
        if com_pick == paper:
            match = "lose"
        if com_pick == scissors:
            match = "win"

    if move == paper:
        if com_pick == rock:
            match = "win"
        if com_pick == paper:
            match = "draw"
        if com_pick == scissors:
            match = "lose"

    if move == scissors:
        if com_pick == rock:
            match = "lose"
        if com_pick == paper:
            match = "win"
        if com_pick == scissors:
            match = "draw"
    print(move, com_pick)
    return match
    
# print(play('scissors'))

wizard = "Wizard"
wizard_hp = 70
wizard_dmg = 150

human = "Human"
human_hp = 150
human_dmg = 20

elf = "Elf"
elf_hp = 100
elf_dmg = 100

orc = "Orc"
orc_hp = 170
orc_dmg = 70

dragon_hp = 300
dragon_dmg = 50
