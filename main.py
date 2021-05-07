import re
import discord
from datetime import datetime
from discord.ext import commands

bot = commands.Bot(command_prefix="//")


@bot.event
async def on_ready() -> None:
    print("{} : Démarrage de bot".format(datetime.now()))


@bot.command()
async def get_covid(message):
    role = discord.utils.get(message.author.guild.roles, name="Covided")
    await message.author.add_roles(role)
    await message.channel.send(f"Hey @Covided, {message.author.name} est maintenant {role.name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "pangolin" in message.content:
        await get_covid(message)

    # FONCTIONS BONUS
    if "covid" in message.content:
        await message.channel.send("On m'a appelé?")

    # détection cyrillique => cyka
    if re.search('[а-яА-Я]', message.content):
        await message.channel.send("сука блять")

    if ''.join(filter(str.isalpha, message.content.lower())).endswith("quoi") \
            and not message.content.lower().endswith(">"):
        print("{} - ".format(message.content.lower()))
        await message.channel.send("FEUR!")


if __name__ == '__main__':
    discord_key = open("key.txt", "r").read()
    bot.run(discord_key)
