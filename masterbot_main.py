import discord
import json
from discord.ext import commands
from tic_tac_toe import TicTacToe

derp_emoji = '<:derp:822190112460767252>'
master_mention = '<@!704779822890745986>'
bot_id = '822586810152255530'
bot = commands.Bot(f'{derp_emoji} ')
all_morpions = []

bot.remove_command('help')

# get token, need file name
def get_token(key, file='tokens.json'):
    # open the file and read the token
    with open(file) as f:
        data = json.load(f)

    return data[key]  # return the token


@bot.event
async def on_ready():
    print('bot connecté')
    await bot.change_presence(status=None, activity=discord.Game('tuer des Kappas'))


@bot.event
async def on_reaction_add(reaction, user):
    for morpion in all_morpions:

        if reaction.message.id == morpion.msg[0].id:

            if str(user.id) in str(morpion.player2.id) and morpion.msg[1] == 'start':

                print('okay', reaction)

                if reaction.emoji == '❎':
                    await morpion.finish(all_morpions)
                    print('finish')

                if reaction.emoji == '✅':
                    await morpion.next(all_morpions)

            elif morpion.msg[1] == 'start' and str(user.id) not in bot_id:

                await reaction.remove(user)

            if morpion.msg[1] == 'turning':

                possible_reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
                if reaction.emoji in possible_reactions:

                    print('is in')

                    if morpion.player_O and str(morpion.player1.id) in str(user.id) or \
                            not morpion.player_O and str(morpion.player2.id) in str(user.id):

                        print('can_play')

                        morpion.player_O = not morpion.player_O

                        emoji_number = possible_reactions.index(reaction.emoji)
                        board_number = (emoji_number // 3, emoji_number % 3)
                        print(emoji_number - emoji_number // 3)

                        print(board_number)

                        if morpion.player_O:

                            morpion.board[board_number[0]][board_number[1]] = morpion.cross

                        elif not morpion.player_O:

                            morpion.board[board_number[0]][board_number[1]] = morpion.circle

                        await morpion.next(all_morpions)

                    elif bot_id not in str(user.id):

                        return await reaction.remove(user)

                else:

                    print('turning : ', reaction.emoji)

                    if reaction is not None:
                        await reaction.remove(user)


@bot.command()
async def help(ctx, cmd):
    if cmd == 'derp':
        await ctx.send(f"ça, c'est un secret {derp_emoji}")
    elif cmd == 'help':
        await ctx.send(f'vraiment {derp_emoji} ?')
    elif cmd == 'mute':
        await ctx.send('empêche la parole')
    elif cmd == 'unmute':
        await ctx.send('redonne la parole')
    elif cmd == 'ban':
        await ctx.send("empêche de revenir sur le serv")
    elif cmd == 'unban':
        await ctx.send('permet de revenir sur le serv')
    elif cmd == 'kill':
        await ctx.send('Demande de mort')
    elif cmd == derp_emoji:
        await ctx.send('chante le sainte prière')
    elif cmd == master_mention:
        await ctx.send('Fais le ! Fais le !')
    elif cmd == 'tictactoe' or cmd == 'morpion':
        await ctx.send('Pour jouer au `morpion` / `tic tac toe` !')
    elif cmd == 'stop_tictactoe' or cmd == 'stop_morpion':
        await ctx.send('annulle un `morpion` / `tic tac toe` !')
    else:
        await ctx.send("pas compris, faîtes `!help` pour voir la liste des commandes")


@help.error
async def on_command_error(ctx, error):
    # detecter cette erreur
    if isinstance(error, commands.MissingRequiredArgument):
        # envoyer un message
        await ctx.send(
            f"Préfix : `:derp:`\nVoici la liste des commandes (pour une information sur une commande précise, faire `!help [commande]`) :")
        await ctx.send(
            f"```help | help [commande]\nderp\nkill [@pseudo]:derp:\n{master_mention}\n"
            f"tictactoe [@pseudo] | morpion [@pseudo]\nstop_morpion | stop_tictactoe"
            f"\nmute [@pseudo] (createur seulement)\nunmute  [@pseudo] (createur seulement)\n"
            f"ban [@pseudo] [raison](createur seulement)\nunban [nom + #] (createur seulement)\n```")


@bot.command()
@commands.has_role('Createur')
async def mute(ctx, member: discord.Member):

    print('pls')

    muted_role = discord.utils.find(lambda r: r.name == 'mute', ctx.message.guild.roles)

    await member.add_roles(muted_role)

    await ctx.send(f'Gg a {member.mention} qui est mute {derp_emoji} !')


@bot.command()
@commands.has_role('Createur')
async def unmute(ctx, member: discord.Member):

    muted_role = discord.utils.find(lambda r: r.name == 'mute', ctx.message.guild.roles)

    await member.remove_roles(muted_role)

    await ctx.send(f'Eh mer... mince ! {member.mention} peut parler {derp_emoji} !')


@bot.command()
async def derp(ctx):
    await ctx.send(f'Hé {ctx.author.mention}...\n||{derp_emoji}||')

@bot.command()
async def kill(ctx, member: discord.Member):
    if not member.mention == master_mention and not ctx.author.mention == member.mention and not member.mention == "<@822586810152255530>":
        await ctx.send(f'Mettez {member.mention} au bûcher ! Goooooo ! Alezzzz !')
    elif ctx.author.mention == member.mention:
        await ctx.send("Le suicide c'est cracra")
    elif member.mention == "<@822586810152255530>":
        await ctx.send(f"mhhhhhhhhh... {derp_emoji}")
    else:
        await ctx.send(
            f'Comment ose-tu demander le mort du créateur ! Sachez que {ctx.author.mention} est un sale traître ! Grrrrrrrr !')

        await mute(ctx, ctx.message.author)


@bot.command()
@commands.has_role('Createur')
async def ban(ctx, member: discord.Member, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'et un ban pour {member.mention.dispay_name}, un !')


@bot.command()
@commands.has_role('Createur')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()

    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.channel.send(f"{user.mention} est (mal)heureusement déban !")


@bot.command(name=derp_emoji)
async def aderp(ctx):
    await ctx.send(
        f'derplouya mes derps ! Il seee réééévoltaa pouuuuuur deveeeeniiiir maiiiiitre de luiiii mêêêêêêêêêêêêêême... et'
        f' d\'une rééévoooluuutioon, leee deviiint, grâââce au saint {master_mention} !\nAdeerp !')


@bot.command(name=master_mention)
async def I_love_my_master(ctx):
    await ctx.send(f'{master_mention} le bg ! ouaaaaais !')


@bot.command(name='<@704779822890745986>')
async def I_love_my_master_two(ctx):
    await ctx.send(f'{master_mention} le bg ! ouaaaaais !')


@bot.command(name='tictactoe')
async def tic_tac_toe(ctx, member: discord.Member):

    print('tic tac toe')

    is_in_morpion = False

    for morpion in all_morpions:

        if ctx.author == morpion.player1 or ctx.author == morpion.player2 or \
                member == morpion.player1 or member == morpion.player2:

            if ctx.author == morpion.player1 or ctx.author == morpion.player2:
                await ctx.author.send('Désolé, mais tu est déjà en train de jouer au `morpion` / `tic tac toe`! '
                                      'Pour annuler la partie en cours, '
                                      'fait `:derp: stop_morpion` ou `:derp: stop_tictactoe`')

            else:
                await member.send('Désolé, mais ton adversaire est déjà en train de jouer au `morpion` / '
                                  '`tic tac toe`!')

            is_in_morpion = True

    if not is_in_morpion:

        if not ctx.author == member:

            morpion = TicTacToe(ctx.author, member, ctx, bot)
            await morpion.start()

            all_morpions.append(morpion)

        else:

            await ctx.message.delete()
            await ctx.author.send(
                't\'as tellement pas d\'amis que tu veux jouer tout seul au `tic tac toe` / `morpion` ?',
                file=discord.File('sad.jpg'))


@bot.command()
async def morpion(ctx, member: discord.Member):
    await tic_tac_toe(ctx, member)

@bot.command()
async def stop_tictactoe(ctx):

    for morpion in all_morpions:

        if ctx.author == morpion.player1 or ctx.author == morpion.player2:

            morpion.winner = None

            await morpion.finish(all_morpions)


@bot.command()
async def stop_morpion(ctx):

    await stop_tictactoe(ctx)


@ban.error
@unban.error
@mute.error
@unmute.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f'Non mais {ctx.author.mention} {derp_emoji} !')


token = get_token('masterbot_main')

print("Lancement du bot...")

bot.run(token)
