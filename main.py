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
    await create_account(user)
    em = discord.Embed(title = f"{ctx.author.name}'s stats", color = discord.Color.red())
    em.add_field(name = "gold", value = rpgdata.execute("SELECT gold FROM rpgdb WHERE userID = ?", (user.id,)).fetchone())
    em.add_field(name = "level", value = rpgdata.execute("SELECT level FROM rpgdb WHERE userID = ?", (user.id,)).fetchone())
    em.add_field(name = "xp needed for level up", value = rpgdata.execute("SELECT xp_needed FROM rpgdb WHERE userID = ?", (user.id,)).fetchone())
    em.add_field(name = "hp_potions", value = rpgdata.execute("SELECT hp_potions FROM rpgdb WHERE userID = ?", (user.id,)).fetchone())
    em.add_field(name = "weapon", value = rpgdata.execute("SELECT weapon FROM rpgdb WHERE userID = ?", (user.id,)).fetchone())
    em.add_field(name = "weapon level", value = rpgdata.execute("SELECT weapon_level FROM rpgdb WHERE userID = ?", (user.id,)).fetchone())
    em.add_field(name = "health", value = rpgdata.execute("SELECT health FROM rpgdb WHERE userID = ?", (user.id,)).fetchone())
    em.add_field(name = "damage", value = rpgdata.execute("SELECT damage FROM rpgdb WHERE userID = ?", (user.id,)).fetchone())
    em.add_field(name = "armor", value = rpgdata.execute("SELECT armor FROM rpgdb WHERE userID = ?", (user.id,)).fetchone())
    em.add_field(name = "evasion", value = rpgdata.execute("SELECT evasion FROM rpgdb WHERE userID = ?", (user.id,)).fetchone())
    await ctx.send(embed = em)

@bot.command()
async def arena(ctx,arg):
    user = ctx.author
    await create_account(user)
    hp = rpgdata.execute("select health from rpgdb where userID=?", (user.id,))
    dmg = rpgdata.execute("select damage from rpgdb where userID=?", (user.id,))

async def create_account(user):
    if rpgdata.execute("SELECT 1 FROM rpgdb WHERE userID = ?", (user.id,)).fetchone():
        return False
    else:
        rpgdata.execute("INSERT INTO rpgdb VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user.id, 100, 1, 100, 5, "sword", 1, 100, 20, 5, 5))   
        conn.commit()
    
   
bot.run(token)
