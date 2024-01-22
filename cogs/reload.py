import discord
from discord.ext import commands
import os

class BotManagement(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='reload', hidden=True)
    async def reload_bot(self, ctx):
        """Reload the bot"""
        try:
            for cog in os.listdir('./cogs'):
                if cog.endswith('.py'):
                    self.client.reload_extension(f'cogs.{cog[:-3]}')
            await ctx.send('Bot reloaded successfully!')
        except Exception as e:
            await ctx.send(f'Error reloading bot: {str(e)}')

def setup(client):
    client.add_cog(BotManagement(client))