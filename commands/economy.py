import discord
from discord.ext import commands
import sqlite3

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("database/database.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 100)")
        self.conn.commit()

    @commands.command()
    async def رصيد(self, ctx):
        """عرض رصيد المستخدم"""
        user_id = ctx.author.id
        self.cur.execute("SELECT balance FROM users WHERE id=?", (user_id,))
        balance = self.cur.fetchone()
        
        if not balance:
            self.cur.execute("INSERT INTO users (id) VALUES (?)", (user_id,))
            self.conn.commit()
            balance = (100,)

        await ctx.send(f"💰 {ctx.author.mention} رصيدك: {balance[0]} عملة!")

# 🔹 هذه الدالة هي السبب في المشكلة، تأكد من أنها موجودة
async def setup(bot):
    await bot.add_cog(Economy(bot))
