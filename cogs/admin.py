import discord  ,  aiosqlite  ,  random
from discord.ext import commands  ,  bridge
from datetime import datetime
from EconomySystem import events


class give(commands.Cog):
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
        await self.check_user( user_id)
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT cash FROM economy WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()

        return result[0]

    async def get_bank(self, user_id):
        await self.check_user( user_id)
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT bank FROM economy WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()

        return result[0]


    @bridge.bridge_command(description='Schenke einem bestimmten Member Diamanten!(Admin Befehl)')
    @discord.default_permissions(administrator=True)
    async def schenken(self, ctx, member: discord.Member, amount: int):
        eco = discord.utils.get(self.client.emojis, name='1Dia')

        cash = await self.get_cash(ctx.author.id)
        cash1 = await self.get_cash(member.id)
        coins = amount

        em1 = discord.Embed(
            description=f'{member.mention} hat {eco} {amount} Diamanten erhalten.',
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        em1.set_author(name=f"{ctx.author.name}", icon_url=f'{ctx.author.avatar}')





        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("UPDATE economy SET cash = cash + ? WHERE user_id = ?", (coins, member.id)) as cursor:
                    await db.commit()

        await ctx.respond(embed=em1)

    @bridge.bridge_command(description='Nimm Diamanten von einem Member weg!(Admin Befehl)')
    @discord.default_permissions(administrator=True)
    async def wegnehmen(self, ctx, member: discord.Member, amount: int):
        eco = discord.utils.get(self.client.emojis, name='1Dia')

        cash = await self.get_cash(ctx.author.id)
        cash1 = await self.get_cash(member.id)
        coins = amount

        em4 = discord.Embed(
            description=f'{member.mention} wurden {eco} {amount} Diamanten weggenommen.',
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        em4.set_author(name=f"{ctx.author.name}", icon_url=f'{ctx.author.avatar}')

        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("UPDATE economy SET cash = cash - ? WHERE user_id = ?", (coins, member.id)) as cursor:
                await db.commit()

        await ctx.respond(embed=em4)




def setup(client):
    client.add_cog(give(client))