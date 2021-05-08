import random
import re
import discord
from datetime import datetime
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="%", intents=intents)
transmission_rate = .5


def risk_infection(message):
    role = discord.utils.find(lambda r: r.name == 'Covided', message.guild.roles)
    return role in message.guild.get_member(message.author.id).roles


@bot.event
async def on_ready() -> None:
    print("{} : Démarrage de bot".format(datetime.now()))


@bot.command()
async def get_covid(message):
    role = discord.utils.get(message.author.guild.roles, name="Covided")
    await message.author.add_roles(role)
    await message.channel.send(f"{message.author.name} est maintenant {role.name}")


@bot.command(pass_context=True)
async def pcr(ctx, user: discord.Member):
    """
    PCR test - Usage: %pcr @member
    :return: if member has covid or not
    """
    role = discord.utils.find(lambda r: r.name == 'Covided', ctx.message.guild.roles)
    if role in user.roles:
        await ctx.send("{} a le Covid".format(user))
    else:
        await ctx.send("{} est sain".format(user))


@bot.event
async def on_message(message):
    # We need this line to allow usage of bot.commands()
    await bot.process_commands(message)

    # FONCTIONS BONUS
    if "covid" in message.content:
        await message.channel.send("On m'a appelé?")

    # détection cyrillique => cyka
    if re.search('[а-яА-Я]', message.content):
        await message.channel.send("сука блять")

    if ''.join(filter(str.isalpha, message.content.lower())).endswith("quoi") \
            and not message.content.lower().endswith(">"):
        await message.channel.send("FEUR!")

    # Logging
    last_message = await message.channel.history(limit=2).flatten()
    last_message = last_message[1]
    print("{} répond à {} - {}".format(message.author, last_message.author, message.content.lower()))

    if message.author == bot.user:
        return

    if risk_infection(last_message):
        if risk_infection(message) or random.random() > transmission_rate:
            return
        else:
            await get_covid(message)


if __name__ == '__main__':
    discord_key = open("key.txt", "r").read()
    bot.run(discord_key)
