import discord
import os
import json
from discord.ext import commands


os.system('cls')
with open('config/config.json') as config:
    data = json.load(config)

intents = discord.Intents.default()
intents.message_content = True 

class StaciaBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.token = data["token"]
        super().__init__(command_prefix="/", intents=intents, *args, **kwargs)

client = StaciaBot(case_insensitive=True)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="กำลังคลั่งรัก"))
    print(f'Welcome, {client.user} is Ready')
if __name__ == "__main__":
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            client.load_extension(f'cogs.{file[:-3]}')
    client.run(client.token)
client.load_extension('cogs.bot_management')