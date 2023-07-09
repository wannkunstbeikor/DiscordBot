import discord
from discord.ext import commands
import re
import os
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

forums = []

checks = []


@bot.tree.command(name="setup")
async def setup(interaction: discord.Interaction, forum: discord.ForumChannel):
    forums.append(forum.id)
    await interaction.response.send_message(f"Setup of {forum} completed", ephemeral=True)


@bot.tree.command(name="add")
async def add(interaction: discord.Interaction, expression: str):
    checks.append(expression)
    await interaction.response.send_message(f"Added regex \"{expression}\"", ephemeral=True)


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


def check_message(message: str):
    for check in checks:
        if re.fullmatch(check, message):
            return True

    return False


@bot.event
async def on_thread_create(thread: discord.Thread):
    if thread.parent_id in forums:
        mes = await thread.fetch_message(thread.id)
        print(mes.content)
        if check_message(mes.content):
            print(f"{thread} is going to be deleted")
            await thread.delete()
            await mes.author.send("Please read the readme and format your message correctly!")

load_dotenv()
token = os.environ['TOKEN']
bot.run(token)
