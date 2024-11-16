import discord
from discord import app_commands

import config

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(
    name="test",
    description="test",
)
async def test(interaction):
    await interaction.response.send_message("Pomme")


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


client.run(config.TOKEN)
