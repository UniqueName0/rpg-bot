import os
import discord
from discord.ext import commands, tasks

token = os.getenv('token')

helptext = open('help.txt', 'r').read()



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
