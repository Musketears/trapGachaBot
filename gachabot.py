import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='~',intents=intents)

is_stop = False
is_processing = False
current_file = ''
balances_file = 'user_balances.json'
user_balances = {}
user_persons = {}
person_pool = ["Alex","Ryan","Priscilla","Jackson","Holli","Nathan"]
#adjective additional sell value will be equal to index of this list
adjectives_pool = ["Default", "Homeless", "Mentally Challenged", "Boring", "Sleepy", "Smoll", "Tilted", "Large", "Goated"]


def update_balance(id, amount):
    global user_balances
    if id in user_balances:
        user_balances[id] += amount
    else:
        user_balances[id] = 100 + amount
    with open(balances_file, 'w') as file:
        json.dump(user_balances, file)

def load_balances():
    global user_balances
    try:
        file = open(balances_file, 'r')
        user_balances = json.load(file)
    except FileNotFoundError:
        user_balances = {}

def update_persons(id, person_in):
    global user_persons
    if id in user_persons:
        user_persons[id].append({'person':person_in})
    else:
        user_persons[id].append({'person':'3 ★ Default Person'})
    with open(balances_file, 'w') as file:
        json.dump(user_persons, file)

def load_persons():
    global user_persons
    try:
        file = open(balances_file, 'r')
        user_persons = json.load(file)
    except FileNotFoundError:
        user_persons = {}

@bot.command(name='pull', help='Pulls 1 person. Cost = 10')
async def pull(ctx):
    global person_pool
    global adjectives_pool
    user_id = str(ctx.author.id)
    if user_id not in user_balances:
        update_balance(user_id, 0)

    bet = 15

    if bet > user_balances[user_id]:
        await ctx.send("You're too poor to play.")
        return

    update_balance(user_id, -bet)
    
   #detemines rarity
    new_person = ""
    result = random.randint(1,100)
    if result == 1:
        new_person = '5 ★ '

    if result >= 2 and result <= 15:
        new_person = '4 ★ '

    if result >= 15 and result <= 50:
        new_person = '3 ★ '
    else:
        new_person = '2 ★ '
    
    #pick random adjective
    new_person = new_person + random.choice(adjectives_pool) + " "
    #pick random person
    new_person = new_person + random.choice(person_pool)
    

    update_persons(user_id, new_person)
    await ctx.send(f"Congratulation! You got a {new_person}!\nYour new balance is: {user_balances[user_id]}.")

#TODO add a sell command

@bot.command(name='balance', help='Check your balance')
async def balance(ctx):
    global user_balances
    user_id = str(ctx.author.id)
    if user_id not in user_balances:
        await ctx.send("You are a new player. Your balance is 100 to start.")
    else:
        await ctx.send(f"Your current balance is {user_balances[user_id]}.")

@bot.command(name='gacha_inv', help='Check your gacha inventory')
async def gacha_inv(ctx):
    global user_persons
    output_str = ""
    user_id = str(ctx.author.id)
    if user_id not in user_balances:
        await ctx.send("You are a new player. You have a 3 ★ Default Person to start.")
    else:
        for person in user_persons:
            for attribute, value in person.items():
                output_str = attribute + ", " + value + "\n"
        await ctx.send(output_str)

if __name__ == "__main__" :
    load_balances()
    bot.run(TOKEN)
