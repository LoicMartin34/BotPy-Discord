import discord
from discord.ext import commands

import random
import json

def setup(bot):
    bot.add_cog(LoL(bot))

class LoL(commands.Cog):
    "Liste des commandes pour LoL"
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lolPicker(self, ctx, param=None, *args):
        """Test lol
        Example : lolPicker TOP
        """
        with open("json/LoLChampions.json") as f:
            data = json.load(f)
        with open("json/LoLChampionsByRoles.json") as f2:
            dataRoles = json.load(f2)

        try :
            action = int(param)
        except:
            action = param

        if action is None:
            selectID = random.randint(0,len(data)-1)
            selectName = data[selectID]["name"]
            selectRoles = data[selectID]["roles"]
            selectRole = ""
            if len(selectRoles) != 0:
                selectRole = selectRoles[random.randint(0, len(selectRoles)-1)]
                embedLolPicker = discord.Embed(color = 0xD79A10)
                embedLolPicker.set_author(name = "Lol Picker", icon_url = "https://i.pinimg.com/originals/b8/3e/6f/b83e6fea403a390bd06ae17c187408e3.png")
                embedLolPicker.add_field(name = "Règles", value = f"Tu dois jouer **{selectName}** avec le rôle **{selectRole.lower()}**")
                embedLolPicker.set_thumbnail(url = f"https://raw.githubusercontent.com/esports-bits/lol_images/master/role_lane_icons/{selectRole}.png")
                embedLolPicker.set_image(url = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{selectName}_0.jpg")
                await ctx.send(embed = embedLolPicker)
                
        elif isinstance(action, int) :
            if action == None or action <= 1 or action > 5:
                    await ctx.send("Merci d'indiquer un nombre valide de joueurs compris entre 2 et 5")
            else:
                players = []
                for x in args:
                    players.append(x)
                if len(players)!=action:
                    await ctx.send("Merci d'entrer la liste complète et correcte des joueurs.")
                else:
                    roles = ["TOP", "JUNGLE", "MIDDLE", "ADC", "SUPPORT"]
                    for i in range(action):
                        role = random.choice(roles)
                        champ = random.choice(dataRoles[role])
                        roles.remove(role)
                        dataRoles.pop(role)

                        for (k, val) in dataRoles.items():
                            if champ in dataRoles[k]:
                                dataRoles[k].remove(champ)

                        embedLolPicker = discord.Embed(color = 0xD79A10)
                        embedLolPicker.set_author(name = "Lol Picker", icon_url = "https://i.pinimg.com/originals/b8/3e/6f/b83e6fea403a390bd06ae17c187408e3.png")
                        embedLolPicker.add_field(name = "Règles", value = f"{players[i]} dois jouer **{champ}** avec le rôle **{role.lower()}**")
                        embedLolPicker.set_thumbnail(url = f"https://raw.githubusercontent.com/esports-bits/lol_images/master/role_lane_icons/{role}.png")
                        embedLolPicker.set_image(url = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champ}_0.jpg")
                        await ctx.send(embed = embedLolPicker)
                            

        
        elif isinstance(action, str) :
            if action not in ["TOP", "JUNGLE", "MIDDLE", "ADC", "SUPPORT"]:
                await ctx.send("Merci d'indiquer un role valide compris dans cette liste : TOP, JUNGLE, MIDDLE, ADC et SUPPORT")
            else:  
                champ = random.choice(dataRoles[action])
                embedLolPickerRole = discord.Embed(color = 0xD79A10)
                embedLolPickerRole.set_author(name = "Lol Picker", icon_url = "https://i.pinimg.com/originals/b8/3e/6f/b83e6fea403a390bd06ae17c187408e3.png")
                embedLolPickerRole.add_field(name = "Règles", value = f"Tu dois jouer **{champ}** avec le rôle **{action.lower()}**")
                embedLolPickerRole.set_thumbnail(url = f"https://raw.githubusercontent.com/esports-bits/lol_images/master/role_lane_icons/{action}.png")
                embedLolPickerRole.set_image(url = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champ}_0.jpg")
                await ctx.send(embed = embedLolPickerRole)
