import discord  ,  aiosqlite  ,  random
from discord.ext import commands  ,  bridge
from datetime import datetime
from EconomySystem import events


class rob(commands.Cog):
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


    @bridge.bridge_command(description='Beklaue jemanden um Geld zu verdienen')
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def klauen(self, ctx, member: discord.Member):
        eco = discord.utils.get(self.client.emojis, name='1Dia')

        cash = await self.get_cash(ctx.author.id)
        cash1 = await self.get_cash(member.id)

        em1 = discord.Embed(
            description=f'Es lohnt sich nicht.',
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        em1.set_author(name=f"{ctx.author.name}", icon_url=f'{ctx.author.avatar}')

        em2 = discord.Embed(
            description=f'Du kannst dich nicht selber beklauen!',
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        em2.set_author(name=f"{ctx.author.name}", icon_url=f'{ctx.author.avatar}')


        if cash1 < 100:
            await ctx.respond(embed=em1)
            return

        if member == ctx.author:
            await ctx.respond(embed=em2)
            return


        Chance = random.randint(1, 100)
        if Chance > 60:
            coins = random.randint(1, cash1)

            eventP = random.choice(events.RobP(coins, eco))

            em = discord.Embed(
                description=f'{eventP}',
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            em.set_author(name=f"{ctx.author.name}", icon_url=f'{ctx.author.avatar}')

            async with aiosqlite.connect(self.DB) as db:
                async with db.execute("UPDATE economy SET cash = cash + ? WHERE user_id = ?", (coins, ctx.author.id)) as cursor:
                    await db.commit()

            async with aiosqlite.connect(self.DB) as db:
                async with db.execute("UPDATE economy SET cash = cash - ? WHERE user_id = ?", (coins, member.id)) as cursor:
                    await db.commit()

            await ctx.respond(embed=em)


        else:
            coinsN = random.randint(1, 175)

            eventN = random.choice(events.RobN(coinsN, eco))

            em2 = discord.Embed(
                description=f'{eventN}',
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            em2.set_author(name=f"{ctx.author.name}", icon_url=f'{ctx.author.avatar}')

            async with aiosqlite.connect(self.DB) as db:
                async with db.execute("UPDATE economy SET cash = cash - ? WHERE user_id = ?", (coinsN, ctx.author.id)) as cursor:
                    await db.commit()

            async with aiosqlite.connect(self.DB) as db:
                async with db.execute("UPDATE economy SET cash = cash + ? WHERE user_id = ?", (coinsN, member.id)) as cursor:
                    await db.commit()

            await ctx.respond(embed=em2)


def setup(client):
    client.add_cog(rob(client))