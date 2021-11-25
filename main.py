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


#import cog_Admin
#import cog_LoL
#import cog_Commands
#import cog_Musics

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
    print("Le bot est connecté au serveur!")
    bot.load_extension("cog_Admin")
    bot.load_extension("cog_Commands")
    bot.load_extension("cog_LoL")
    bot.load_extension("cog_Musics")

@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(909492384251908099)
    await channel.send(f"Bienvenue sur le serveur {member} !")

@bot.event
async def on_member_remove(member):
    channel = member.guild.get_channel(909492384251908099)
    await channel.send(f"{member} nous a malheureusement quitté !")




"""@bot.event
async def on_message_edit(before, after):
    await before.channel.send(f"{before.author} a édité son message :\nAvant -> {before.content}\nAprès -> {after.content}")"""





"""@bot.command()
async def sondage(ctx):
    await ctx.send("Kick ce membre ?")

    def checkMessage(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel

    try:
        answer = await bot.wait_for("message", timeout=10, check=checkMessage)
    except:
        return
    await ctx.send(f"La réponse est {answer.content}")
    message = await ctx.send("Le vote va commencer!")
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def checkReaction(reaction, user):
        return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout = 10, check = checkReaction)
        if reaction.emoji == "✅":
            await ctx.send("Le membre est kick!")
        else:
            await ctx.send("Le membre n'est pas kick!")
    except:
        await ctx.send("Le sondage n'a pas été effectué")
"""


"""Commandes permettant de gérer les extensions"""

@bot.command()
@commands.check(roikku)
async def load(ctx, name = None):
    if name:
        bot.load_extension(name)

@bot.command()
@commands.check(roikku)
async def unload(ctx, name = None):
    if name:
        bot.unload_extension(name)

@bot.command()
@commands.check(roikku)
async def reload(ctx, name = None):
    if name:
        try:
            bot.reload_extension(name)
        except:
            bot.load_extension(name)

    
#bot.add_cog(cog_Admin.cogAdmin(bot))
#bot.add_cog(cog_LoL.cogLoL(bot))
#bot.add_cog(cog_Commands.cogCommands(bot))

bot.run(os.getenv("TOKEN"))



