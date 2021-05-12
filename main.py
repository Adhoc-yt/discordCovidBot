import random
import re
import discord
from datetime import datetime
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="%", intents=intents)
transmission_rate = .87

# TODO: ajouter les rôles Covided et Dr Raoult sur des nouveaux serveur
# Fonction infection_passive, qui infecte les membres côte à côte dans la liste alphabétique des users
# Fonction %geste_barrière, si invoquée le membre ne peux pas être infecté en postant son message
# Fonction %vaccin, divise par 10 les chances d'être infecté
# Fonction %stats, qui indique le nombre de personnes infectées sur l'ensemble du serveur, hors bot
# Si Covid, nickname suffixe peu glorieux (le raciste, le gros, le pédants, etc), une fois guéri on l'enlève
# Le rôle 5G permet d'utiliser la commande %5g @member et d'infecter cette personne


def risk_infection(message):
    role_covid = discord.utils.find(lambda r: r.name == 'Covided', message.guild.roles)
    return role_covid in message.guild.get_member(message.author.id).roles


@bot.event
async def on_ready() -> None:
    print("{} : Démarrage de bot".format(datetime.now()))


async def get_covid(message):
    role = discord.utils.get(message.author.guild.roles, name="Covided")
    await message.author.add_roles(role)
    await message.channel.send(f"{message.author.name} est maintenant {role.name}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Rupture de stock",
                           description=f"Oh non Docteur, nous n'avons plus de chloroquine!\n\
                                        Nous en aurons à nouveau dans {error.retry_after:.2f} secondes.")
        await ctx.send(embed=em)
        await ctx.send(error.args)


# Si Installateur 5G, peut installer une antenne 5G près d'un membre qui a une chance de refiler le covid
@bot.command(pass_context=True)
@commands.has_role('5G')
@commands.cooldown(2, 60, commands.BucketType.guild)
async def ondes5g(ctx, user_client: discord.Member):
    """
    Dose de 5G - Usage: %5G @member
    :return: null, a une chance d'infecter du Covid (parce que la 5G refile le coronavirus, c'est scientifique)
    """
    role_covid = discord.utils.find(lambda r: r.name == 'Covided', ctx.message.guild.roles)
    proba_covid = 0.70

    if role_covid in user_client.roles:
        await ctx.send(f"{user_client} a déjà la 5G.")
    elif random.random() <= proba_covid:
        await ctx.send("Le client a la 5G, et le covid.")
        await user_client.add_roles(role_covid)
    else:
        replies = [
            "Rien ne s'est produit, mais j'ai un meilleur réseau!",
            "L'antenne 5G est installée, mais personne n'est malade... Pour l'instant"
        ]
        await ctx.send(random.choice(replies))


# Si le membre a le covid, seul Dr Raoult peut utiliser la commande Chloroquine sur ce membre
# Cependant, la cholorquine a X% de chances de tuer le patient (kick serveur)
# Comme la chloroquine devient rare, Dr Raoult ne peut utiliser la choloroquine que 2 fois toutes les minutes
@bot.command(pass_context=True)
@commands.has_role('Dr Raoult le Fédérateur')
@commands.cooldown(2, 60, commands.BucketType.guild)
async def chloroquine(ctx, user_patient: discord.Member):
    """
    Dose de choloroquine - Usage: %chloroquine @member
    :return: null, a une chance de soigner du Covid ou de kick le membre
    """
    role_covid = discord.utils.find(lambda r: r.name == 'Covided', ctx.message.guild.roles)
    proba_kick = 0.05
    # Idée historique patient, injections ratées augmentent risque de mort
    proba_guerison = 0.70

    if role_covid in user_patient.roles:
        if random.random() <= proba_kick:
            await user_patient.send("Le Covid n'a pas eu raison de toi, mais le docteur, oui.\n\
Pour revenir: https://discord.gg/6QEvgHWnM3")
            await ctx.guild.kick(user_patient, reason="Chloroquined")
            await ctx.send(f"{user_patient} n'a pas survécu à sa dose de choloroquine!")
        elif random.random() <= proba_guerison:
            await user_patient.remove_roles(role_covid)
            await ctx.send(f"{user_patient.name} est guéri, merci Docteur!")
        else:
            await ctx.send("Le patient n'est pas guéri... Mais au moins, il n'est pas mort !")
    else:
        replies = [
            "Mais enfin Docteur, ce patient est sain",
            "Docteur, vous avez (encore) bu?",
            "Ce patient est guéri !... Mais n'était pas malade."
        ]
        await ctx.send(random.choice(replies))


@chloroquine.error  # <- name of the command + .error
async def help_mod_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Vous n'êtes pas Docteur, sale usurpateur ! Cassez-vous !")


@bot.command(pass_context=True)
async def pcr(ctx, user: discord.Member):
    """
    PCR test - Usage: %pcr @member
    :return: si le membre a le covid ou pas
    """
    role = discord.utils.find(lambda r: r.name == 'Covided', ctx.message.guild.roles)
    if role in user.roles:
        await ctx.send("{} a le Covid".format(user))
    else:
        await ctx.send("{} est sain".format(user))


@bot.event
async def on_message(message):
    # Besoin de cette ligne pour ne pas bloquer les bot.commands()
    await bot.process_commands(message)
    # Logging
    last_message = await message.channel.history(limit=2).flatten()
    last_message = last_message[1]
    print("{} répond à {} - {}".format(message.author, last_message.author, message.content.lower()))
    if message.author == bot.user:
        return

    # FONCTIONS BONUS
    if "covid" in message.content:
        await message.channel.send("On m'a appelé?")
    if "pied" in message.content or "feet" in message.content:
        await message.channel.send("Ah, ça parle de pied? <@!830199237856723004> est fétichiste!")
    if "éthique" in message.content:
        await message.channel.send("> L'éthique, c'est pour les pauvres.\n- <@!307964302533591050>")

    # détection cyrillique => cyka
    if re.search('[а-яА-Я]', message.content):
        await message.channel.send("сука блять")

    if ''.join(filter(str.isalpha, message.content.lower())).endswith("quoi") \
            and not message.content.lower().endswith(">"):
        await message.channel.send("FEUR!")

    if not message.author.bot and risk_infection(last_message):
        if risk_infection(message) or random.random() >= transmission_rate:
            return
        else:
            await get_covid(message)


if __name__ == '__main__':
    discord_key = open("key.txt", "r").read()
    bot.run(discord_key)
