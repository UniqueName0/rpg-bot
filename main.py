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
    em.add_field(name = "hp potions", value = rpgdata.execute("SELECT hp_potions FROM rpgdb WHERE userID = ?", (user.id,)).fetchone())
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
    hp2 = rpgdata.execute("select health from rpgdb where userID=?", (user.id,)).fetchone()
    hp1 = "".join(c for c in hp2 if  c.isdecimal())
    hp = hp1
    dmg = rpgdata.execute("select damage from rpgdb where userID=?", (user.id,)).fetchone()
    defense = rpgdata.execute("select armor from rpgdb where userID=?", (user.id,))
    dodge = rpgdata.execute("select evasion from rpgdb where userID=?",  (user.id,))
    enemyhp = 25*int(arg)
    enemydmg = 5*int(arg)
    enemystats = discord.Embed(title = "enemy", color = discord.Color.red())
    enemystats.add_field(name = f"health: {enemyhp}", value = f"damage: {enemydmg}")
    await ctx.send(embed = enemystats)
    userstats = discord.Embed(title = user.name, color = discord.Color.red())
    userstats.add_field(name = f"health: {hp}", value = f"damage: {dmg}")
    await ctx.send(embed = userstats)
    #check = reaction_check(message=msg, author=ctx.author, emoji=(emoji1, emoji2))
    #try: 
     #   reaction, user = await self.client.wait_for('reaction_add', timeout=10.0, check=check)
      #  if reaction.emoji == emoji1:
       # 
        #elif reaction.emoji == emoji2:
        
    #except TimeoutError:
    
async def create_account(user):
    if rpgdata.execute("SELECT 1 FROM rpgdb WHERE userID = ?", (user.id,)).fetchone():
        return False
    else:
        rpgdata.execute("INSERT INTO rpgdb VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user.id, 100, 1, 100, 5, "sword", 1, 100, 20, 5, 5))   
        conn.commit()
    
   
bot.run(token)
