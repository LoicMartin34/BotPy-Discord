import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Admin(bot))

class Admin(commands.Cog):
    """Liste des commandes admin"""
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(administrator = True)
    async def serverInfo(self, ctx):
        server = ctx.guild
        serverName = server.name
        numberTextChannels = len(server.text_channels)
        numberVoiceChannels = len(server.voice_channels)
        descriptionServer = server.description
        numberMember = server.member_count
        message = f"Le serveur {serverName} est composé de {numberMember} personne(s).\nLa description du serveur est {descriptionServer}\nLe serveur est composé de {numberTextChannels} salons textuels et {numberVoiceChannels} salons vocaux"
        await ctx.send(content=message)


    @commands.command()
    @commands.has_permissions(administrator = True)
    async def getInfo(self, ctx, info):
        server = ctx.guild
        if info == "memberCount":
            await ctx.send(server.member_count)
        elif info == "numberOfChannels":
            await ctx.send(len(server.text_channels) + len(server.voice_channels))
        elif info == "name":
            await ctx.send(server.name)
        else:
            await ctx.send("Mauvaise commande indiquée")


    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, number_of_messages:int):
        messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()
        for message in messages:
            await message.delete()



    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, user:discord.User, *, reason = "Aucune raison donnée"):
        await ctx.guild.ban(user, reason = reason)
        embedBan = discord.Embed(title = "**Banissement**", color = 0xf44336, url = "https://fr.wikipedia.org/wiki/Respect")
        embedBan.set_thumbnail(url = "https://emoji.gg/assets/emoji/3283-pepe-banned.png")
        embedBan.add_field(name = "Membre banni", value = user.name, inline = True)
        embedBan.add_field(name = "Banni par", value = ctx.author.name, inline = True)
        embedBan.add_field(name = "Raison", value = reason, inline = True)
        await ctx.send(embed = embedBan)
    


    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, user, *reason):
    #user sous la forme username#tag
        reason = " ".join(reason)
        username, tag = user.split('#')
        bannedUsers = await ctx.guild.bans()
        for userBan in bannedUsers:
            if userBan.user.name == username and userBan.user.discriminator == tag:
                await ctx.guild.unban(userBan.user, reason = reason)
                await ctx.send(f"{user} a été déban pour la raison suivante : {reason}")
                return 
        #L'utilisateur n'a pas été trouvé
        await ctx.send(f"{user} n'est pas dans la liste des bannis.")


    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def getBanList(self, ctx):
        banList = []
        bans = await ctx.guild.bans()
        for ban in bans:
            banList.append(ban.user.name+"#"+ban.user.discriminator)
        if len(banList) == 0:
            await ctx.send(content="Aucun membre n'est actuellement banni")
        else:
            await ctx.send("Voici la liste des membres bannis sur le serveur : ")
            await ctx.send(content="\n".join(banList))