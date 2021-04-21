import discord
from weird_bot import DiscordBot  # bot class
import requests
import json
from random import randint


# define constants
def define_constants():
    # return constants
    constants = {
        "not_allowed_words": ['blonde', 'arabe', 'juif', 'obèse'],  # "no_worlds" : not allowed worlds in jokes
        "derp emoji": '<:derp:822190112460767252>',
        'derp emojis': ['<:wow_derp:825451424107200573>', '<:wizard_derp:825425434044661830>',
                        '<:white_derp:825404599322017832>',
                        '<:termina_derp:825437326637400155>', '<:storm_hungry_derp:825404624579592213>',
                        '<:star_derp:825373824966721536>', '<:sad_derp:825419665110597643>',
                        '<:red_derp:823152144257515550>',
                        '<:old_derp:825430217404186665>', '<:love_derp:825380379514110033>',
                        '<:laughing_derp:826871192262541369>', '<:killer_derp:825423560553660437> ',
                        '<:ink_derp:826081060210344028>', '<:idiot_derp:825426870824337479> ',
                        '<:hungy_derp:825404566853648405>', '<:hungry_black_derp:825374191837904917> ',
                        '<:hugly_happy_derp:825419213661012019>', '<:happy_derp:825425791969132644> ',
                        '<:derp_gene:826117378411724810>', '<:derp:822190112460767252>',
                        '<:criing_derp:825419483899887646> ',
                        '<:chocked_derp:825419136925564948>', '<:bully_derp:825439375335751781>',
                        '<:brain_derp:825428421844140042>', '<:boring_derp:825419407668150272>',
                        '<:blue_derp:823152491948539904>', '<:black_derp:825370095865692242>'],
        "bot id": 834171699297386546
    }

    return constants


# get token, need file name
def get_token(key, file='tokens.json'):
    # open the file and read the token
    with open(file) as f:
        data = json.load(f)

    return data[key]  # return the token


# joke : get a random joke from an api, need api url and the not allowed worlds
async def send_a_joke(args_list__url_not_allowed_words, message):
    url = args_list__url_not_allowed_words[0]
    not_allowed_words = args_list__url_not_allowed_words[1]

    data = requests.get(url,
                        headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzE4N'
                                                  'zQzMjM5MTI1MTA2NzI4IiwibGltaXQiOjEwMCwia2V5IjoiVEh6S1IyQUFRZlpGV2'
                                                  'ZCWXZYOTFHWGRGSnVCMGtwSktiTHBoSlo3TmJzb0xBMVJwT0YiLCJjcmVhdGVkX2F'
                                                  '0IjoiMjAyMS0wMy0yMVQxNTowNDoxOCswMDowMCIsImlhdCI6MTYxNjMzOTA1OH0.'
                                                  '0Tbo7AcZniPDHHt3tI9ynIDUbWAY7HH7XSn_p4dJGM8'})
    joke = json.loads(data.text)
    ok = True

    for element in joke:

        for word in not_allowed_words:

            if word in str(joke[element]):
                ok = False

    if ok:

        embed = discord.Embed(
            title=joke["joke"],
            description=f'||*{joke["answer"]}* ||',
            colour=discord.Color.random()
        )

        await message.channel.send(embed=embed)

    else:

        await send_a_joke(args_list__url_not_allowed_words, message)


async def send_a_derp(args_list__emojis_botid, message):
    if not message.author.id == args_list__emojis_botid[1]:
        await message.channel.send(args_list__emojis_botid[0][randint(0, len(args_list__emojis_botid[0]) - 1)])


# set the key words, key messages, and command
def set_worlds_messages_commands(bot, constants):
    # set key words in a dict : {'variable name' : (function, [arg one, arg two, etc])}
    bot.set_world_in_messages({
        # 'blague' call joke([url, not allowed words])
        'blagu': (send_a_joke, ['https://www.blagues-api.fr/api/random', constants['not_allowed_words']]),
        constants['derp emoji']: (send_a_derp, [constants['derp emojis'], constants['bot id']])
    })


# set what append o the 'on ready' event, need bot
def is_ready(bot):
    @bot.event  # it's an event of the bot
    async def on_ready():
        # print in console : [name of the bot] ready
        print(f'{bot.user.display_name} ready')
        await bot.change_presence(activity=discord.Game('être bizare'))  # change status of the bot


# main function
def main():
    bot = DiscordBot()  # define bot

    is_ready(bot)  # call is ready

    constants = define_constants()  # define constants

    set_worlds_messages_commands(bot, constants)  # set key worlds, etc

    bot.update()  # update the bot

    print('starting bot...')  # just a print for say 'the script has starting'

    bot.run(get_token('weird_bot'))  # run the bot with the token


if __name__ == '__main__':
    main()  # call main function
