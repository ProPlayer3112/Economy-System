import discord  ,  aiosqlite
from discord.ext import commands  ,  bridge
from discord.commands import slash_command, Option
from datetime import datetime

class Balance(commands.Cog):
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
        name='kontostand',
        description='Zeige einen Kontostand von einem Member an',
        aliases=['bal']
        )
    async def balance(self, ctx, member: Option(discord.Member, "Wähle einen Member aus", required= False)):
           user = member or ctx.author
           eco = discord.utils.get(self.client.emojis, name='1Dia')

           cash = await self.get_cash(user.id)
           bank = await self.get_bank(user.id)
           total = await self.get_bank(user.id) + await self.get_cash(user.id)

           em = discord.Embed(
              color=discord.Color.green(),
              timestamp=datetime.now()
           )
           em.add_field(
              name='Cash:',
              value=f' {eco} {cash:,}'
           )
           em.add_field(
              name='Bank:',
              value=f' {eco} {bank:,}'
           )
           em.add_field(
               name='Total:',
               value=f'{eco} {total:,}'
           )
           em.set_author(name=f"{user.name}'s Kontostand", icon_url=f'{user.avatar}')

           await ctx.respond(embed=em)




def setup(client):
    client.add_cog(Balance(client))