from discord.ext import commands
from discord.commands import Option
import discord
from discord.ext.commands import Paginator

class getmember(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(f'Error: {error}')

    @commands.slash_command(
        name="listmembers",
        description="List all members in the server",
        guild_ids=[1061824781906870302]
    )
    async def list_members(self, ctx):
        try:
            # Get all members in the server
            members = ctx.guild.members

            # Paginate the list
            paginator = Paginator(prefix='', suffix='')
            for member in members:
                paginator.add_line(f"{member.name} ({member.id})")

            # Send paginated content
            for page in paginator.pages:
                await ctx.send(f"Members in the server:\n{page}")

        except (discord.DiscordException, discord.HTTPException) as e:
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred: {e}",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(getmember(bot))