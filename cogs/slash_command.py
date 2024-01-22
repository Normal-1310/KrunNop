from discord.ext import commands
from discord.commands import Option
import discord

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user} ({self.bot.user.id})')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(f'Error: {error}')

    @commands.slash_command(
        name="addrole",
        description="Add a role to a member or everyone",
        guild_ids=[1061824781906870302]
    )
    async def add_role(
        self,
        ctx,
        member: Option(str, description="Select a member", required=True),
        role: Option(commands.RoleConverter, description="Select a role", required=True)
    ):
        try:
            # Check if the bot has the necessary permissions to add roles
            if not ctx.guild.me.guild_permissions.manage_roles:
                raise discord.errors.Forbidden("Bot lacks 'Manage Roles' permission.")

            if member.lower() == "@everyone":
                # Add the role to everyone in the server
                for server_member in ctx.guild.members:
                    await server_member.add_roles(role)
                embed = discord.Embed(
                    title="Role Added",
                    description=f"Role {role.name} added to everyone",
                    color=discord.Color.blue()
                )
            else:
                # Add the role to the specified member
                member_obj = await commands.MemberConverter().convert(ctx, member)
                await member_obj.add_roles(role)
                embed = discord.Embed(
                    title="Role Added",
                    description=f"Role {role.name} added to {member_obj.mention}",
                    color=discord.Color.blue()
                )
        except discord.errors.Forbidden as e:
            embed = discord.Embed(
                title="Error",
                description=f"I don't have the necessary permissions to add that role: {e}",
                color=discord.Color.red()
            )
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred: {e}",
                color=discord.Color.red()
            )
        finally:
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(SlashCommands(bot))
