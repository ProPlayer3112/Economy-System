import discord  ,  aiosqlite  ,  random
from discord.ext import commands  ,  bridge
from datetime import datetime
from EconomySystem import events


class slut(commands.Cog):
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


    @bridge.bridge_command(description='Sei eine Schlampe, um ein paar Münzen zu verdienen')
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def slut(self, ctx):
        eco = discord.utils.get(self.client.emojis, name='1Dia')

        Chance = random.randint(1, 100)
        if Chance > 60:
            coins = random.randint(20, 80)

            eventP = random.choice(events.slutP(coins, eco))

            em = discord.Embed(
                description=f'{eventP}',
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            em.set_author(name=f"{ctx.author.name}", icon_url=f'{ctx.author.avatar}')

            async with aiosqlite.connect(self.DB) as db:
                async with db.execute("UPDATE economy SET cash = cash + ? WHERE user_id = ?", (coins, ctx.author.id)) as cursor:
                    await db.commit()

            await ctx.respond(embed=em)


        else:
            coinsN = random.randint(10, 70)

            eventN = random.choice(events.slutN(coinsN, eco))

            em2 = discord.Embed(
                description=f'{eventN}',
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            em2.set_author(name=f"{ctx.author.name}", icon_url=f'{ctx.author.avatar}')

            async with aiosqlite.connect(self.DB) as db:
                async with db.execute("UPDATE economy SET cash = cash - ? WHERE user_id = ?", (coinsN, ctx.author.id)) as cursor:
                    await db.commit()

            await ctx.respond(embed=em2)





def setup(client):
    client.add_cog(slut(client))