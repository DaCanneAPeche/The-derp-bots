import discord


def join_board(board):
    joined_board = []

    for row in board:
        joined_board.append(" | ".join(map(str, row)))

    return "\n".join(joined_board)


def equal_three(a, b, c):
    return a == b and b == c and not type(a) == int


class TicTacToe:

    def __init__(self, player1, player2, ctx, bot):
        self.ctx = ctx
        self.player1 = player1
        self.player2 = player2

        self.bot = bot

        self.msg = None

        self.channel = self.bot.get_channel(self.ctx.channel.id)
        self.board = [[1, 2, 3],
                      [4, 5, 6],
                      [7, 8, 9]]

        self.player_O = False

        self.cross = 'X'
        self.circle = 'O'

        self.winner = ''

    async def start(self):
        emojis = ['✅', '❎']

        self.msg = (await self.ctx.send(
            f'{self.player2.mention}, acceptes-tu la demande de duel par `tic tac toe` / `morpion` de '
            f'{self.player1.mention} ?'), 'start')

        for emoji in emojis:

            if self.msg[1] == 'start':
                await self.msg[0].add_reaction(emoji)

    async def next(self, all_morpions):

        self.check_winner()

        if not self.winner == '':
            await self.finish(all_morpions)

        else:

            await self.remove_message(self.msg[0])

            print('next')

            reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

            for i in range(3):
                for x in range(3):

                    if not type(self.board[i][x]) == int:
                        reactions[i * 3 + x] = None
                        print('None')

            sending_board = join_board(self.board)

            embed = discord.Embed(
                title=f'C\'est le tour du joueur X !\n({self.player2.display_name})',
                description=f'```{sending_board}```',
                colour=discord.Color.blue()
            )

            if self.player_O:
                embed.title = f'C\'est le tour du joueur 0 !\n({self.player1.display_name})'
                embed.colour = discord.Color.red()

            self.msg = (await self.ctx.send(embed=embed), 'turning')

            for reaction in reactions:

                if reaction is not None:
                    await self.msg[0].add_reaction(reaction)
                    print('reacting')

    async def finish(self, all_morpions):

        if self.winner == '':

            await self.player1.send(f'Bah {self.player2.mention} il veux pas')

        elif self.winner == 'no':

            await self.ctx.send('Égalité !')

        elif type(self.winner) == str:

            await self.congratulate_winner(self.winner, all_morpions)

        else:

            await self.ctx.send('Partie annulée !')
        all_morpions.remove(self)

    async def remove_message(self, message):

        await message.delete()
        print('removing message')

    def check_winner(self):

        winner = ''

        board = self.board

        for i in range(3):

            if equal_three(board[i][0], board[i][1], board[i][2]):  # check ---

                winner = board[i][0]

            if equal_three(board[0][i], board[1][i], board[2][i]):  # check |

                winner = board[0][i]

        if equal_three(board[0][0], board[1][1], board[2][2]):

            winner = board[1][1]

        elif equal_three(board[0][2], board[1][1], board[2][0]):

            winner = board[1][1]

        elif type(board[0][0]) == str and type(board[0][1]) == str and type(board[0][2]) == str and \
                type(board[1][0]) == str and type(board[1][1]) == str and type(board[1][2]) == str and \
                type(board[2][0]) == str and type(board[2][1]) == str and type(board[2][2]) == str:

            winner = 'no'

        self.winner = winner

    async def congratulate_winner(self, player, all_morpions):

        await self.remove_message(self.msg[0])

        embed = discord.Embed(
            title=f'Le joueur X ({self.player2.display_name}) gagne !',
            description='Bravo à lui !',
            colour=discord.Color.blue()
        )

        if player == 'O':

            embed.title = f'Le joueur O ({self.player1.display_name}) gagne !'
            embed.colour = discord.Color.red()
            await self.player1.send('Bravo à toi !')
            await self.player2.send('Tu feras mieux la prochaine fois !')

        else:
            await self.player1.send('Tu feras mieux la prochaine fois !')
            await self.player2.send('Bravo à toi !')

        await self.ctx.send(embed=embed)

        await self.finish(all_morpions)
