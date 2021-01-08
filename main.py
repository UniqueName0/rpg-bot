import os
import discord
from discord.ext import commands, tasks
import sqlite3
import random

conn = sqlite3.connect('rpg.db')
token = os.getenv('token')

helptext = open('help.txt', 'r').read()

rpgdata = conn.cursor()
rpgdata.execute('''CREATE TABLE IF NOT EXISTS rpgdb (userID, gold, level, xp_needed, hp_potions, weapon, weapon_level, health, damage, armor, evasion)''')
conn.commit()

bot = commands.Bot(command_prefix='-')

bot.remove_command('help')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(activity=discord.Game('-help'))

@bot.command()
async def help(ctx):
    await ctx.send(helptext)

@bot.command()
async def stats(ctx):
    user = ctx.author
    await create_account()
    em = discord.Embed(title = f"{ctx.author.name}'s stats", color = discord.Color.red())
    em.add_field(name = "gold", value = rpgdata.execute("SELECT gold FROM rpgdb WHERE userID = ?", user.id).fetchone())
    await ctx.send(embed = em)


async def create_account:
    if rpgdata.execute("SELECT 1 FROM rpgdb WHERE userID = ?", user.id).fetchone():
        return False
    else:
        rpgdata.execute("INSERT INTO rpgdb VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user.id, 100, 1, 100, 5, "sword", 1, 100, 20, 5, 5)   
        conn.commit()
    
   
bot.run(token)
