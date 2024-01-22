import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class ForexCalculator(commands.Cog):
    def __init__(self, client):
        self.client = client
    @slash_command(guild_ids=[1151244211195228232,1061824781906870302], description="Calculate lot size")
    async def calculate_lot_size(
        self,
        ctx,
        balance: float,
        risk_percentage: float,
        stop_loss_distance: float,
    ):
        try:
            lot_size = (balance * (risk_percentage / 100)) / stop_loss_distance
            embed = discord.Embed(
                title="Forex Lot Size Calculator",
                color=0x0080ff,
            )
            embed.add_field(name="Balance", value=f"${balance:.2f}", inline=False)
            embed.add_field(name="Risk Percentage", value=f"{risk_percentage}%", inline=False)
            embed.add_field(name="Stop Loss Distance", value=f"{stop_loss_distance} pips", inline=False)
            embed.add_field(name="Lot Size", value=f"{lot_size:.2f}", inline=False)
            await ctx.respond(embed=embed)
        except ZeroDivisionError:
            await ctx.respond("Stop loss distance cannot be zero.")
def setup(client):
    client.add_cog(ForexCalculator(client))
