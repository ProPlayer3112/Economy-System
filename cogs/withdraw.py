import discord, aiosqlite
from discord.ext import commands, bridge
from datetime import datetime
from discord.commands import Option


class withdraw(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.DB = "economy.db"

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS economy (
                user_id INTEGER PRIMARY KEY,
                bank INTEGER DEFAULT 0,
                cash INTEGER DEFAULT 0
                )"""
            )
    async def check_user(self, user_id):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute("INSERT OR IGNORE INTO economy (user_id) VALUES (?)", (user_id,))
            await db.commit()

    async def get_cash(self, user_id):
        await self.check_user(user_id)
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT cash FROM economy WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()

        return result[0]

    async def get_bank(self, user_id):
        await self.check_user(user_id)
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT bank FROM economy WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()

        return result[0]

    @bridge.bridge_command(
        name='abheben',
        description='Hebe dein Geld von der Bank ab.',
        aliases=['with']
    )
    async def withdraw(self, ctx, *, amount=None):
        eco = discord.utils.get(self.client.emojis, name='1Dia')

        cash = await self.get_cash(ctx.author.id)
        bank = await self.get_bank(ctx.author.id)

        emErr = discord.Embed(
            description=f'Du hast nicht so viel Geld!',
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        emErr.add_field(
            name='Aktuelle Diamanten auf Ihrer Bank:',
            value=f'{eco} {bank:,}'
        )
        emErr.set_author(name=f"{ctx.author.name}", icon_url=f'{ctx.author.avatar}')

        if str(amount) == 'all':

            emA = discord.Embed(
                description=f'Du hast erfolgreich {eco} **{bank:,}** Diamanten abgehoben.',
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            emA.set_author(name=f"{ctx.author.name}", icon_url=f'{ctx.author.avatar}')

            await ctx.respond(embed=emA)

            async with aiosqlite.connect(self.DB) as db:
                async with db.execute("UPDATE economy SET cash = cash + bank, bank = 0 WHERE user_id = ?",
                                      (ctx.author.id,)) as cursor:
                    await db.commit()


        elif int(amount) > bank:
            return await ctx.send(embed=emErr)

        elif int(amount) < 0:
            return await ctx.send(embed=emErr)

        else:

            bank -= str(amount)
            cash += str(amount)

            async with aiosqlite.connect(self.DB) as db:
                async with db.execute("UPDATE economy SET bank = ?, cash = ? WHERE user_id = ?",
                                      (bank, cash, ctx.author.id)) as cursor:
                    await db.commit()

            em = discord.Embed(
                description=f'Du hast erfolgreich {eco} **{amount}** Diamanten abgehoben.',
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            em.set_author(name=f"{ctx.author.name}", icon_url=f'{ctx.author.avatar}')

            await ctx.respond(embed=em)


def setup(client):
    client.add_cog(withdraw(client))