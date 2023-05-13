import discord
from discord.commands import Option
from discord.commands import slash_command
import os
from dotenv import load_dotenv
from discord.ext import commands, bridge
from datetime import datetime
import asyncio



manage_roles = True
intents = discord.Intents.default()
intents.members = True
intents.message_content = True


activity = discord.Activity(type=discord.ActivityType.watching, name="💻|Proplayer#3112")

bot = bridge.Bot(intents=intents ,
                  debug_guilds=[#Deine Server-ID],
                  activity=activity
                  )




if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")




load_dotenv()
bot.run(os.getenv("TOKEN"))



