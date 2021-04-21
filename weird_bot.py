import discord


class DiscordBot(discord.Client):

    def __init__(self):
        super().__init__()

        self.commands = []  # commands
        self.messages = []  # key messages
        self.worlds_in_messages = []  # key worlds

    # for the three, all is in the function name
    def set_commands(self, commands):
        self.commands = commands

    def set_world_in_messages(self, worlds):
        self.worlds_in_messages = worlds

    def set_messages(self, messages):
        self.worlds_in_messages = messages

    # update function
    def update(self):

        # call the key words for optimization
        worlds_in_messages = self.worlds_in_messages

        @self.event
        async def on_message(message):

            muted_role = discord.utils.find(lambda r: r.name == 'mute', message.guild.roles)

            if muted_role in message.author.roles:

                await message.delete()

            else:

                for world in worlds_in_messages:

                    if world in message.content.lower():  # if the word is in message

                        await worlds_in_messages[world][0](worlds_in_messages[world][1], message)  # call function
