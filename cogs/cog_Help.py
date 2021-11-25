import discord

from typing import Optional, Set
from discord.ext import commands
from discord import Embed
from discord.ext.commands.core import Group


class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return f"!{command.qualified_name}{command.signature}"

    async def _help_embed(self, title: str, description: Optional[str] = None, mapping: Optional[str] = None, command_set: Optional[Set[commands.Command]] = None):
        embed = Embed(title=title)
        if description:
            embed.description = description
        if command_set:
            filtered = await self.filter_commands(command_set, sort = True)
            for command in filtered:
                embed.add_field(
                    name = self.get_command_signature(command), 
                    value = command.help or "...", 
                    inline = False
                )
        elif mapping:
            for cog, command_set in mapping.items():
                filtered = await self.filter_commands(command_set, sort = True)
                if not filtered:
                    continue
                name = cog.qualified_name if cog else "Pas de catégorie"
                cmd_list = "\n".join(
                    f"`{self.context.prefix}{cmd.name}`" for cmd in filtered
                )
                value = (
                    f"{cmd_list}"
                )
                embed.add_field(name=name, value=value)

        return embed

    async def send_bot_help(self, mapping: dict):
        embed = await self._help_embed(
            title = "Commandes du Bot",
            description = self.context.bot.description,
            mapping = mapping
        )
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command: commands.Command):
        embed = await self._help_embed(
            title = command.qualified_name,
            description = command.help,
            command_set = command.commands if isinstance(command, commands.Group) else None
        )
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog):
        embed = await self._help_embed(
            title = cog.qualified_name,
            description = cog.description,
            command_set = cog.get_commands()
        )
        await self.get_destination().send(embed=embed)

    send_group_help = send_command_help



class Help(commands.Cog, name ="Help"):
    """Affiche des informations concernant les commandes"""

    def __init__(self, bot):
        self.original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()

    def cog_unload(self):
        self.bot.help_command = self.original_help_command


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))
    