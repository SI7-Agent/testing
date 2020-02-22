import csv
import random
import os
import nickname_generator
import faker

month = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

addons = [
    "Black Mountain",
    "Curse of Naxxramas",
    "Goblines and gnomes",
    "Grand tournament",
    "Whispers of the old gods",
    "One night in Karazhan",
    "Mean streets of Gadgetzan",
    "Ungoro's exploring",
    "Knights of frozen throne",
    "Cobolds and catacombs",
    "Witchwood",
    "Boomsday project",
    "Rastakhan's rumble",
    "Rise of shadows",
    "Uldum's saviors"
]

races = [
    "Murloc",
    "Beast",
    "Dragon",
    "Totem",
    "Mechanism",
    "Demon",
    "Elemental",
    "Pirat"
]

rarity = [
    "Base",
    "Common",
    "Rare",
    "Epic",
    "Legendary"
]

ability = [
    "Taunt",
    "Battle cry",
    "Stealth",
    "Rush",
    "Windfury",
    "Poisonous",
    "Lifesteal",
    "Divine shield",
    "Deathrattle",
    "Mega windfury",
    "Non-target",
    "Overkill"
]

mode = [
    "Arena",
    "Adventure",
    "Brawl",
    "Rating game",
    "Free game"
]

gameplay = [
    "Own 30 cards deck",
    "Building a deck on the go",
    "Building a deck on the go with actual cards",
    "Deck of developers"
]

def create_copy(clone):
    copy = []

    for i in clone:
        copy.append(i)

    return copy

def pair_generator():
    rec = ""

    random.seed()
    num1 = random.randint(1, 1000)

    random.seed()
    num2 = random.randint(1, 1000)

    if num1 == num2:
        while num1 == num2:
            random.seed()
            num1 = random.randint(1, 1000)

            random.seed()
            num2 = random.randint(1, 1000)

    rec += str(num1)
    rec += ','
    rec += str(num2)

    return rec

def day_generator(month, year):
    day = 0

    if month in [0, 2, 4, 6, 7, 9, 11]:
        day = random.randint(1, 31)
    elif month == 1:
        if not year%4:
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 28)
    else:
        day = random.randint(1, 30)

    return day

def date_generator():
    global month
    month_num = random.randint(0,11)
    year = random.randint(2014,2019)
    day = day_generator(month_num, year)

    ready_str = ""
    ready_str += str(day) + " "
    ready_str += month[month_num] + " "
    ready_str += str(year)

    return ready_str

def generate_addons():
    global addons

    FILENAME = 'addon_database.csv'

    random.seed()
    if os.path.exists(FILENAME):
        with open(FILENAME, "a", newline="") as file:
            writer = csv.writer(file)
            for i in range(len(addons)):
                rec = ""
                rec += str(i+1) #id
                rec += ','
                rec += addons[i] #name
                rec += ','
                rec += date_generator() #date
                writer.writerow(rec.split(','))
    else:
        f = open(FILENAME, "w", newline="")
        f.close()
        generate_addons()

def generate_cards():
    global addons, races, ability, rarity

    FILENAME = 'card_database.csv'

    random.seed()
    if os.path.exists(FILENAME):
        with open(FILENAME, "a", newline="") as file:
            writer = csv.writer(file)
            for i in range(1000):
                rec = ""
                rec += str(i+1) #id
                rec += ','
                rec += faker.Faker().name() #name
                rec += ','
                rec += str(random.randint(1, len(addons))) #id_addon
                rec += ','
                rec += races[random.randint(0, len(races) - 1)] #race
                rec += ','
                rec += ability[random.randint(0, len(ability) - 1)] #ability
                rec += ','
                rec += rarity[random.randint(0, len(rarity) - 1)] #rarity
                rec += ','
                rec += str(random.randint(1, 20)) #health
                rec += ','
                rec += str(random.randint(0, 20)) #attack
                rec += ','
                rec += str(random.randint(0, 25)) #manacost
                writer.writerow(rec.split(','))
    else:
        f = open(FILENAME, "w", newline="")
        f.close()
        generate_cards()

def generate_modes():
    global mode

    FILENAME = 'mode_database.csv'

    random.seed()
    if os.path.exists(FILENAME):
        with open(FILENAME, "a", newline="") as file:
            writer = csv.writer(file)
            for i in range(len(mode)):
                rec = ""
                rec += str(i + 1) #id
                rec += ','
                rec += mode[i] #mode_name
                rec += ','
                cost = random.randint(1,3)
                if cost == 1:
                    rec += "Free" #cost
                elif cost == 2:
                    rec += "700 of gold"
                elif cost == 3:
                    rec += "60 usd"
                writer.writerow(rec.split(','))
    else:
        f = open(FILENAME, "w", newline="")
        f.close()
        generate_modes()

def generate_histories():
    FILENAME = 'history_database.csv'

    random.seed()
    if os.path.exists(FILENAME):
        with open(FILENAME, "a", newline="") as file:
            writer = csv.writer(file)
            n_ch = [i for i in range (1, 1001)]
            for i in range(1000):
                rec = ""
                rec += str(i+1) #id
                rec += ','
                m = random.randint(0,len(n_ch) - 1)
                rec += str(n_ch[m]) #id_game
                n_ch.remove(n_ch[m])
                rec += ','
                rec += str(random.randint(1, 45)) #turn_num
                rec += ','
                rec += str(random.randint(1, 1000)) #last_card
                writer.writerow(rec.split(','))
    else:
        f = open(FILENAME, "w", newline="")
        f.close()
        generate_histories()

def generate_gameplays():
    global mode, gameplay

    FILENAME = 'gameplay_database.csv'

    random.seed()
    if os.path.exists(FILENAME):
        with open(FILENAME, "a", newline="") as file:
            writer = csv.writer(file)
            k = 1
            for i in range (len(mode)):
                num = random.randint(1, len(gameplay))
                g_ch = create_copy(gameplay)
                for j in range (num):
                    rec = ""
                    rec += str(k) #id
                    rec += ","
                    rec += str(i+1) #id_mode
                    rec += ","
                    m = random.randint(0, len(g_ch) - 1)
                    rec += g_ch[m] #gameplay
                    g_ch.remove(g_ch[m])
                    k += 1
                    writer.writerow(rec.split(','))
    else:
        f = open(FILENAME, "w", newline="")
        f.close()
        generate_gameplays()


def generate_players():
    FILENAME = "player_database.csv"

    random.seed()
    if os.path.exists(FILENAME):
        with open(FILENAME, "a", newline="") as file:
            writer = csv.writer(file)
            for i in range(1000):
                rec = ""
                rec += str(i+1) #id
                rec += ","
                rec += nickname_generator.generate() #nickname
                writer.writerow(rec.split(','))
    else:
        f = open(FILENAME, "w", newline="")
        f.close()
        generate_players()

def generate_games():
    global mode

    FILENAME = "game_database.csv"

    random.seed()
    if os.path.exists(FILENAME):
        with open(FILENAME, "a", newline="") as file:
            writer = csv.writer(file)
            for i in range(1000):
                rec = ""
                rec += str(i + 1)
                rec += ","
                rec += pair_generator() #id_players
                rec += ","
                rec += str(random.randint(1,2)) #winner
                rec += ","
                rec += str(random.randint(1, len(mode))) #mode_played
                writer.writerow(rec.split(','))
    else:
        f = open(FILENAME, "w", newline="")
        f.close()
        generate_games()

generate_gameplays()
# generate_addons()
# generate_players()
# generate_cards()
# generate_games()
# generate_histories()
# generate_modes()
#manacost, health, damage
#