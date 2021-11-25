import discord
from discord.ext import commands

import random
import asyncio

def setup(bot):
    bot.add_cog(cogCommands(bot))

class cogCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    global mutePeople
    mutePeople = []
    global deafPeople
    deafPeople = []

    def listMembersVocal(self, ctx):
        channel = ctx.author.voice.channel
        members = []
        for member in channel.members:
            members.append(member)
        """print(members)
        print("-")"""
        return members


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """print("a")
        print(mutePeople)
        print("b")
        print(deafPeople)"""
        if before.channel is None and after.channel is not None:
            if member not in mutePeople:
                if after.mute == True:
                    await member.edit(mute=False)
            if member not in deafPeople:
                if after.deaf == True:
                    await member.edit(deafen=False)


    @commands.command()
    async def coucou(self, ctx):
        print("coucou")
        await ctx.send(content="Coucou toi!")

    @commands.command()
    async def say(self, ctx, *texte):
        await ctx.send(" ".join(texte))


    @commands.command()
    @commands.has_guild_permissions(mute_members = True)
    async def mute(self, ctx, member : discord.Member, mute_time=0):
        if mute_time < 0:
            await ctx.send("Merci d'indiquer une valeur positive.")
        elif mute_time == 0:
            await member.edit(mute=True)
            if member not in mutePeople:
                mutePeople.append(member)
        else:
            if member not in mutePeople:
                await member.edit(mute=True)
                await asyncio.sleep(mute_time)
                await member.edit(mute=False)

    @commands.command()
    @commands.has_guild_permissions(mute_members = True)
    async def unmute(self, ctx, member : discord.Member):
        mutePeople.remove(member)
        await member.edit(mute=False)

    @commands.command()
    @commands.has_guild_permissions(mute_members = True)
    async def allmute(self, ctx):
        vc = ctx.author.voice.channel
        #print(ctx.author)
        for member in vc.members:
            if member != ctx.author:
                await member.edit(mute=True)

    @commands.command()
    @commands.has_guild_permissions(mute_members = True)
    async def allunmute(self, ctx):
        vc = ctx.author.voice.channel
        for member in vc.members:
            await member.edit(mute=False)

    @commands.command()
    @commands.has_guild_permissions(deafen_members = True)
    async def deaf(self, ctx, member : discord.Member, deaf_time=0):
        if deaf_time < 0:
            await ctx.send("Merci d'indiquer une valeur positive.")
        elif deaf_time == 0:
            await member.edit(deafen=True)
            if member not in deafPeople:
                deafPeople.append(member)
        else:
            if member not in deafPeople:
                await member.edit(deafen=True)
                await asyncio.sleep(deaf_time)
                await member.edit(deafen=False)


    @commands.command()
    @commands.has_guild_permissions(deafen_members = True)
    async def undeaf(self, ctx, member : discord.Member):
        deafPeople.remove(member)
        await member.edit(deafen=False)



    @commands.command()
    @commands.has_permissions(move_members = True)
    async def kick(self, ctx, user:discord.User):
        #print(user.id)
        member = ctx.guild.get_member(user.id)
        #kick_channel = await ctx.guild.create_voice_channel("kick")
        await member.move_to(None)
        #await kick_channel.delete()


    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def randomKick(self, ctx):
        if ctx.author.voice is None:
            await ctx.send(f"Merci de rejoindre un salon vocal pour kick une personne aléatoire.")
        else:
            members = self.listMembersVocal(ctx)
            if len(members)<2:
                await ctx.send(f"Il est nécessaire d'être au moins deux personnes pour exécuter un random kick.")
            else:
                memberKick = random.choice(members)
                await memberKick.move_to(None)

    @commands.command()
    @commands.has_guild_permissions(kick_members = True)
    async def kickServer(self, ctx, user:discord.User, *reason):
        reason = " ".join(reason)
        await ctx.guild.kick(user, reason = reason)


    @commands.command()
    @commands.has_permissions(send_messages = True)
    @commands.cooldown(rate=1, per=30)
    async def roueDeLaFortune(self, ctx):
        embedRDF = discord.Embed(title = "**Roue de la fortune**", color = 0x88e684)
        embedRDF.set_thumbnail(url = "https://c.tenor.com/HGpVsyfgOgMAAAAC/wheel-of.gif")
        msgEmbed = await ctx.send(embed = embedRDF)
        if ctx.author.voice is None:
            embedRDF.description = "Merci de rejoindre un salon vocal pour lancer la roue."
            await msgEmbed.edit(embed = embedRDF)
        else:
            members = self.listMembersVocal(ctx)
            if len(members)<2:
                embedRDF.description = "Il est nécessaire d'être au moins deux personnes dans le vocal pour lancer la roue de la fortune."
                await msgEmbed.edit(embed = embedRDF)
                #await ctx.send(f"Il est nécessaire d'être au moins deux personnes dans le vocal pour lancer la roue de la fortune.")
            else:
                embedRDF.description = "La roue de la fortune va commencer!\n Ajouter la réaction ✅ pour y participer."
                await msgEmbed.edit(embed = embedRDF)
                #message = await ctx.send("La roue de la fortune va commencer. Ajouter la réaction ✅ pour y participer.")
                await msgEmbed.add_reaction("✅")

                players = []
                #print("membre du vocal : ")
                #print(members)
                def checkReaction(reaction, player):
                    #player != bot.user Pour l'instant le bot ne peut pas rejoindre de vocal, il ne sera donc jamais dans la liste des membres présents dans le channel 
                    if player in members:
                        #print(f"{player} dans le vocal!")
                        return msgEmbed.id == reaction.message.id and (str(reaction.emoji) == "✅")
                    else:
                        return
                        #print(f"{player} nest pas dans le vocal!")

                try:
                    while True:
                        reaction, player = await self.bot.wait_for("reaction_add", timeout = 10, check = checkReaction)
                        if len(players) == 0:
                            embedRDF.add_field(name = "Participants", value = player)
                            await msgEmbed.edit(embed = embedRDF)
                            players.append(player)

                        else:
                            if player not in players:
                                players.append(player)
                                stringPlayers = ""
                                for player in players:
                                    stringPlayers += player.name+"#"+player.discriminator+"\n"
                                embedRDF.set_field_at(index = 0, name = "Participants", value = stringPlayers)
                                await msgEmbed.edit(embed = embedRDF)

                        #await ctx.send(f"{player} nouveau participant!")
                        
                except:
                    print("Démarrage du tirage")
                """print("membre du jeu : ")
                print(players)"""
                rewards = ["kick", "randomKick", "mute", "deaf"]

                if len(players) >= 2:
                    #Affichage à retravailler pour le rendre ergonomique et sympa visuellement
                    embedRDF.add_field(name="Compteur", value = "La roue va être lancée dans 3", inline=False)
                    await msgEmbed.edit(embed = embedRDF)
                    #await ctx.send("La roue va être lancée dans 3")
                    await asyncio.sleep(1)
                    embedRDF.set_field_at(name="Compteur", index = 1, value = "La roue va être lancée dans 2", inline=False)
                    await msgEmbed.edit(embed = embedRDF)
                    #await ctx.send("2")
                    await asyncio.sleep(1)
                    embedRDF.set_field_at(name="Compteur", index = 1, value = "La roue va être lancée dans 1", inline=False)
                    await msgEmbed.edit(embed = embedRDF)
                    #await ctx.send("1")
                    await asyncio.sleep(1)
                    loser = random.choice(players)
                    reward = random.choice(rewards)
                    embedRDF.set_field_at(index = 1, name = "Récompense", value = f"{loser} a gagné un {reward}", inline=False)
                    await msgEmbed.edit(embed = embedRDF)
                    #await ctx.send(f"{loser} a gagné un {reward}")

                    #liste des possibilités
                    if reward == "kick":
                        await self.kick(ctx, loser)
                    elif reward == "randomKick":
                        await self.randomKick(ctx)
                    elif reward == "mute":
                        await self.mute(ctx, loser, 30)
                    elif reward == "deaf":
                        await self.deaf(ctx, loser, 15)

                else:
                    embedRDF.description = "La roue de la fortune est annulée par manque de participants !"
                    await msgEmbed.edit(embed = embedRDF)
                    #await ctx.send(f"La roue de la fortune est annulée par manque de participants!")