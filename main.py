import random
import re
import discord
from datetime import datetime
from discord.ext import commands

# Config bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="%", intents=intents)
transmission_rate = .69
role_covid_name = 'Covided'
role_dr_name = 'Docteur-Marabout chloroquine'
role_5g_name = 'Technicien Orange'
role_masque_name = 'Porte un masque'
suffixes_peu_glorieux = [" gilet jaune",
                         " malade",
                         " inutile",
                         " gras·se",
                         " gros·se",
                         " socialiste",
                         " terroriste",
                         " gauchiste",
                         " droitard·e",
                         " sous-être",
                         " contagieux·se",
                         " zoophile",
                         " sale",
                         " malpropre",
                         " boiteux·se",
                         " clandestin·e",
                         " migrant·e",
                         " parasite",
                         " le rat puant",
                         " pédant·e",
                         " suce-boules",
                         " l'ordure",
                         " cocu·e",
                         " puceau·lle",
                         " con·ne",
                         " idiot·e",
                         " fourbe",
                         " arabe",
                         " enfoiré·e",
                         " dingue",
                         " cinglé·e",
                         " l'invalide",
                         " consanguin·e",
                         " furry",
                         " casse-couilles",
                         " fan de pieds",
                         " mécréant·e",
                         " l'infidèle",
                         " la grosse cochonne",
                         " ramolo",
                         " la petite chienne ouaf ouaf"
                         " relou·e",
                         " soumis·e",
                         " bâtard·e",
                         " nul·le",
                         " faible",
                         " malhonnête",
                         " brise-burnes",
                         " clochard·e",
                         " l'abruti·e",
                         " pauvre",
                         " drogué·e",
                         " boulimique",
                         " anorexique",
                         " obsédé·e",
                         " gérontophile",
                         " l'ultra pervers·e",
                         " pleutre",
                         " l'impotent·e",
                         " la chienne frigide",
                         " à la tendance pédophile",
                         " l'angoissé·e",
                         " maniaco-dépressif·ve",
                         " schizophrène",
                         " l'obèse morbide",
                         " l'impuissant·e",
                         " la petite bite",
                         " la pute",
                         " le sac à foutre",
                         " la serpillère à sperme",
                         " avec un petit sac à main"
                         ]
dict_questions_reponses = {'quoi': 'feur',
                           'pk': 'fure',
                           'pq': 'feur',
                           'non': 'bril',
                           'oui': 'ghours',
                           'ouais': 'stern',
                           'hein': 'dien',
                           'un': 'dien',
                           'ain': 'dien',
                           'bon': 'jour',
                           'qui': 'quette',
                           'ki': 'wi',
                           'ky': 'quette',
                           'test': 'ticule',
                           'tests': 'ticule'
                           }
image_sibeth = discord.File('sibeth.png')
covid_channel = "covid-log"
# Probas
proba_perte_masque = 0.025
proba_guerison_chloroquine = 0.80
proba_guerison_solo = 0.05
proba_covid_5g = 0.70
proba_symptom = 0.40
proba_kick_chloroquine = 0.05
proba_fin_de_phrase = 0.10


# Fonction Usage et Help (erreur mauvais paramètres + description du jeu)
# Fonction infection_passive, qui infecte les membres côte à côte dans la liste alphabétique des users
# Fonction %geste_barrière, si invoquée le membre ne peut pas être infecté en postant son message
# Fonction %vaccin, divise par 10 les chances d'être infecté
# Fonction %stats, qui indique le nombre de personnes infectées sur l'ensemble du serveur, hors bot
# Fonction %masque qui permet de mettre un :masque:, a chaque une chance de le perdre, réduit le risque d'infection
# Autre idée si Covid, le membre est en slowmode car insuffisance respiratoire


@bot.command()
@commands.has_role('Admin')
async def setup(ctx):
    """
    %setup - Vérifie et installe les rôles nécessaires au bon fonctionnement du bot.
    Cette commande ne peut être utilisée que par les Admins (role Discord).
    """
    for role in [role_covid_name, role_dr_name, role_5g_name, role_masque_name]:
        if discord.utils.get(ctx.guild.roles, name=role):
            print(f"Role {role} exists")
        else:
            await ctx.guild.create_role(name=role, colour=discord.Colour(random.randint(0, 0xFFFFFF)))
            print(f"Role {role} created")


async def show_symptoms(message):
    role_covid = discord.utils.find(lambda r: r.name == role_covid_name, message.guild.roles)
    if role_covid in message.guild.get_member(message.author.id).roles \
            and random.random() <= proba_symptom:
        suffixe = random.choice(suffixes_peu_glorieux)
        await message.author.edit(nick=message.author.name + suffixe)
        print(f'Nickname changed: {message.author}')


async def self_heal(message):
    role_covid = discord.utils.find(lambda r: r.name == role_covid_name, message.guild.roles)
    if role_covid in message.guild.get_member(message.author.id).roles \
            and random.random() <= proba_guerison_solo:
        await message.guild.get_member(message.author.id).remove_roles(role_covid)
        await message.channel.send(f":medical_symbol: {message.author.mention} est guéri !")
        await message.guild.get_member(message.author.id).edit(nick='')


def risk_infection(message):
    role_covid = discord.utils.find(lambda r: r.name == role_covid_name, message.guild.roles)
    return role_covid in message.guild.get_member(message.author.id).roles


def porte_masque(message):
    role_masque = discord.utils.find(lambda r: r.name == role_masque_name, message.guild.roles)
    return role_masque in message.guild.get_member(message.author.id).roles


@bot.event
async def on_ready() -> None:
    print("{} : Démarrage du bot Covid".format(datetime.now()))


async def get_covid(message):
    if message.author.bot:
        return
    role = discord.utils.get(message.author.guild.roles, name=role_covid_name)
    await message.author.add_roles(role)
    await show_symptoms(message)

    channel = message.channel
    if covid_channel:
        channel = discord.utils.get(message.author.guild.text_channels, name=covid_channel)

    channel.send(f"{message.author.mention} est maintenant {role.name} "
                 f"- plus d'EXP <:exp:874179122430103592> tant que pas guéri")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        print("Erreur perms")

    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f":warning: Cooldown",
                           description=f"Retentez la commande dans {error.retry_after:.2f} secondes.")
        if ctx.command.qualified_name == "ondes5g":
            em = discord.Embed(title=f":warning: Alerte gilets Jaunes",
                               description=f":signal_strength: Oh non, les gilets jaunes bloquent le rond-point!\n\
Tu pourras installer une antenne 5G dans {error.retry_after:.2f} secondes.")
        elif ctx.command.qualified_name == "heal":
            em = discord.Embed(title=f":warning: Rupture de stock",
                               description=f":medical_symbol: Oh non Docteur, nous n'avons plus de chloroquine!\n\
Nous en aurons à nouveau dans {error.retry_after:.2f} secondes.")
        elif ctx.command.qualified_name == "masque":
            em = discord.Embed(title=f":warning: Rupture de stock",
                               description=f":mask: Oups, plus de masque!\n\
On a oublié d'en commander. Nous en aurons à nouveau dans {error.retry_after:.2f} secondes.")

        await ctx.send(embed=em)


# Si Installateur 5G, peut installer une antenne 5G près d'un membre qui a une chance de refiler le covid
@bot.command(aliases=['antenne5g', 'antenne5G', 'ondes5G', '5g', '5G'])
@commands.has_role(role_5g_name)
@commands.cooldown(1, 60, commands.BucketType.guild)
async def ondes5g(ctx, user_client: discord.Member):
    """
    Installe une antenne 5G près du membre - Usage: %5g @membre
    Alias commande: %antenne5g, %antenne5G, %ondes5g, %5g, %5G
    A une chance d'infecter le membre du Covid20 (parce que la 5G refile le coronavirus, c'est scientifique).
    Cette commande ne peut être utilisée que par les Techniciens Orange (role Discord).
    Cette commande est soumise à un cooldown.
    """
    role_covid = discord.utils.find(lambda r: r.name == role_covid_name, ctx.message.guild.roles)
    if user_client.bot:
        return

    if role_covid in user_client.roles:
        await ctx.send(f":signal_strength: {user_client.name} a déjà la 5G.")
    elif random.random() <= proba_covid_5g:
        await ctx.send(f":signal_strength: {user_client.name} a la 5G, et le covid.")
        await user_client.add_roles(role_covid)
    else:
        replies = [
            ":signal_strength: Rien ne s'est produit, mais j'ai un meilleur réseau!",
            ":signal_strength: L'antenne 5G est installée, mais personne n'est malade... Pour l'instant"
        ]
        await ctx.send(random.choice(replies))


@ondes5g.error  # <- name of the command + .error
async def help_mod_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(":x: Encore un mec de Free qui se prend pour un Technicien Orange. Pas de 5G pour toi!")


# Si le membre a le covid, seul Dr Raoult peut utiliser la commande Chloroquine sur ce membre
# Cependant, la cholorquine a X% de chances de tuer le patient (kick serveur)
# Comme la chloroquine devient rare, Dr Raoult ne peut utiliser la choloroquine que 2 fois toutes les minutes
@bot.command(aliases=['chloroquine'])
@commands.has_role(role_dr_name)
@commands.cooldown(2, 60, commands.BucketType.guild)
async def heal(ctx, user_patient: discord.Member):
    """
    Injecte une dose de chloroquine au membre - Usage: %5g @membre
    Alias commande: %chloroquine
    A une chance de:
    - Kick le membre (mort du covid20) qui reçoit une invitation en MP pour rejoindre
    - Soigner le membre et enlever tout symptôme

    Cette commande ne peut être utilisée que par Docteur Raoult Le Fédérateur (role Discord).
    Cette commande est soumise à un cooldown.
    """
    role_covid = discord.utils.find(lambda r: r.name == role_covid_name, ctx.message.guild.roles)

    # Idée historique patient, injections ratées augmentent risque de mort
    if user_patient.bot:
        return

    if role_covid in user_patient.roles:
        if random.random() <= proba_kick_chloroquine:
            await user_patient.send(":skull: Le Covid n'a pas eu raison de toi, mais le docteur, oui.\n\
Pour revenir: https://discord.gg/85yShvhRgX")
            await ctx.guild.kick(user_patient, reason="Chloroquined")
            await ctx.send(f":skull: {user_patient.name} n'a pas survécu à sa dose de choloroquine!")
        elif random.random() <= proba_guerison_chloroquine:
            await user_patient.remove_roles(role_covid)
            await ctx.send(f":medical_symbol: {user_patient.name} est guéri, merci Docteur!")
            await user_patient.edit(nick='')
        else:
            await ctx.send(":medical_symbol: Le patient n'est pas guéri... Mais au moins, il n'est pas mort !")
    else:
        replies = [
            ":medical_symbol: Mais enfin Docteur, ce patient est sain",
            ":medical_symbol: Docteur, vous avez (encore) bu ?",
            ":medical_symbol: Ce patient est guéri !... Mais n'était pas malade."
        ]
        await ctx.send(random.choice(replies))


@heal.error  # <- name of the command + .error
async def help_mod_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(":x: Vous n'êtes pas Docteur, sale usurpateur ! Cassez-vous !")


@bot.command()
@commands.cooldown(5, 60, commands.BucketType.guild)
async def masque(ctx):
    """
    Met un masque
    Possibilité de perdre son masque à chaque message posté
    """
    role_masque = discord.utils.find(lambda r: r.name == role_masque_name, ctx.message.guild.roles)
    await ctx.message.author.add_roles(role_masque)
    if role_masque in ctx.guild.get_member(ctx.message.author.id).roles:
        replies_replacemask = [
            f":mask: {ctx.message.author.display_name} a remplacé son masque !",
            f":mask: {ctx.message.author.display_name} a changé son masque !",
            f":mask: {ctx.message.author.display_name} montre l'exemple, et change de masque."
        ]
        await ctx.send(random.choice(replies_replacemask))
    else:
        replies_putmask = [
            f":mask: {ctx.message.author.display_name} a mis un masque !",
            f":mask: {ctx.message.author.display_name} a enfin mis son masque !",
            f":mask: {ctx.message.author.display_name} montre l'exemple, et met un masque."
        ]
        await ctx.send(random.choice(replies_putmask))


@bot.command(aliases=['rt-pcr', 'test-anal'])
async def pcr(ctx, user: discord.Member):
    """
    PCR test - Usage: %pcr @member
    :return: si le membre a le covid ou pas
    """
    role = discord.utils.find(lambda r: r.name == role_covid_name, ctx.message.guild.roles)
    if role in user.roles:
        await ctx.send(":nauseated_face: {} a le Covid".format(user))
    else:
        await ctx.send(":white_check_mark: {} est sain".format(user))


@bot.event
async def on_message(message):
    # Besoin de cette ligne pour ne pas bloquer les bot.commands()
    await bot.process_commands(message)
    # Logging
    last_message = await message.channel.history(limit=2).flatten()
    last_message = last_message[1]
    message.content = message.content.lower()

    if message.author.bot:
        print("Ignored bot {} saying: {}".format(message.author, message.content))
        return  # ignore bot messages

    await self_heal(message)
    await show_symptoms(message)

    print("{} répond à {} - {}".format(message.author, last_message.author, message.content))
    gestes_barrieres = ["%geste_barrière", "%geste_barriere", "%gestes_barrieres" "%gestes_barrières"]
    if any(geste_barriere in message.content for geste_barriere in gestes_barrieres):
        return

    if porte_masque(message):
        role_masque = discord.utils.find(lambda r: r.name == role_masque_name, message.guild.roles)
        reponses_perte_masque = ["n'a plus de masque",
                                 "a perdu son masque",
                                 "a fait tomber son masque"]
        if random.random() <= proba_perte_masque:
            await message.author.remove_roles(role_masque)
            if message.content == "%masque":
                await message.channel.send(f"... Mais il est tombé :upside_down:\n\
Bah alors {message.author.display_name}, on ne sait pas mettre un masque?")
                await message.channel.send(file=image_sibeth)
            else:
                await message.channel.send(f"{message.author.display_name} {random.choice(reponses_perte_masque)}")
            return

    # FONCTIONS BONUS
    if "covid" in message.content:
        replies_covid = [
            "On m'a appelé ?",
            "Qui me parle ?",
            "Plaît-il ?",
            "Comment ça 'covid' ?",
            "Oui(stiti) ?",
            "Quoi, encore ?",
            '*blushes*',
            "Je suis une sacrée starlette."
        ]
        await message.channel.send(random.choice(replies_covid))
        return

    # détection cyrillique => cyka
    if re.search('[а-яА-Я]', message.content):
        insultes_russes = ["сука блять",
                           "иди нахуй",
                           "мудак",
                           "Пёс ёб твою мать",
                           "Меня это заебало",
                           "заткнись"
                           ]
        await message.channel.send(random.choice(insultes_russes))
        return

    # fins de phrases remarquables
    if not message.content.endswith(">") and random.random() <= proba_fin_de_phrase:
        filtered_message = ''.join(filter(str.isalpha, message.content))
        for fin_de_phrase in dict_questions_reponses:
            if filtered_message.endswith(fin_de_phrase):
                await message.channel.send(dict_questions_reponses[fin_de_phrase].upper() + "!")
                return

    if not message.author.bot and risk_infection(last_message):
        if risk_infection(message) or random.random() <= transmission_rate:
            return
        else:
            await get_covid(message)
            return


if __name__ == '__main__':
    discord_key = open("key.txt", "r").read()
    bot.run(discord_key)
