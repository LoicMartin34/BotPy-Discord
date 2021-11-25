import os
import sys

import discord
import asyncio
import random
import json
import youtube_dl
import nacl

from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord import Intents
from dotenv import load_dotenv


intents = discord.Intents.default()
intents.members = True

load_dotenv(dotenv_path="config")

bot = commands.Bot(command_prefix="!", intents=intents.all())



def roikku(ctx):
    return ctx.message.author.id == 228825158603767808

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Cette commande n'existe pas!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Un ou des arguments sont manquants!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas la permission d'exécuter cette commande!")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Le bot n'a pas la permission nécessaire pour exécuter cette commande!")

@bot.event
async def on_ready():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
    print("Le bot est connecté au serveur!")


@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(909492384251908099)
    await channel.send(f"Bienvenue sur le serveur {member} !")

@bot.event
async def on_member_remove(member):
    channel = member.guild.get_channel(909492384251908099)
    await channel.send(f"{member} nous a malheureusement quitté !")


"""Commandes permettant de gérer les extensions"""

@bot.command()
@commands.check(roikku)
async def load(ctx, name = None):
    if name:
        bot.load_extension(f'cogs.{name}')

@bot.command()
@commands.check(roikku)
async def unload(ctx, name = None):
    if name:
        bot.unload_extension(f'cogs.{name}')

@bot.command()
@commands.check(roikku)
async def reload(ctx, name = None):
    if name:
        try:
            bot.reload_extension(f'cogs.{name}')
        except:
            bot.load_extension(f'cogs.{name}')



bot.run(os.getenv("TOKEN"))














"""@bot.event
async def on_message_edit(before, after):
    await before.channel.send(f"{before.author} a édité son message :\nAvant -> {before.content}\nAprès -> {after.content}")"""


"""@bot.command()
async def sondage(ctx):
    await ctx.send("Kick ce membre ?")"""



