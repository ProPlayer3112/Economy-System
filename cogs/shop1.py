import discord  ,  aiosqlite  ,  random
from discord.ext import commands  ,  bridge
from datetime import datetime
from EconomySystem import events


class shop1(commands.Cog):
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




    @bridge.bridge_command(
        name='item-kaufen',
        description='Kaufe dir ein Item aus dem Shop.',
        aliases=['item1']
    )
    async def buyitem(self, ctx: bridge.BridgeContext, item=None):
        eco = discord.utils.get(self.client.emojis, name='1Dia')
        role1 = 1080231895389978714
        user = ctx.author
        role = ctx.author.guild.get_role(role1)
        cash = await self.get_cash(ctx.author.id)
        bank = await self.get_bank(ctx.author.id)
        total = await self.get_bank(ctx.author.id) + await self.get_cash(ctx.author.id)
        amount = 50



        if role in user.roles:
            await ctx.respond("Du hast die Rolle schon", ephemeral=True)
        else:
            if str(item) == 'Bettler':
               if int(amount) < total:
                   coins = 50

                   eventB = random.choice(events.buyP(coins, eco))

                   emA = discord.Embed(
                      description=eventB,
                      color=discord.Color.green(),
                      timestamp=datetime.now()
                    )
                   emA.set_author(name=f"{ctx.author.name}", icon_url=f'{ctx.author.avatar}')







                   async with aiosqlite.connect(self.DB) as db:
                      async with db.execute("UPDATE economy SET cash = cash - ? WHERE user_id = ?",
                                          (coins, ctx.author.id)) as cursor:
                          await db.commit()

                   await ctx.author.add_roles(role)
                   await ctx.respond(embed=emA)

               elif int(amount) > total:
                    emErr = discord.Embed(
                       description=f'Du hast nur {eco}{total} Diamanten von {eco}{amount} Diamanten .',
                       color=discord.Color.green(),
                       timestamp=datetime.now())

                    return await ctx.respond(embed=emErr)


def setup(client):
   client.add_cog(shop1(client))