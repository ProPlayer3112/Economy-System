import discord  ,  aiosqlite
from discord.ext import commands  ,  bridge
from datetime import datetime

class Shop(commands.Cog):
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
        name='shop',
        description='Lasse dir den Shop anzeigen.',
        aliases=['shop1']
        )
    async def balance(self, ctx):
        eco = discord.utils.get(self.client.emojis, name='1Dia')

        cash = await self.get_cash(ctx.author.id)
        bank = await self.get_bank(ctx.author.id)
        total = await self.get_bank(ctx.author.id) + await self.get_cash(ctx.author.id)

        em = discord.Embed(title="🌌ProNight🌌-Shop",description="**Verwende den Befehl `item-kaufen <Name>` um einen Artikel zu kaufen.**"
            "\n"
            f"{eco}50 - Bettler |<:Level1:1080229242064879719>"
            "Vorteile: Du bekommst die Rolle `Bettler`",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        await ctx.respond(embed=em)





def setup(client):
    client.add_cog(Shop(client))