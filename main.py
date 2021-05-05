import discord
from datetime import datetime
from discord.ext import commands

bot = commands.Bot(command_prefix="//")


@bot.event
async def on_ready() -> None:
    print("{} : Démarrage de bot".format(datetime.now()))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('ping'):
        await message.channel.send('Pong!')

    if "covid" in message.content:
        await message.channel.send("On m'a appelé?")

    if message.content.endswith("quoi"):
        await message.channel.send("FEUR!")


if __name__ == '__main__':
    discord_key = open("key.txt", "r").read()
    bot.run(discord_key)
