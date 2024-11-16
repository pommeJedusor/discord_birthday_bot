import discord
from discord import app_commands

import config
from model.Birthday import Birthday

Birthday.init()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


async def send_birthday_notif(user: discord.User, name: str):
    await user.send(f"Today is the birthday of {name}")


@tree.command(
    name="add_birthday",
    description="add a birthday to be notified of",
)
async def add_birthday(
    interaction: discord.Interaction, day: int, month: int, name: str
):
    message = (
        f"The insertion of\n```\nname: {name}\ndate: {day}/{month}\n```has succeeded\n"
    )
    try:
        pass
    except Exception as e:
        message = f"an error as occured\n```\n{e}\n```"
    await interaction.response.send_message(message)


@tree.command(
    name="remove_birthday",
    description="remove a birthday to be notified of",
)
async def remove_birthday(interaction: discord.Interaction, name: str):
    message = f"The removal of the birthday of {name} has succeeded"
    try:
        pass
    except Exception as e:
        message = f"an error as occured\n```\n{e}\n```"
    await interaction.response.send_message(message)


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


client.run(config.TOKEN)
