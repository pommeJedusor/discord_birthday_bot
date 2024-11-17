import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import tasks
import datetime

if not os.path.exists("db"):
    os.makedirs("db")

from model.Birthday import Birthday


load_dotenv()
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("Please set a TOKEN")
    exit()

Birthday.init()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


current_date = (None, None)


async def send_birthday_notif(user: discord.User, name: str):
    await user.send(f"Today is the birthday of {name}")


@tasks.loop(minutes=5)
async def check_birthdays():
    global current_date

    today = datetime.datetime.today()
    if current_date == (today.day, today.month):
        return

    today_birthdays = Birthday.getByDateIfNotChecked(today.day, today.month)
    current_date = (today.day, today.month)

    while today_birthdays:
        birthday = today_birthdays.pop()
        user = client.get_user(birthday.user_id)
        if user is None:
            Birthday.delete(birthday.user_id, birthday.name)
        else:
            await send_birthday_notif(user, birthday.name)
            birthday.check()


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
        Birthday.save(interaction.user.id, name, day, month)
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
        if not Birthday.getByUserIdAndName(interaction.user.id, name):
            raise Exception("birthday not found")
        Birthday.delete(interaction.user.id, name)
    except Exception as e:
        message = f"an error as occured\n```\n{e}\n```"
    await interaction.response.send_message(message)


@tree.command(
    name="see_birthdays",
    description="See all the birthdays you inserted",
)
async def see_birthdays(interaction: discord.Interaction):
    message = f""
    try:
        birthdays = Birthday.getByUserId(interaction.user.id)
        for birthday in birthdays:
            message += f"{birthday.name}: {birthday.day}/{birthday.month}\n"
        message = message or "No birthday found, to insert one do `/add_birthday`"
    except Exception as e:
        message = f"an error as occured\n```\n{e}\n```"
    await interaction.response.send_message(message)


@client.event
async def on_ready():
    await tree.sync()
    check_birthdays.start()
    print("Ready!")


client.run(TOKEN)
